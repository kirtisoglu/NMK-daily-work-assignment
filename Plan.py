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


data = pd.read_excel(excel_file, sheet_name=sheet_name)
allTasks = data.values


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

# Merge the programs in an order and calculate n.

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




# Define constraints.




# Construct Simulated Annealing and solve the problem.




# Convert your solution vector to a daily-task assignment of groups. 




# Print the task assignment as a table. Save the table.

