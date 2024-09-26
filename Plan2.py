import numpy as np
import pandas as pd
import random

# Constants and Variables
num_of_programs = 8
num_groups = 28
num_tasks = 28
num_days = 7
group_numbers_of_programs = {
    "program_1": 7,
    "program_2": 6,
    "program_3": 8,
    "program_4": 2,
    "program 5": 3,
    "program 6": 1,
    "program 7": 1
}
programs_easy_task_days = {
    "program_1": None,
    "program_2": None,
    "program_3": None,
    "program_4": None,
    "program 5": [3,7],
    "program 6": None,
    "program 7": [3,7]
}
# Loading the Excel file
file_path = './Task List for 28 people.xlsx' 
task_data = pd.read_excel(file_path)
task_names = task_data['Tasks'].tolist()


# Define the costs for each task type
variables = {
    'w_1': 1,
    'w_2': 3,
    'w_3': 5,
    'w_4': 7,
    "w_5": 5
}

# Replacing the cost labels with the corresponding numerical values
task_data['Costs'] = task_data['Costs'].replace(variables)

# Creating Group Details DataFrame
group_details = []
group_number = 0
for program, num_groups in group_numbers_of_programs.items():
    for _ in range(num_groups):
        group_details.append({
            "group_id": group_number,
            "program": program
        })
        group_number += 1
group_details_df = pd.DataFrame(group_details)

# Adding Easy Task Days to Group Details
group_details_df['easy_task_days'] = [
    programs_easy_task_days[program] or [] for program in group_details_df['program']
]

group_details_with_easy_task_days = group_details_df[['group_id', 'easy_task_days']]

# Creating The İnitial Task Schedule

# Recalculating num_groups based on group_numbers_of_programs
num_groups_corrected = sum(group_numbers_of_programs.values())

# Creating the task_schedule with the correct dimensions (num_groups_corrected, num_tasks, num_days)
task_schedule = np.zeros((num_groups_corrected, num_tasks, num_days), dtype=int)

# Determining Groups with Easy Task Day
easy_task_groups_by_day = {}
for day in range(1, num_days + 1):
    easy_task_groups = []
    for group in range(num_groups_corrected):
        program = group_details_df.loc[group, 'program']
        if programs_easy_task_days[program] and day in programs_easy_task_days[program]:
            easy_task_groups.append(group)
    easy_task_groups_by_day[f"Day {day}"] = easy_task_groups

# Assigning Easy Tasks
easy_tasks = list(range(num_tasks))  # Assuming tasks are numbered from 0 to num_tasks-1
remaining_task_list_total=[]
for day in range(1, num_days + 1):
    easy_task_groups = easy_task_groups_by_day[f"Day {day}"]
    easy_tasks_count = len(easy_task_groups)
    
    # Creating the easy_task_list for the current day
    easy_task_list = easy_tasks[:easy_tasks_count]
    
    # Shuffling the easy_task_list for random assignment
    random.shuffle(easy_task_list)
    
    day_index = day - 1
    for i, group in enumerate(easy_task_groups):
        task = easy_task_list[i]
        task_schedule[group, task, day_index] = 1  # Assigning the task to the group on the specified day

    # Creating the remaining_task_list
    remaining_task_list = list(set(range(num_tasks)) - set(easy_task_list))
    remaining_task_list_total.append(remaining_task_list)

    # Assigning Remaining Tasks
    remaining_task_groups = [group for group in range(num_groups_corrected) if group not in easy_task_groups_by_day[f"Day {day}"]]
    remaining_tasks_count = len(remaining_task_groups)
    
    
    # Shuffling the remaining_task_list for random assignment
    random.shuffle(remaining_task_list)
    
    for i, group in enumerate(remaining_task_groups):
        task = remaining_task_list[i]
        task_schedule[group, task, day_index] = 1  # Assigning the task to the group on the specified day

initial_schedule=task_schedule

def calculate_total_costs(task_schedule):
    total_costs_per_group = {}
    
    # Iterate through days and groups to calculate costs
    for group in range(num_groups_corrected):
        total_costs = 0
        for day in range(num_days):
            tasks_assigned = np.where(task_schedule[group, :, day] == 1)[0]
            for task in tasks_assigned:
                total_costs += task_data.at[int(task),"Costs"]
        total_costs_per_group[group] = total_costs
    
    return total_costs_per_group

def calculate_cost_difference(task_schedule):
    costs=calculate_total_costs(task_schedule)
    min_cost = min(costs.values())
    max_cost = max(costs.values())
    return max_cost-min_cost

def constraint_1(task_schedule):
    total_overlaps = 0
    
    # Iterate through days and tasks to count overlaps
    for day in range(num_days):
        for task in range(num_tasks):
            groups_assigned = np.where(task_schedule[:, task, day] == 1)[0]
            overlaps = len(groups_assigned) - 1 
            total_overlaps += overlaps
    
    return total_overlaps

def constraint_2(task_schedule):
    total_double_assignments = 0
    
    # Iterate through days and groups to count double assignments
    for day in range(num_days):
        for group in range(num_groups_corrected):
            tasks_assigned = np.where(task_schedule[group, :, day] == 1)[0]
            assignments = len(tasks_assigned)
            if assignments > 1:
                total_double_assignments += assignments - 1
            else:
                total_double_assignments=0
    return total_double_assignments

def constraint_3(task_schedule):
    total_overlaps_of_task = 0
    
    for group in range(num_groups_corrected):
        for task in range(num_tasks):
            task_assigned = np.where(task_schedule[group, task, : ] == 1)[0]
            overlaps = len(task_assigned) - 1 
            total_overlaps_of_task += overlaps
            if total_overlaps_of_task > 1:
                return total_overlaps_of_task
            else:
                return 0
    

def neighbor_schedule(task_schedule):
    new_schedule = task_schedule.copy()

    # Choose two distinct random groups
    group1 = random.randint(0, num_groups_corrected - 1)
    group2 = random.randint(0, num_groups_corrected - 1)
    while group2 == group1:
        group2 = random.randint(0, num_groups_corrected - 1)

    # Choose a random day and task
    day = random.randint(0, num_days - 1)
    task_1 = None
    for j in range(0, num_tasks):
        if new_schedule[group1, j, day] == 1:
            task_1 = j
            break
    task_2 = None
    for j in range(0, num_tasks):
        if new_schedule[group2, j, day] == 1:
            task_2 = j
            break

    # Swap the task assignments between the two groups for the selected day
    """new_schedule[group1, task_1, day], new_schedule[group2, task_2, day] = new_schedule[group2, task_2, day], new_schedule[group1, task_1, day]"""
    new_schedule[group1,task_1,day]=0
    new_schedule[group1,task_2,day]=1
    new_schedule[group2,task_2,day]=0
    new_schedule[group2,task_1,day]=1
    
    return new_schedule


def task_penalty(task_schedule):
    total_penalty = 0
    for day in range(num_days):
        for group in range(num_groups_corrected):
            program = group_details_df.loc[group, 'program']
            if programs_easy_task_days[program] and day + 1 in programs_easy_task_days[program]:
                for task in remaining_task_list_total[day]:
                    if task_schedule[group, task, day] == 1:
                        total_penalty += 10000
    
    return total_penalty


def objective_function(task_schedule):
    r_1=10000
    r_2=10000
    r_3=10000
    r_4=10000
    total_costs_per_group = calculate_cost_difference(task_schedule)
    a = constraint_1(task_schedule)
    b = constraint_2(task_schedule)
    c = task_penalty(task_schedule)
    d = constraint_3(task_schedule)
    
    return total_costs_per_group+ r_1 * a + r_2 * b + r_3 * c + r_4 * d

def simulated_annealing(initial_schedule, initial_temperature, cooling_rate, max_iterations):
    current_solution = initial_schedule
    current_objective = objective_function(current_solution)
    best_solution = current_solution
    best_objective = current_objective
    temperature = initial_temperature
    iteration = 1
    
    while temperature > 1e-6 and iteration <= max_iterations:
        new_solution = neighbor_schedule(current_solution)
        new_objective = objective_function(new_solution)

        # Calculate the change in objective value
        delta_objective = new_objective - current_objective

        # If the new solution is better or accepted probabilistically
        if delta_objective < 0 or random.random() < np.exp(-delta_objective / temperature):
            current_solution = new_solution
            current_objective = new_objective

            # Update the best solution if needed
            if new_objective < best_objective:
                best_solution = new_solution
                best_objective = new_objective

        # Cool down the temperature
        temperature *= cooling_rate

        iteration += 1

    return best_solution, best_objective

# Define parameters
initial_temperature = 10000.0
cooling_rate = 0.99
max_iterations = 15000

# Call simulated annealing function
final_solution, final_objective = simulated_annealing(initial_schedule, initial_temperature, cooling_rate, max_iterations)
print(final_solution)
print(calculate_total_costs(final_solution))
print(calculate_cost_difference(final_solution))

filtered_schedule={}
for i in range(0,num_groups_corrected):
    for k in range(0,7):
        for j in range(0,num_tasks):
            if final_solution[i,j,k] == 1:
                filtered_schedule[(i+1,j+1,k+1)] = "1"

# Create lists to hold the separate components of the tuple keys
index_tuples = list(filtered_schedule.keys())
value = list(filtered_schedule.values())

# Create a DataFrame
df = pd.DataFrame({
    "Index Tuple": index_tuples,
    "Value": value
})

# Export the DataFrame to an Excel file
excel_file_path = "output.xlsx"
df.to_excel(excel_file_path, index=False)

df = pd.read_excel(excel_file_path)

# Create a dictionary to store the organized data
organized_data = {}

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    index_tuple = row['Index Tuple']
    value = row['Value']
    i, j, k = map(int, index_tuple.strip('()').split(','))  # Extract i, j, k as integers
    day = f"Day {k}"
    group = f"Group {i}"
    
    if day not in organized_data:
        organized_data[day] = {}
    
    organized_data[day][group] = task_names[j-1] 

# Sort the days in ascending order
sorted_days = sorted(organized_data.keys(), key=lambda day: int(day.split()[1]))

# Create a new DataFrame from the organized data with sorted days
new_df = pd.DataFrame({day: organized_data[day] for day in sorted_days})

# Export the DataFrame to a new Excel file

output_excel_file = "output_organized_sorted.xlsx"
new_df.to_excel(output_excel_file)


