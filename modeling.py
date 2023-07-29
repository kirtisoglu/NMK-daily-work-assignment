from pulp import LpProblem, LpVariable, LpBinary, LpMaximize, LpStatus

def solve_task_distribution(num_participants, num_weeks, num_tasks, tasks_per_group):
    # Create the optimization problem
    model = LpProblem("Task Distribution", LpMaximize)

    # Create decision variables
    x = {}  # x[i, j, k] represents whether participant i is assigned task k in week j
    for i in range(1, num_participants+1):
        for j in range(1, num_weeks+1):
            for k in range(1, num_tasks+1):
                x[i, j, k] = LpVariable(f"x_{i}_{j}_{k}", cat=LpBinary)

    # Define the objective function (minimize the ?)
    model += sum(x[i, j, k] for i in range(1, num_participants+1)
                 for j in range(1, num_weeks+1)
                 for k in range(1, num_tasks+1))

    # Add constraints: each task is assigned to exactly one participant in each week
    for j in range(1, num_weeks+1):
        for k in range(1, num_tasks+1):
            model += sum(x[i, j, k] for i in range(1, num_participants+1)) == 1

    # Add constraints: each participant is assigned to at most one task in each week
    for i in range(1, num_participants+1):
        for j in range(1, num_weeks+1):
            model += sum(x[i, j, k] for k in range(1, num_tasks+1)) <= 1

    # Add constraints: each task should have the desired number of participants
    for j in range(1, num_weeks+1):
        for k in range(1, num_tasks+1):
            model += sum(x[i, j, k] for i in range(1, num_participants+1)) == tasks_per_group[k-1]

    # Solve the optimization problem
    status = model.solve()

    if status == 1:  # The problem has been solved
        # Print the optimal task assignment
        print("Optimal Task Assignment:")
        for j in range(1, num_weeks+1):
            print(f"Week {j}:")
            for k in range(1, num_tasks+1):
                print(f"Task {k}:")
                for i in range(1, num_participants+1):
                    if x[i, j, k].value() == 1:
                        print(f"Participant {i}")
                print()
    else:
        print("No feasible solution found.")

    # Print the status of the problem (e.g., Optimal, Infeasible, Unbounded, etc.)
    print("Status:", LpStatus[status])

# Example usage
num_participants = 500
num_weeks = 4
num_tasks = 5
tasks_per_group = [4, 3, 3, 2, 2]  # Number of participants required for each task

solve_task_distribution(num_participants, num_weeks, num_tasks, tasks_per_group)

