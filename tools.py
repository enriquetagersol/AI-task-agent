import json

TASKS_FILE = "tasks.json"

def get_tasks():
	"""Return all tasks stored in the task list"""
	try:
		with open(TASKS_FILE,"r") as file:
			return json.load(file)
	except FileNotFoundError:
		return []

def add_tasks(title):
	"""Add new tasks to the list"""
	tasks = get_tasks()

	new_task = {
		"id": len(tasks) + 1,
		"title": title,
		"completed": False
	}
	tasks.append(new_task)
	
	with open(TASKS_FILE,"w") as file:
		json.dump(tasks,file,indent=4)
	return new_task

def complete_task(task_id):
    """Mark a task as completed"""
    tasks = get_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True

            with open(TASKS_FILE, "w") as file:
                json.dump(tasks, file, indent=4)

            return task

    return {"error": "Task not found"}
    
def delete_task(task_id):
    """Delete a task from the task list"""
    tasks = get_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            with open(TASKS_FILE, "w") as file:
                json.dump(tasks, file, indent=4)

            return task

    return None


	