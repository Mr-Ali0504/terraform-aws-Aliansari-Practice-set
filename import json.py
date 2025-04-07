import json
import random
import time

# Sample tasks data
tasks = [
    {"id": 1, "title": "Fix server issue", "status": "Pending"},
    {"id": 2, "title": "Deploy new release", "status": "In Progress"},
    {"id": 3, "title": "Code review for PR #42", "status": "Completed"},
    {"id": 4, "title": "Update documentation", "status": "Pending"},
    {"id": 5, "title": "Optimize database queries", "status": "Pending"},
]

def display_tasks():
    """Displays all tasks in a formatted table."""
    print("\n📌 Current Task List:")
    print("-" * 50)
    print(f"{'ID':<5}{'Title':<30}{'Status':<15}")
    print("-" * 50)
    for task in tasks:
        print(f"{task['id']:<5}{task['title']:<30}{task['status']:<15}")
    print("-" * 50)

def add_task():
    """Adds a new task to the task list."""
    title = input("Enter task title: ")
    new_id = max(task["id"] for task in tasks) + 1
    tasks.append({"id": new_id, "title": title, "status": "Pending"})
    print(f"✅ Task '{title}' added successfully!")

def update_task():
    """Updates the status of a task."""
    task_id = int(input("Enter Task ID to update: "))
    for task in tasks:
        if task["id"] == task_id:
            new_status = input("Enter new status (Pending/In Progress/Completed): ")
            task["status"] = new_status
            print(f"🔄 Task '{task['title']}' updated to '{new_status}'")
            return
    print("❌ Task not found!")

def delete_task():
    """Deletes a task from the task list."""
    task_id = int(input("Enter Task ID to delete: "))
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    print(f"🗑️ Task {task_id} deleted successfully!")

def save_tasks():
    """Saves the task list to a file."""
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    print("📁 Tasks saved successfully!")

def load_tasks():
    """Loads the task list from a file."""
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
        print("📂 Tasks loaded successfully!")
    except FileNotFoundError:
        print("⚠️ No saved tasks found!")

def simulate_work():
    """Simulates work for a few seconds to look busy 😂"""
    print("⌛ Processing tasks...")
    for _ in range(9):
        time.sleep(9)
        print("... still working ...")
    print("✅ Task processing complete!")

# Main menu loop
while True:
    print("\n🎯 Task Manager")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Save Tasks")
    print("6. Load Tasks")
    print("7. Simulate Work")
    print("8. Exit")

    choice = input("Enter your choice: ")
    
    if choice == "1":
        display_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        update_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        save_tasks()
    elif choice == "6":
        load_tasks()
    elif choice == "7":
        simulate_work()
    elif choice == "8":
        print("👋 Exiting Task Manager. Have a great day!")
        break
    else:
        print("❌ Invalid choice! Please select a valid option.")
