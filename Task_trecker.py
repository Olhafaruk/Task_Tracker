import json
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description, due_date, priority, category, status="Pending", progress=0, assigned_users=None, created_at=None, reminders=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
        self.progress = progress
        self.assigned_users = assigned_users if assigned_users else []
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reminders = reminders if reminders else []

    def __repr__(self):
        return f"Task({self.title}, {self.description}, {self.due_date}, {self.priority}, {self.category}, {self.status}, {self.progress}, {self.assigned_users}, {self.created_at}, {self.reminders})"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "progress": self.progress,
            "assigned_users": self.assigned_users,
            "created_at": self.created_at,
            "reminders": self.reminders
        }

class TaskTracker:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date, priority, category, assigned_users=None):
        task = Task(title, description, due_date, priority, category, assigned_users=assigned_users)
        self.tasks.append(task)

    def edit_task(self, index, title=None, description=None, due_date=None, priority=None, category=None, assigned_users=None):
        if 0 <= index < len(self.tasks):
            if title:
                self.tasks[index].title = title
            if description:
                self.tasks[index].description = description
            if due_date:
                self.tasks[index].due_date = due_date
            if priority:
                self.tasks[index].priority = priority
            if category:
                self.tasks[index].category = category
            if assigned_users is not None:
                self.tasks[index].assigned_users = assigned_users

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_as_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = "Done"

    def set_task_progress(self, index, progress):
        if 0 <= index < len(self.tasks):
            self.tasks[index].progress = progress

    def add_reminder(self, index, reminder_time):
        if 0 <= index < len(self.tasks):
            self.tasks[index].reminders.append(reminder_time)

    def filter_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category == category]

    def filter_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def filter_tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority == priority]

    def save_tasks(self, file_path):
        with open(file_path, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_tasks(self, file_path):
        with open(file_path, 'r') as file:
            tasks_data = json.load(file)
            self.tasks = [Task(**data) for data in tasks_data]

    def __repr__(self):
        return f"TaskTracker({self.tasks})"

def display_menu():
    print("Меню таск-трекера:")
    print("1. Добавить задачу")
    print("2. Редактировать задачу")
    print("3. Удалить задачу")
    print("4. Пометить задачу как выполненную")
    print("5. Установить прогресс задачи")
    print("6. Добавить напоминание")
    print("7. Фильтровать задачи по категории")
    print("8. Фильтровать задачи по статусу")
    print("9. Фильтровать задачи по приоритету")
    print("10. Сохранить задачи в файл")
    print("11. Загрузить задачи из файла")
    print("12. Показать все задачи")
    print("13. Выйти")

def main():
    tracker = TaskTracker()

    while True:
        display_menu()
        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            due_date = input("Введите срок выполнения задачи (YYYY-MM-DD): ")
            priority = input("Введите приоритет задачи (Высокий, Средний, Низкий): ")
            category = input("Введите категорию задачи: ")
            assigned_users = input("Введите пользователей, назначенных на задачу (через запятую): ").split(',')
            tracker.add_task(title, description, due_date, priority, category, assigned_users)
        elif choice == '2':
            index = int(input("Введите индекс задачи для редактирования: "))
            title = input("Введите новое название задачи (оставьте пустым для сохранения текущего): ")
            description = input("Введите новое описание задачи (оставьте пустым для сохранения текущего): ")
            due_date = input("Введите новый срок выполнения задачи (оставьте пустым для сохранения текущего): ")
            priority = input("Введите новый приоритет задачи (оставьте пустым для сохранения текущего): ")
            category = input("Введите новую категорию задачи (оставьте пустым для сохранения текущего): ")
            assigned_users = input("Введите новых пользователей, назначенных на задачу (оставьте пустым для сохранения текущих): ").split(',')
            tracker.edit_task(index, title or None, description or None, due_date or None, priority or None, category or None, assigned_users if assigned_users != [''] else None)
        elif choice == '3':
            index = int(input("Введите индекс задачи для удаления: "))
            tracker.delete_task(index)
        elif choice == '4':
            index = int(input("Введите индекс задачи для отметки как выполненной: "))
            tracker.mark_task_as_done(index)
        elif choice == '5':
            index = int(input("Введите индекс задачи для установки прогресса: "))
            progress = int(input("Введите процент выполнения задачи: "))
            tracker.set_task_progress(index, progress)
        elif choice == '6':
            index = int(input("Введите индекс задачи для добавления напоминания: "))
            reminder_time = input("Введите время напоминания (YYYY-MM-DD HH:MM:SS): ")
            tracker.add_reminder(index, reminder_time)
        elif choice == '7':
            category = input("Введите категорию для фильтрации задач: ")
            filtered_tasks = tracker.filter_tasks_by_category(category)
            print("Задачи в категории", category, ":", filtered_tasks)
        elif choice == '8':
            status = input("Введите статус для фильтрации задач (Pending, Done): ")
            filtered_tasks = tracker.filter_tasks_by_status(status)
            print("Задачи со статусом", status, ":", filtered_tasks)
        elif choice == '9':
            priority = input("Введите приоритет для фильтрации задач (Высокий, Средний, Низкий): ")
            filtered_tasks = tracker.filter_tasks_by_priority(priority)
            print("Задачи с приоритетом", priority, ":", filtered_tasks)
        elif choice == '10':
            file_path = input("Введите путь к файлу для сохранения задач: ")
            tracker.save_tasks(file_path)
        elif choice == '11':
            file_path = input("Введите путь к файлу для загрузки задач: ")
            tracker.load_tasks(file_path)
        elif choice == '12':
            print("Все задачи:", tracker)
        elif choice == '13':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию от 1 до 13.")

if __name__ == '__main__':
    main()

# def main():
#     tracker = TaskTracker()

    # добавления задач
    # tracker.add_task("Complete report", "Finish the quarterly report", "2024-12-20", "High", "Work", ["Olga", "David"])
    # tracker.add_task("Update the project Task_trecker", "Add archiving of completed tasks", "2024-12-18", "Medium", "IT-department")

    # редактирования задачи
    # tracker.edit_task(0, description="Finish the annual report")

    # удаления задачи
    # tracker.delete_task(1)

    # Пример отметки задачи как выполненной
    # tracker.mark_task_as_done(0)

    # Пример установки прогресса задачи
    # tracker.set_task_progress(0, 80)

    # Пример добавления напоминания
    # tracker.add_reminder(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))

    # Пример фильтрации задач по категории
    # work_tasks = tracker.filter_tasks_by_category("Work")
    # print("Work tasks:", work_tasks)

    # Пример фильтрации задач по статусу
    # done_tasks = tracker.filter_tasks_by_status("Done")
    # print("Done tasks:", done_tasks)

    # Пример фильтрации задач по приоритету
    # high_priority_tasks = tracker.filter_tasks_by_priority("High")
    # print("High priority tasks:", high_priority_tasks)

    # Сохранение задач в файл
    # tracker.save_tasks('tasks.json')

    # Загрузка задач из файла
    # tracker.load_tasks('tasks.json')

    # Вывод задач
    # print(tracker)

# if __name__ == '__main__':
#     main()
