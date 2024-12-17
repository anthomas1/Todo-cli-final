import argparse
import json
import os
class TodoItem:
    def __init__(self, item_id, category, description, status="incomplete"):
        self.item_id = item_id
        self.category = category
        self.description = description
        self.status = status
    def to_dict(self):
        return {
            "id": self.item_id,
            "category": self.category,
            "description": self.description,
            "status": self.status}
    @staticmethod
    def from_dict(data):
        return TodoItem(data["id"], data["category"], data["description"], data["status"])
class TodoListManager:
    def __init__(self, filename="TODO.json"):
        self.filename = filename
        self.todos = []
        self.load_todos()
    def load_todos(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.todos = [TodoItem.from_dict(item) for item in data]
            else:
                self.todos = []
        except json.JSONDecodeError:
            print(f"Error: Failed to decode the file {self.filename}. The file could be corrupted.")
        except Exception as e:
            print(f"Something wrong happened while loading the file: {e}")
    def save_todos(self):
        try:
            with open(self.filename, "w") as file:
                json.dump([todo.to_dict() for todo in self.todos], file, indent=4)
        except PermissionError:
            print(f"Error: Permission denied when trying to write to {self.filename}.")
        except Exception as e:
            print(f"Something wrong happened while saving the file: {e}")
    def display_todos(self):
        if not self.todos:
            print("Your TODO list is empty!")
        else:
            for todo in self.todos:
                print(f"ID: {todo.item_id}, Category: {todo.category}, Description: {todo.description}, Status: {todo.status}")
    def add_todo(self, category, description):
        if not category or not description:
            print("Error: You need a category and description to add a new TODO item.")
            return
        new_id = len(self.todos) + 1
        new_todo = TodoItem(new_id, category, description)
        self.todos.append(new_todo)
        self.save_todos()
        print(f"Added TODO item with ID {new_id}.")
    def update_todo(self, item_id, category=None, description=None, status=None):
        if status and status not in ["incomplete", "in progress", "complete"]:
            print("Error: Wrong status. You have to choose from 'incomplete', 'in progress', or 'complete'.")
            return
        for todo in self.todos:
            if todo.item_id == item_id:
                if category:
                    todo.category = category
                if description:
                    todo.description = description
                if status:
                    todo.status = status
                self.save_todos()
                print(f"Updated TODO item with ID {item_id}.")
                return
        print(f"Error: TODO item with ID {item_id} not found.")
    def change_list(self, new_filename):
        if not new_filename:
            print("Error: Give a filename to switch the TODO list.")
            return
        self.filename = new_filename
        self.load_todos()
        print(f"Switched to TODO list file: {self.filename}")
def main():
    parser = argparse.ArgumentParser(description="TODO List CLI Tool")
    parser.add_argument("--list-name", help="Specify a custom TODO list file", default="TODO.json")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("display", help="Display all TODO items")
    add_parser = subparsers.add_parser("add", help="Add a new TODO item")
    add_parser.add_argument("category", help="Category of the TODO item")
    add_parser.add_argument("description", help="Description of the TODO item")
    update_parser = subparsers.add_parser("update", help="Update an existing TODO item")
    update_parser.add_argument("id", type=int, help="ID of the TODO item to update")
    update_parser.add_argument("--category", help="New category for the TODO item")
    update_parser.add_argument("--description", help="New description for the TODO item")
    update_parser.add_argument("--status", help="New status for the TODO item", choices=["incomplete", "in progress", "complete"])
    args = parser.parse_args()
    todo_manager = TodoListManager(args.list_name)
    if args.command == "display":
        todo_manager.display_todos()
    elif args.command == "add":
        todo_manager.add_todo(args.category, args.description)
    elif args.command == "update":
        todo_manager.update_todo(args.id, category=args.category, description=args.description, status=args.status)
if __name__ == "__main__":
    main()
