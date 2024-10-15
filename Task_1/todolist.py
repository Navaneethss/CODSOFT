import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QInputDialog, QListWidgetItem

tasks_file = 'tasks.json'

def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dump(tasks, file)

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do List')
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        title_label = QLabel('To-Do List')
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: #3C3C3C; padding: 10px;")
        layout.addWidget(title_label)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: #444444; color: white; font-size: 16px;")
        layout.addWidget(self.task_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Task')
        add_button.setStyleSheet("background-color: #555555; color: white;")
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        view_all_button = QPushButton('View All Tasks')
        view_all_button.setStyleSheet("background-color: #555555; color: white;")
        view_all_button.clicked.connect(self.view_all_tasks)
        button_layout.addWidget(view_all_button)

        complete_button = QPushButton('Complete Task')
        complete_button.setStyleSheet("background-color: #555555; color: white;")
        complete_button.clicked.connect(self.complete_task)
        button_layout.addWidget(complete_button)

        view_pending_button = QPushButton('View Pending Tasks')
        view_pending_button.setStyleSheet("background-color: #555555; color: white;")
        view_pending_button.clicked.connect(self.view_pending_tasks)
        button_layout.addWidget(view_pending_button)

        view_completed_button = QPushButton('View Completed Tasks')
        view_completed_button.setStyleSheet("background-color: #555555; color: white;")
        view_completed_button.clicked.connect(self.view_completed_tasks)
        button_layout.addWidget(view_completed_button)

        delete_button = QPushButton('Delete Task')
        delete_button.setStyleSheet("background-color: #FF4500; color: white;")
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.update_task_list()

    def update_task_list(self, filtered_tasks=None):
        self.task_list.clear()
        tasks = filtered_tasks if filtered_tasks is not None else load_tasks()

        for task in tasks:
            status = "✓" if task['completed'] else "✗"
            item = QListWidgetItem(f"{status} {task['description']}")
            self.task_list.addItem(item)

    def add_task(self):
        description, ok = QInputDialog.getText(self, 'Add Task', 'Enter the task:')
        if ok and description:
            tasks = load_tasks()
            task = {"description": description, "completed": False}
            tasks.append(task)
            save_tasks(tasks)
            self.update_task_list()
            QMessageBox.information(self, 'Success', 'Task added')
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a task.')

    def view_pending_tasks(self):
        tasks = load_tasks()
        pending_tasks = [task for task in tasks if not task['completed']]
        self.update_task_list(pending_tasks)

    def view_completed_tasks(self):
        tasks = load_tasks()
        completed_tasks = [task for task in tasks if task['completed']]
        self.update_task_list(completed_tasks)

    def view_all_tasks(self):
        self.update_task_list()

    def complete_task(self):
        tasks = load_tasks()
        selected_items = self.task_list.selectedItems()

        if selected_items:
            for item in selected_items:
                description = item.text()[2:] 
                for task in tasks:
                    if task['description'] == description:
                        task['completed'] = True
            save_tasks(tasks)
            self.update_task_list()
            QMessageBox.information(self, 'Success', 'Selected tasks marked as completed')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select at least one task to complete.')

    def delete_task(self):
        tasks = load_tasks()
        selected_items = self.task_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select at least one task to delete.')
            return

        confirm = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete the selected tasks?', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            for item in selected_items:
                description = item.text()[2:]  
                for task in tasks:
                    if task['description'] == description:
                        tasks.remove(task)
            save_tasks(tasks)
            self.update_task_list()
            QMessageBox.information(self, 'Success', 'Deleted task(s)')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    todo_app.show()
    sys.exit(app.exec_())
