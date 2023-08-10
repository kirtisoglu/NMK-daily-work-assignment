# We will assign daily-tasks to groups every week. 
# This program does not remember what are assigned the last week. 
# Define the libraries you need.
import pandas as pd
from pulp import LpVariable, LpProblem, LpBinary, LpMinimize, value, lpSum
import random


# Define task lists of length 15, 20, 25, 30. 
# Define their weight lists using parameters. Weights should be w_1, w_2, w_3, w_4.
# And so we can change w_i's and test the result for different w_i's.
# w_1's are easy tasks for off days. We will add a constraint for that.

print("Hoş geldiniz")

excel_file = './ornekgorev.xlsx' 
sheet_name = 'Sayfa1'
print("Görevleriniz {} dosyasında,{} sayfasından okunuyor".format(excel_file, sheet_name))


data = pd.read_excel(excel_file, sheet_name=sheet_name)
allTasks = data.values

## Define the first column as task names and the corresponding second column as the weight of it.




## Define w_1, w_2, w_3, w_4.
## For example, let's take w_1=1, w_2=3, w_3=5, w=4=7 and see what happens.



task_names = allTasks[:, 0]
weights = allTasks[:, 1]

## Define w_1, w_2, w_3, w_4.
## For example, let's take w_1=1, w_2=3, w_3=5, w=4=7 and see what happens.
variables = {
    'w_1': 1,
    'w_2': 3,
    'w_3': 5,
    'w_4': 7
}
#print(variables[allTasks[0][1]]) gives the first tasks weight

# Create two different types of each program. 
# One has an off day in the week, the other does not have. 
# OR Ask program name, number of groups, and off day of the program as an input and skip the following.

days = {
    "pazartesi": 1,
    "salı": 2,
    "çarşamba": 3,
    "perşembe": 4,
    "cuma": 5,
    "cumartesi": 6,
    "pazar": 7
}

num_of_groups_with_easy_task_day = None
easy_task_days = []

while True:
    try:
        num_of_groups_with_easy_task_day = int(input("Tatil günleri olan grupların sayısını giriniz: "))
        if num_of_groups_with_easy_task_day < 0:
            print("Lütfen 0 veya daha büyük bir değer girin.")
        else:
            break
    except ValueError:
        print("Geçerli bir tam sayı girmediniz. Lütfen tekrar deneyin.")

while True:
    try:
        easy_task_days_input = input("Grupların tatil günlerini virgül ile ayırarak giriniz: ").split(',')
        for day in easy_task_days_input:
            day = day.strip().lower()
            if day in days:
                numerical_value = days.get(day)
                easy_task_days.append(day)
            else:
                print(f"'{day}' geçerli bir gün ismi değil. Lütfen tekrar deneyin.")
        break
    except ValueError:
        print("Geçerli bir gün ismi girmediniz. Lütfen tekrar deneyin.")

num_of_groups_without_easy_task_day = None

while True:
    try:
        num_of_groups_without_easy_task_day = int(input("Tatil günleri olmayan grupların sayısını giriniz: "))
        if num_of_groups_without_easy_task_day < 0:
            print("Lütfen 0 veya daha büyük bir değer girin.")
        else:
            break
    except ValueError:
        print("Geçerli bir tam sayı girmediniz. Lütfen tekrar deneyin.")

# Merge the programs in an order and calculate n.

allGroups = []

for i in range(0, num_of_groups_with_easy_task_day +num_of_groups_without_easy_task_day):
    allGroups.append({
        "id": i + 1,
        "has_easy_task_days": i< num_of_groups_with_easy_task_day,
    })
    
allGroupsLength = len(allGroups)
taskList = allTasks[0:allGroupsLength]







# Now we know task lists, programs and their numbers, off days of programs, easy tasks. 
# Dfine the objective function by using n, weights, and the main task list. 



## We might have different off-days, not only wednesday.
## Call it easy-task-day. For example, undergrad programs might have
## both wednesday and sunday to have easy tasks since sunday is the last day
## for their program and some of the group members leave the village.  
## So, it is possible to have 2 easy-task-day for a group. 
 
## Imagine you learned the easy-task-day of a group. How do you teach this to
## your integer program? For the decision variable x_{ijk}, k indicates the days of week. 
## k=3 for wednesday. Define a set of easy tasks E. Here is the constraint:
## x_{ij3}=0 for groups i (i must be defined by using inputs) for all j in E_c, the complement of E.
## Since we have a constraint to assign a task every day to each group, 
## a task is assigned to group i on Wednesday from E.

# Merge the programs in an order and calculate n.
# Pick the first list whose length exceed n. 
# Delete unneccesary tasks from the list. 
# Define it as the main task list.


# Now we know task lists, programs and their numbers, off days of programs, easy tasks. 
# Define the objective function by using n, weights, and the main task list. 

I = allGroupsLength
J = allGroupsLength
K = 7

problem = LpProblem("NMK-daily-work-assignment", LpMinimize)

x_values = {}


for i in range(1,I + 1):
    for j in range(1,J + 1):
        for k in range(1,K + 1):
            var_name = f'x_{i}_{j}_{k}'
            x_values[(i, j, k)] = LpVariable(var_name, cat=LpBinary)
            
#print(x_values[(0,0,0)].value())

 
#Create C_i's
C_i = []
for i in range(1, I + 1):
    variable_name = f"C_{i}"
    new_variable = LpVariable(variable_name, lowBound=0)
    C_i.append(new_variable)

def calculate_C_individual(i):
    sum=0
    for j in range(1,allGroupsLength+1):
        for k in range(1,8):
            sum+=x_values[(i, j, k)].value()
    return sum
#print(calculate_C_individual(1))

C = LpVariable("C", lowBound=0) 

#Define C_i's
C_i = [calculate_C_individual(i) for i in range(1, I + 1)]
for i in range(1, I + 1):
    problem += C >= C_i[i - 1]

#objective function
problem += C

problem.solve()

print("Optimal value of C:", value(C))


# Define constraints.


#her gruba her gün 1 görev
for j in range(1, J + 1):
    for k in range(1, K + 1):
        problem += lpSum(x_values[(i, j, k)] for i in range(1, I + 1)) == 1



#Hocam C_i'lara ihtiyacım var C için ama C'i leri bilmiyorum çünkü x_values'ı bilmiyorum.

# Construct Simulated Annealing and solve the problem.




# Convert your solution vector to a daily-task assignment of groups. 




# Print the task assignment as a table. Save the table.