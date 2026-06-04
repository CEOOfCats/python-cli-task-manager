import json
from datetime import datetime
import time

task_list = []

def load_tasks():
    try:
        with open("TO_DO.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

task_list = load_tasks()

def save_tasks():
    with open("TO_DO.json", "w") as f:
        json.dump(task_list, f, indent= 4)

def add_task(task, date):
    task_list.append({"Task" : task, "Status" : False, 'Due Date' : date})
    sort_tasks()

def view_tasks(opt):
    count = 0
    comp = 0
    for idx, task in enumerate(task_list, start= 1):
        due = datetime.strptime(task["Due Date"], "%d-%m-%Y")
        if opt == 1:
            state = 'X' if task["Status"] else " "
            print(f"{idx}. [{state}] {task['Task']}\nDue: {task['Due Date']}")
        elif opt == 2:
            if task["Status"]:
                print(f"{idx}. [X] {task['Task']}\nDue: {task['Due Date']}")
        elif opt == 3:
            if not task["Status"]:
                print(f"{idx}. [ ] {task['Task']}\nDue: {task['Due Date']}")
        else:
            if due < datetime.now() and not task["Status"]:
                print(f"{idx}. [ ] {task['Task']}\nDue: {task['Due Date']}")

        count += 1
        if task["Status"]:
            comp += 1
        if due < datetime.now() and not task["Status"] and opt != 4:
            print("^^^OVERDUE^^^")

    if count == 0:
        print("No tasks found.")
    else:
        print(f"\nTotal tasks completed: {comp}")
        print(f"Productivity status: {(comp/count)*100:.1f}%")

def delete_task(task_no):
    task_list.pop(task_no)
    save_tasks()

def toggle_task(i):
    
    task_list[i]["Status"] = not task_list[i]["Status"]

    save_tasks()

def search_by_task(keyword):
    found = False
    for task in task_list:
        if keyword.lower() in task["Task"].lower():
            due = datetime.strptime(task["Due Date"], "%d-%m-%Y")
            state = 'X' if task["Status"] else " "
            print(f"[{state}] {task['Task']}\nDue: {task['Due Date']}\n")

            if due < datetime.now() and not task["Status"]:
                print("^^^OVERDUE^^^")

            found = True
    if not found:
        print("Nope, never seen this\n")

def search_by_Date(Date):
    found = False
    for task in task_list:
        if Date == task["Due Date"]:
            due = datetime.strptime(task["Due Date"], "%d-%m-%Y")
            state = 'X' if task["Status"] else " "
            print(f"[{state}] {task['Task']}\nDue: {task['Due Date']}\n")

            if due < datetime.now() and not task["Status"]:
                print("^^^OVERDUE^^^")

            found = True
    if not found:
        print("Nope, nothing due on this date\n")

def sort_tasks():
    task_list.sort(key=lambda task: datetime.strptime(task["Due Date"], "%d-%m-%Y"))
    save_tasks()

def get_valid_date():
    while(True):
        date = input("Enter due date (dd-mm-yyyy): ")

        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date
        except ValueError:
            print("Enter a valid date!")

def get_valid_index(prompt):
    while True:
        try:
            idx = int(input(prompt))
            if 1 <= idx <= len(task_list):
                return (idx - 1)

            print("Invalid index")

        except ValueError:
            print("Enter a number")

def main():
    while(True):
        choice = input("\nWhat would u like to do? (Enter the number 1-7)\n1. Add a task\n2. View tasks\n3. Delete task\n4. Toggle task status\n5. Check a task\n6. Edit task\n7. Exit\n\n")
        if choice == '7':
            print("\nExiting program...\n")
            break

        elif choice == '1':
            task = input("\nEnter task: ")
            date = get_valid_date()
            add_task(task, date)
            print("\nTask added successfully!!")
            time.sleep(0.5)

        elif choice == '2':
            while(True):
                opt = input("\nChoose filter method: (Choose no. 1-3)\n1. Show all\n2. Show completed\n3. Show pending\n4. Show overdue tasks\n\n")
                try:
                    opt = int(opt)
                except ValueError:
                    print("\nEnter a valid choice (Number from 1-4)\n")
                    continue
                if opt > 4 or opt < 1:
                    print("\nEnter a valid choice (Number from 1-4)\n")
                    continue
                else:
                    break
            print("\nLoading up tasks...\n")
            time.sleep(0.5)
            view_tasks(opt)

        elif choice == '3':
            print("\nLoading up tasks...\n")
            view_tasks(1)
            idx = get_valid_index("\nWhich task do u wish to delete?(Enter index number): ")
            delete_task(idx)

        elif choice == '4':
            view_tasks(1)
            idx = get_valid_index("\nWhich task do u wish to toggle?(Enter index number): ")
            toggle_task(idx)

        elif choice == '5':
            while(True):
                opt = input("Do you wish to check by due date or task name?: (Enter 1 or 2)\n1. Task name\n2. Due date\n")
                try:
                    opt = int(opt)
                except ValueError:
                    print("\nEnter a valid option!\n")
                    continue
                if opt > 2 or opt < 1:
                    print("\nEnter a valid option!\n")
                    continue
                else:
                    break
            if opt == 1:
                keyword = input("Which task do u wish to check for?: ")
                search_by_task(keyword)
            else:
                date = get_valid_date()
                search_by_Date(date)

        elif choice == '6':
            view_tasks(1)
            idx = get_valid_index("\nWhich task do u wish to edit?(Enter index number): ")

            task = input("\nEnter new task: ")
            date = get_valid_date()

            task_list[idx]["Task"] = task
            task_list[idx]["Due Date"] = date
            sort_tasks()

        else:
            print("\nInvalid input. Please enter a number from 1-7\n")


main()
