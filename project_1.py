
#Функция для добавления новой задачи.
# Запрашивает у пользователя название задачи, описание,
# срок выполнения и исполнителя, затем создает задачу и добавляет ее в трекер.
import TaskTracker

def add_task(tracker):
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    due_date = input("Введите срок выполнения задачи (YYYY-MM-DD): ")
    assignee = input("Введите исполнителя задачи: ")
    task = TaskTracker.Task(title, description, TaskTracker.TaskStatus.OPEN, due_date, assignee)
    tracker.add_task(task)
    print("Задача добавлена.")

def view_tasks_by_assignee(tracker):
    assignee = input("Введите имя исполнителя для просмотра задач: ")
    tracker.display_tasks_by_assignee(assignee)

#Функция для просмотра задач по исполнителю.
# Запрашивает у пользователя имя исполнителя и отображает все задачи,
# назначенные этому исполнителю.

