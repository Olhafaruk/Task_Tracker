import json
from enum import Enum
from tabulate import tabulate

class TaskStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"

class Task:
    _id_counter = 1

    def __init__(self, title, description, status, due_date, assignee=None, progress=0):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.assignee = assignee
        self.progress = progress

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'due_date': self.due_date,
            'assignee': self.assignee,
            'progress': self.progress
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            status=TaskStatus[data['status'].replace(" ", "_").upper()],
            due_date=data['due_date'],
            assignee=data.get('assignee'),
            progress=data.get('progress', 0)
        )
        task.id = data['id']
        Task._id_counter = max(Task._id_counter, task.id + 1)
        return task

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['username'], data['password'], data['role'])

class TaskTracker:
    def __init__(self, config):
        self.tasks = []
        self.users = []
        self.config = config
        self.load_tasks()
        self.load_users()
        self.current_user = None

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != int(task_id)]

    def change_task_status(self, task_id, new_status):
        for task in self.tasks:
            if task.id == int(task_id):
                if self.current_user.role == 'admin' or self.current_user.username == task.assignee:
                    task.status = TaskStatus[new_status.replace(" ", "_").upper()]
                    return True
                else:
                    print("У вас нет прав для изменения статуса этой задачи.")
                    return False

    def update_task_progress(self, task_id, progress):
        for task in self.tasks:
            if task.id == int(task_id):
                if self.current_user.role == 'admin' or self.current_user.username == task.assignee:
                    task.progress = progress
                    return True
                else:
                    print("У вас нет прав для изменения прогресса этой задачи.")
                    return False

    def display_tasks(self, show_completed=False):
        for task in self.tasks:
            if self.current_user.role == 'admin' or task.assignee == self.current_user.username:
                if show_completed:
                    if task.status == TaskStatus.COMPLETED:
                        print(f"{task.id}: {task.title} - {task.status.value} - {task.assignee} - {task.progress}%")
                else:
                    if task.status != TaskStatus.COMPLETED:
                        print(f"{task.id}: {task.title} - {task.status.value} - {task.assignee} - {task.progress}%")

    def display_tasks_by_status(self, status):
        for task in self.tasks:
            if self.current_user.role == 'admin' or task.assignee == self.current_user.username:
                if task.status == TaskStatus[status.replace(" ", "_").upper()]:
                    print(f"{task.id}: {task.title} - {task.status.value} - {task.assignee} - {task.progress}%")

    def display_tasks_by_assignee(self, assignee):
        for task in self.tasks:
            if self.current_user.role == 'admin' or task.assignee == self.current_user.username:
                if task.assignee == assignee:
                    print(f"{task.id}: {task.title} - {task.status.value} - {task.assignee} - {task.progress}%")

    def display_task_deadlines(self):
        for task in self.tasks:
            if self.current_user.role == 'admin' or task.assignee == self.current_user.username:
                print(f"{task.id}: {task.title} - {task.due_date} - {task.assignee} - {task.progress}%")

    def toggle_show_completed(self):
        self.config['show_completed'] = not self.config.get('show_completed', False)
        self.save_config()
        self.display_tasks(show_completed=self.config['show_completed'])

    def save_tasks(self):
        with open(self.config['tasks_file'], 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_tasks(self):
        try:
            with open(self.config['tasks_file'], 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task.from_dict(data) for data in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл со списком задач не найден или поврежден. Создание нового списка задач.")
            self.tasks = []

    def save_users(self):
        with open('users.json', 'w') as file:
            json.dump([user.to_dict() for user in self.users], file, indent=4)

    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
                self.users = [User.from_dict(data) for data in users_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл с пользователями не найден или поврежден. Создание нового списка пользователей.")
            self.users = []

    def save_config(self):
        with open('config.json', 'w') as file:
            json.dump(self.config, file, indent=4)

    def notify_user(self):
        print("Уведомления о задачах:")
        for task in self.tasks:
            if self.current_user.role == 'admin':
                if task.status in [TaskStatus.OPEN, TaskStatus.OVERDUE]:
                    print(f"{task.id}: {task.title} - {task.status.value} - {task.due_date} - {task.assignee} - {task.progress}%")
            elif self.current_user.username == task.assignee:
                if task.status in [TaskStatus.OPEN, TaskStatus.OVERDUE]:
                    print(f"{task.id}: {task.title} - {task.status.value} - {task.due_date} - {task.assignee} - {task.progress}%")

    def generate_report(self):
        headers = ["ID", "Title", "Description", "Status", "Due Date", "Assignee", "Progress"]
        rows = [[task.id, task.title, task.description, task.status.value, task.due_date, task.assignee, f"{task.progress}%"] for task in self.tasks]
        report = tabulate(rows, headers, tablefmt="grid")
        print("Отчет по задачам:")
        print(report)
        with open("task_report.txt", "w") as file:
            file.write(report)

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Добро пожаловать, {username}!")
                self.notify_user()  # Добавляем вызов метода notify_user при входе в систему
                return True
        print("Неверное имя пользователя или пароль.")
        return False

    def register_user(self, username, password, role):
        new_user = User(username, password, role)
        self.users.append(new_user)
        self.save_users()
        print(f"Пользователь {username} зарегистрирован.")
