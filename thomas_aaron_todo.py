import argparse
import json
import os
class TodoItem:
    # Represents a single TODO item
    def __init__(self, item_id, category, description, status="incomplete"):
        self.item_id = item_id
        self.category = category
        self.description = description
        self.status = status
    # Turn the TODO item into a dictionary for saving
    def to_dict(self):
        return {"id": self.item_id,
            "category": self.category,
            "description": self.description,
            "status": self.status,}
    # Create a TODO item from a dictionary
    @staticmethod
    def from_dict(data):
        return TodoItem(data["id"], data["category"], data["description"], data["status"])
class TodoListManager:
    # Handles TODO items and file operations
    def __init__(self, filename="TODO.json"):
        self.filename = filename
        self.todos = []
        self.load_todos()
    # Load TODO items from a file
    def load_todos(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.todos = [TodoItem.from_dict(item) for item in data]
            else:
                self.todos = []
        except json.JSONDecodeError:
            print(f"Error: Could not read {self.filename}. File might be corrupted.")
        except Exception as e:
            print(f"Error loading the file: {e}")
    # Save TODO items to a file
    def save_todos(self):
        try:
            with open(self.filename, "w") as file:
                json.dump([todo.to_dict() for todo in self.todos], file, indent=4)
        except PermissionError:
            print(f"Error: No permission to write to {self.filename}.")
        except Exception as e:
            print(f"Error saving the file: {e}")
    # Show all TODO items
    def display_todos(self):
        if not self.todos:
            print("Your TODO list is empty!")
        else:
            for todo in self.todos:
                print(f"ID: {todo.item_id}, Category: {todo.category}, Description: {todo.description}, Status: {todo.status}")
    # Add a new TODO item
    def add_todo(self, category, description):
        if not category or not description:
            print("Error: You need both a category and description to add an item.")
            return
        new_id = len(self.todos) + 1
        new_todo = TodoItem(new_id, category, description)
        self.todos.append(new_todo)
        self.save_todos()
        print(f"Added TODO item with ID {new_id}.")
    # Update an existing TODO item by ID
    def update_todo(self, item_id, category=None, description=None, status=None):
        if status and status not in ["incomplete", "in progress", "complete"]:
            print("Error: Status must be 'incomplete', 'in progress', or 'complete'.")
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
    # Delete a TODO item by ID
    def delete_todo(self, item_id):
        for i, todo in enumerate(self.todos):
            if todo.item_id == item_id:
                del self.todos[i]
                # Reassign IDs to keep them in order after deleting
                for index, todo in enumerate(self.todos, start=1):
                    todo.item_id = index
                self.save_todos()
                print(f"Deleted TODO item with ID {item_id}.")
                return
        print(f"Error: TODO item with ID {item_id} not found.")
    # Switch to a different TODO list file
    def change_list(self, new_filename):
        if not new_filename:
            print("Error: You need to provide a filename to switch to a new list.")
            return
        self.filename = new_filename
        self.load_todos()
        print(f"Switched to TODO list file: {self.filename}")
def main():
    # Handle user input and commands
    parser = argparse.ArgumentParser(description="TODO List CLI Tool")
    parser.add_argument("--list-name", help="Use a custom TODO list file", default="TODO.json")
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Display subcommand
    subparsers.add_parser("display", help="Show all TODO items")
    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new TODO item")
    add_parser.add_argument("category", help="The category of the TODO item")
    add_parser.add_argument("description", help="The description of the TODO item")
    # Update subcommand
    update_parser = subparsers.add_parser("update", help="Update an existing TODO item")
    update_parser.add_argument("id", type=int, help="The ID of the TODO item to update")
    update_parser.add_argument("--category", help="The new category for the TODO item")
    update_parser.add_argument("--description", help="The new description for the TODO item")
    update_parser.add_argument("--status", help="The new status for the TODO item", choices=["incomplete", "in progress", "complete"])
    # Delete subcommand
    delete_parser = subparsers.add_parser("delete", help="Delete a TODO item")
    delete_parser.add_argument("id", type=int, help="The ID of the TODO item to delete")
    args = parser.parse_args()
    # Initialize the TODO list manager
    todo_manager = TodoListManager(args.list_name)
    if args.command == "display":
        todo_manager.display_todos()
    elif args.command == "add":
        todo_manager.add_todo(args.category, args.description)
    elif args.command == "update":
        todo_manager.update_todo(args.id, category=args.category, description=args.description, status=args.status)
    elif args.command == "delete":
        todo_manager.delete_todo(args.id)
if __name__ == "__main__":
    main()
