# We will assign daily-tasks to groups every week. 
# This program does not remember what are assigned the last week. 
# Define the libraries you need.
import pandas as pd
import numpy as np
import random
import math

print("Hoş geldiniz")

excel_file = './ornekgorev.xlsx' 
sheet_name = 'Sayfa1'
print("Görevleriniz {} dosyasında,{} sayfasından okunuyor".format(excel_file, sheet_name))


data = pd.read_excel(excel_file, sheet_name=sheet_name)
#taskList w_1 lerden başlasın w_3 lere geçsin sonra w_2 ler sonra w_5 ler en son w_4 ler
allTasks = data.values
taskList= allTasks #beni düzelt sonra
task_names = taskList[:, 0]

num_of_programs=4
programs_easy_task_days = {
    "program_1": [2,3],
    "program_2": [2,4],
    "program_3": [7],
    "program_4": None
}
num_groups = 30
group_numbers_of_programs = {
    "program_1": 5,
    "program_2": 10,
    "program_3": 7,
    "program_4": 8
}
allGroups = []

current_group = 1  # Initialize the current group counter

for program, group_count in group_numbers_of_programs.items():
    for i in range(group_count):
        group = {
            "id": current_group,
            "program type": program
        }
        allGroups.append(group)
        current_group += 1
        

num_tasks = 30
num_days = 7

r_1 = 20 #penalty parameter
r_2 = 20

task_schedule = {}

for group in range(1, num_groups + 1):
    for task in range(1, num_tasks + 1):
        for day in range(1, num_days + 1):
            task_schedule[(group, task, day)] = 0

# Define the weights for each task type
variables = {
    'w_1': 1,
    'w_2': 3,
    'w_3': 5,
    'w_4': 7,
    "w_5": 5
}

days = {
    "pazartesi": 1,
    "salı": 2,
    "çarşamba": 3,
    "perşembe": 4,
    "cuma": 5,
    "cumartesi": 6,
    "pazar": 7
}

# Define the cost difference calculation function
def calculate_C_individual(i, schedule):
    total_cost = 0
    for k in range(1, num_days + 1):
        for j in range(1, num_tasks + 1):
            if schedule.get((i, j, k), 0) == 1:
                total_cost += variables[allTasks[j - 1][1]]
    return total_cost

def calculate_cost_difference(schedule):
    group_costs = [calculate_C_individual(i, schedule) for i in range(1, num_groups + 1)]
    return max(group_costs) - min(group_costs)

# Define the neighbor schedule generation function
def neighbor_schedule(current_schedule):
    new_schedule = current_schedule.copy()

    # Choose a random task assignment to change
    group = random.randint(1, num_groups)
    task = random.randint(1, num_tasks)
    day = random.randint(1, num_days)
    # Toggle the assignment (0 to 1 or 1 to 0)
    new_schedule[(group, task, day)] = 1 - new_schedule.get((group, task, day), 0)

    return new_schedule

# Simulated Annealing algorithm
def simulated_annealing(initial_schedule, initial_temperature=1000, cooling_rate=0.99, iterations=1000):
    current_schedule = initial_schedule
    current_cost_difference = calculate_cost_difference(current_schedule)

    best_schedule = current_schedule
    best_cost_difference = current_cost_difference

    temperature = initial_temperature

    for _ in range(iterations):
        new_schedule = neighbor_schedule(current_schedule)
        new_cost_difference = calculate_cost_difference(new_schedule)

        if new_cost_difference < current_cost_difference or random.random() < math.exp((current_cost_difference - new_cost_difference) / temperature):
            current_schedule = new_schedule
            current_cost_difference = new_cost_difference

            if new_cost_difference < best_cost_difference:
                best_schedule = new_schedule
                best_cost_difference = new_cost_difference

        temperature *= cooling_rate

    return best_schedule

# Generate an initial schedule (you can modify this based on your logic)
def generate_initial_schedule():
    initial_schedule = task_schedule.copy() 

    for k in range(1, 8):
        count = 0
        programs=[]
        for key, value in programs_easy_task_days.items():
            if value is not None and k in value:
                count += group_numbers_of_programs[key]
                programs.append(key)      
        if count > 0:
            index=0
            index_1=0
            task_numbers_1=[i for i in range(1,count+1)]
            shuffled_easy_tasks=task_numbers_1.copy()
            random.shuffle(shuffled_easy_tasks)
            for i in range(1,num_groups+1):
                if allGroups[i-1]["program type"] in programs:
                    index+=1
                    initial_schedule[i,shuffled_easy_tasks[index-1],k]=1
                    #print(i,"th group", "got the", shuffled_easy_tasks[index-1], "task on",k,"th day")
            task_numbers_3=[i for i in range(count+1,num_groups+1)]
            shuffled_easy_tasks_2=task_numbers_3.copy()
            random.shuffle(shuffled_easy_tasks_2) 
            for i in range(1,num_groups+1):
                if allGroups[i-1]["program type"] not in programs:
                    #print(k,allGroups[i-1],"not")
                    index_1+=1
                    initial_schedule[i,shuffled_easy_tasks_2[index_1-1],k]=1
                    #print(i,"th group", "got the", shuffled_easy_tasks_2[index_1-1], "task on",k,"th day")
        else:
            task_numbers_2=[i for i in range(1, num_groups + 1)]
            shuffled_task_numbers_2 = task_numbers_2.copy()
            random.shuffle(shuffled_task_numbers_2)
            
            for group_number in range(1, num_groups + 1):
                initial_schedule[group_number, shuffled_task_numbers_2[group_number-1], k] = 1
                #print(group_number,"th group", "got the", shuffled_task_numbers_2[group_number-1], "task on",k,"th day")

    return initial_schedule

initial_schedule = generate_initial_schedule()



# Define the objective function and constraints
def objective_function(schedule):
    
    C_i=[]
    for i in range (1,num_groups+1):
        cost = calculate_C_individual(i,schedule)
        C_i.append(cost)
    C = max(C_i)
    
    #constraint_1 : iki gruba aynı görev atanmamalı
    sum_squared_1 = 0
    for k in range(1,8):
        for j in range(1,num_groups+1):
            sum_i = 0
            for i in range(1,num_groups+1):
                sum_i += schedule[(i, j, k)]
            """if sum_i!=1:
                print(sum_i,j,k)"""
            sum_squared_1 += (1 - sum_i)**2
    #print("a",sum_squared_1)
    
    #constraint 2: Each group should have exactly one task each day
    sum_squared_2 = 0
    for k in range(1,8):
        for i in range(1,num_groups+1):
            sum_j = 0
            for j in range(1,num_groups+1):
                sum_j += schedule[(i, j, k)]
            sum_squared_2 += (1 - sum_j)**2
    #print("b",sum_squared_2)
    obj= calculate_cost_difference(schedule)+ r_1 * sum_squared_1 +r_2 * sum_squared_2
    return obj


# Run the simulated annealing algorithm
best_schedule = simulated_annealing(initial_schedule, initial_temperature=1000, cooling_rate=0.99, iterations=1000)

# Print the best schedule and its cost difference
#print("Best Schedule:", best_schedule)
print("Cost Difference:", calculate_cost_difference(best_schedule))

filtered_schedule={}
for key, value in best_schedule.items():
    if value == 1:
        filtered_schedule[key] = value

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
    
    organized_data[day][group] = f"{allTasks[j - 1]}"

# Sort the days in ascending order
sorted_days = sorted(organized_data.keys(), key=lambda day: int(day.split()[1]))

# Create a new DataFrame from the organized data with sorted days
new_df = pd.DataFrame({day: organized_data[day] for day in sorted_days})

# Export the DataFrame to a new Excel file

output_excel_file = "output_organized_sorted.xlsx"
new_df.to_excel(output_excel_file)