# We will assign daily-tasks to groups every week. 
# This program does not remember what are assigned the last week. 
# Define the libraries you need.
import pandas as pd
import numpy as np
import random
import math

# Define your problem parameters here
num_groups = 30
num_tasks = 30
num_days = 7

# Define your task scheduling problem as a dictionary of groups and tasks
# For example: task_schedule[(group, task, day)] = 1 if the task is assigned to the group on the day
task_schedule = {}

# Define the weights for each task type
variables = {
    'w_1': 1,
    'w_2': 3,
    'w_3': 5,
    'w_4': 7
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
    current_cost_difference = calculate_cost_difference(initial_schedule)

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
    initial_schedule = {}  

    # generate the initial schedule here.

    return initial_schedule



# Define the objective function and constraints
def objective_function(schedule):
    return calculate_cost_difference(schedule)

def constraint_1(schedule):
    for j in range(1, num_tasks + 1):
        constraint_sum = sum(schedule.get((i, j, k), 0) for i in range(1, num_groups + 1) for k in range(1, num_days + 1))
        if constraint_sum != 1:
            return False
    return True

def constraint_2(schedule):
    for i in range(1, num_groups + 1):
        constraint_sum = sum(schedule.get((i, j, k), 0) for j in range(1, num_tasks + 1) for k in range(1, num_days + 1))
        if constraint_sum != 1:
            return False
    return True

# Run the simulated annealing algorithm
initial_schedule = generate_initial_schedule()
best_schedule = simulated_annealing(initial_schedule, initial_temperature=1000, cooling_rate=0.99, iterations=1000)

# Print the best schedule and its cost difference
print("Best Schedule:", best_schedule)
print("Cost Difference:", calculate_cost_difference(best_schedule))
