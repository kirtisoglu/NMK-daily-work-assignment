import random
import math

num_groups=int(input("Enter number of groups: "))
num_tasks=num_groups
task_costs = [1,2,5,8,9]
num_days=7

import random
import math

def get_initial_schedule(num_groups, num_days):
    """
    Generate a random initial schedule where each group is assigned a unique task for each day.
    """
    all_tasks = list(range(num_groups))
    initial_schedule = [random.sample(all_tasks, num_groups) for _ in range(num_days)]
    return initial_schedule


def calculate_cost_difference(schedule, task_costs):
    """
    Calculate the difference in costs among the groups in the given schedule.
    """
    group_costs = [0] * len(schedule[0])
    for day in schedule:
        for group, task in enumerate(day):
            group_costs[group] += task_costs[task]
    return max(group_costs) - min(group_costs)

def neighbor_schedule(current_schedule, num_groups):
    """
    Generate a neighbor schedule by swapping tasks between two days.
    """
    day_to_swap = random.randint(0, len(current_schedule) - 1)
    task_to_swap1, task_to_swap2 = random.sample(range(num_groups), 2)

    neighbor_schedule = [day.copy() for day in current_schedule]
    neighbor_schedule[day_to_swap][task_to_swap1], neighbor_schedule[day_to_swap][task_to_swap2] = \
        neighbor_schedule[day_to_swap][task_to_swap2], neighbor_schedule[day_to_swap][task_to_swap1]
    return neighbor_schedule

def simulated_annealing(task_costs, num_groups, num_days, initial_temperature=1000, cooling_rate=0.99, iterations=1000):
    """
    Simulated annealing algorithm for task scheduling with cost balancing among groups.
    """
    current_schedule = get_initial_schedule(num_groups, num_days)
    current_cost_difference = calculate_cost_difference(current_schedule, task_costs)

    best_schedule = current_schedule
    best_cost_difference = current_cost_difference

    temperature = initial_temperature

    for _ in range(iterations):
        new_schedule = neighbor_schedule(current_schedule, num_groups)
        new_cost_difference = calculate_cost_difference(new_schedule, task_costs)

        if new_cost_difference < current_cost_difference or random.random() < math.exp((current_cost_difference - new_cost_difference) / temperature):
            current_schedule = new_schedule
            current_cost_difference = new_cost_difference

            if new_cost_difference < best_cost_difference:
                best_schedule = new_schedule
                best_cost_difference = new_cost_difference

        temperature *= cooling_rate

    return best_schedule

best_schedule= simulated_annealing(task_costs, num_groups,7)
for i in range(len(best_schedule)):
    for j in range(len(best_schedule[i])):
        best_schedule[i][j] += 1

print("Best schedule:", best_schedule)
print("Tasks of Monday for each group are",best_schedule[0],"\n" "Tasks of Tuesday for each group are",best_schedule[1],"\n","Tasks of Wednesday for each group are",best_schedule[2],"\n","Tasks of Thursday for each group are",best_schedule[3],"\n","Tasks of Friday for each group are",best_schedule[4],"\n""Tasks of Saturday for each group are",best_schedule[5],"\n""Tasks of Sunday for each group are",best_schedule[6],"respectively.")
