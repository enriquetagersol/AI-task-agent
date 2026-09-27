TOOLS = [
    {
        "functionDeclarations": [
            {
                "name": "get_tasks",
                "description": "Get all tasks from the task list",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "add_tasks",
                "description": "Add a new task to the task list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task to add"
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "complete_task",
                "description": "Mark an existing task as completed using its task ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to mark as completed"
                        }
                    },
                    "required": ["task_id"]
                }
            },
            {
    			"name": "delete_task",
    			"description": "Delete an existing task using its task ID",
    			"parameters": {
        			"type": "object",
        			"properties": {
            			"task_id": {
                			"type": "integer",
                			"description": "The ID of the task to delete"
            			}
        			},
        		"required": ["task_id"]
    			}
			}
        ]
    }
]