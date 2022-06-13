# Todo App

This project is a todo app. Users can create new todo items, change their completed status, update todo details (title and description), search for todo items and delete todo items.

## Getting started

### Pre-requisites and Local Development

Developers using this project should already have python3, pip and node installed on their local machines.

#### Backend

From the backend folder, run `pip install -r requirements.txt` to install all required packages.

To run the application, run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask Documentation](https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/).

## API Reference

### Getting started

- Base URL: The base URL for this API is http://127.0.0.1:5000/
- Authentication: This API does not require authentication or API keys

### Error Handling

The API may return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

### Endpoint Library

#### GET /todos

- General:
  - Returns a list of todo items as objects, a success value and the total number of todos.
- Sample: `curl http://127.0.0.1:5000/todos`

```
{
  "success": true,
  "todos": [
    {
      "completed": false,
      "description": "This is my first todo item",
      "id": 1,
      "title": "1st Todo"
    },
    {
      "completed": true,
      "description": "2nd description updated",
      "id": 2,
      "title": "2nd Todo"
    }
  ],
  "total_todos": 2
}
```

#### POST /todos

- General:
  - Creates a new todo using the submitted title, description and completed fields. Returns the id of the created todo, a success value and the total number of todos.
- Sample: `curl http://127.0.0.1:5000/todos -X POST -H 'Content-Type: application/json' -d '{"title": "New Todo", "description": "New Todo Item", "completed": true}'`

```
{
    "created": 3,
    "success": true,
    "total_todos": 3
}
```

#### DELETE /todos/{todo_id}

- General:
  - Deletes the todo item of the given id if it exists. Returns a success value.
- Sample: `curl -X DELETE 'http://127.0.0.1:5000/todos/2'`

```
{
    "success": True
}
```

#### PUT /todos/{todo_id}

- General:
  - Updates a todo item using the submitted title, description and completed fields. Returns a success message and the edited todo.
- Sample: `curl http://127.0.0.1:5000/todos -X PUT -H 'Content-Type: application/json' -d '{"title": "Updated Todo", "description": "Updated Todo Item", "completed": true}'`

## Deployment N/A

## Authors

Tobi Samuel
