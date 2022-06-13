from ast import expr_context
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import setup_db, Todo


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        return response

    @app.route("/todos")
    def get_todos():
        todos = Todo.query.all()
        formatted_todos = [todo.format() for todo in todos]

        if len(todos) == 0:
            abort(404)

        return jsonify(
            {"success": True, "todos": formatted_todos, "total_todos": len(todos)}
        )

    @app.route("/todos/<int:todo_id>")
    def get_todo(todo_id):
        try:
            todo = Todo.query.filter(Todo.id == todo_id).one_or_none()
            return jsonify(todo.format())
        except:
            abort(404)

    @app.route("/todos", methods=["POST"])
    def create_todo():
        body = request.get_json()
        title = body.get("title", None)
        description = body.get("description", None)
        completed = body.get("completed", False)
        search = body.get("search", None)

        try:
            if search:
                todos = Todo.query.order_by(Todo.id).filter(
                    Todo.title.ilike("%{}%".format(search))
                )

                return jsonify(
                    {
                        "success": True,
                        "todos": todos,
                        "total_todos": len(todos.all()),
                    }
                )

            else:
                todo = Todo(title=title, description=description, completed=completed)
                todo.insert()

                return jsonify(
                    {
                        "success": True,
                        "created": todo.id,
                        "total_todos": len(Todo.query.all()),
                    }
                )
        except:
            abort(422)

    @app.route("/todos/<int:todo_id>", methods=["PUT"])
    def update_todo(todo_id):
        body = request.get_json()
        title = body.get("title")
        description = body.get("description")
        completed = body.get("completed")

        try:
            todo = Todo.query.filter(Todo.id == todo_id).one_or_none()
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.update()

            return jsonify({"success": True, "todo": todo.format()})
        except:
            abort(400)

    @app.route("/todos/<int:todo_id>", methods=["DELETE"])
    def delete_todo(todo_id):
        try:
            todo = Todo.query.filter(Todo.id == todo_id).one_or_none()

            if todo is None:
                abort(404)

            todo.delete()
            return jsonify({"success": True})
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app
