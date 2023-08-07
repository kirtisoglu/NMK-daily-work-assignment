# We will assign daily-tasks to groups every week. 
# This program does not remember what are assigned the last week. 
# Define the libraries you need.
import pandas as pd


# Define task lists of length 15, 20, 25, 30. 
# Define their weight lists using parameters. Weights should be w_1, w_2, w_3, w_4.
# And so we can change w_i's and test the result for different w_i's.
# w_1's are easy tasks for off days. We will add a constraint for that.

print("Hoş geldiniz")

excel_file = './ornekgorev.xlsx' 
sheet_name = 'Sayfa1'

print("Görevleriniz {} dosyasında,{} sayfasından okunuyor".format(excel_file, sheet_name))
## Why do you need this?

data = pd.read_excel(excel_file, sheet_name=sheet_name)
allTasks = data.values

## Define the first column as task names and the corresponding second column as the weight of it.




## Define w_1, w_2, w_3, w_4.
## For example, let's take w_1=1, w_2=3, w_3=5, w=4=7 and see what happens.




# Create two different types of each program. 
# One has an off day in the week, the other does not have. 
# OR Ask program name, number of groups, and off day of the program as an input and skip the following.

while True:
    try:
        num_of_groups_with_off_day = int(input("Çarşamba günü tatil yapacak olan grupların sayısını giriniz: "))
        if num_of_groups_with_off_day < 0:
            print("Lütfen 0 veya daha büyük bir değer girin.")
        else:
            break
    except ValueError:
        print("Geçerli bir tam sayı girmediniz. Lütfen tekrar deneyin.")

while True:
    try:
        num_of_groups_without_off_day = int(input("Tatil yapmayan grupların sayısını giriniz: "))
        if num_of_groups_without_off_day < 0:
            print("Lütfen 0 veya daha büyük bir değer girin.")
        else:
            break
    except ValueError:
        print("Geçerli bir tam sayı girmediniz. Lütfen tekrar deneyin.")

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


allGroups = []

for i in range(0, num_of_groups_with_off_day +num_of_groups_without_off_day):
    allGroups.append({
        "id": i + 1,
        "hasOffDay": i< num_of_groups_with_off_day,
    })
    
allGroupsLength = len(allGroups)

taskList = []

if allGroupsLength > 25 :
    taskList = allTasks[0:allGroupsLength]
elif  allGroupsLength > 20 : 
    taskList = allTasks[0:allGroupsLength]
elif  allGroupsLength > 15 : 
    taskList = allTasks[0:allGroupsLength]
else: 
    taskList = allTasks[0:allGroupsLength]







# Now we know task lists, programs and their numbers, off days of programs, easy tasks. 
# Dfine the objective function by using n, weights, and the main task list. 





# Define constraints.





# Construct Simulated Annealing and solve the problem.




# Convert your solution vector to a daily-task assignment of groups. 




# Print the task assignment as a table. Save the table.

