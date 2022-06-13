import json
import unittest

from flaskr import create_app
from models import setup_db, Todo


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testdb"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "tobabes55", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_todo = {
            "title": "New Todo",
            "description": "A new todo",
            "completed": False,
        }

    def tearDown(self):
        pass

    def test_get_todos(self):
        res = self.client().get("/todos")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_todos"])
        self.assertTrue(len(data["todos"]))

    def test_get_todo(self):
        res = self.client().get("/todos/4")
        todo = Todo.query.filter(Todo.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(todo.format()["description"], "fourth description")

    def test_404_sent_requesting_invalid_todo(self):
        res = self.client().get("/todos/1000")

        self.assertEqual(res.status_code, 404)

    def test_update_todo(self):
        res = self.client().put(
            "/todos/2",
            json={
                "title": "2nd Todo",
                "description": "2nd description",
                "completed": True,
            },
        )
        data = json.loads(res.data)
        todo = Todo.query.filter(Todo.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(todo.format()["description"], "2nd description")

    def test_400_for_failed_update(self):
        res = self.client().put("/todos/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_todo(self):
        res = self.client().delete("/todos/3")
        data = json.loads(res.data)

        todo = Todo.query.filter(Todo.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(todo, None)

    def test_422_if_book_todo_not_exist(self):
        res = self.client().delete("/todos/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_todo(self):
        res = self.client().post("/todos", json=self.new_todo)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_405_if_todo_creation_not_allowed(self):
        res = self.client().post("/todos/4", json=self.new_todo)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_todos_search_with_results(self):
        res = self.client().post("/todos", json={"search": "1st todo"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_todos"])
        self.assertEqual(len(data["todos"]), 5)

    def test_get_todos_search_without_results(self):
        res = self.client().post("/todos", json={"search": "wontwork"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_todos"], 0)
        self.assertEqual(len(data["todos"]), 0)


if __name__ == "__main__":
    unittest.main()
