def view_task_status(tracker):
    status = input("Введите статус задач для просмотра (OPEN, IN_PROGRESS, COMPLETED, OVERDUE): ")
    tracker.display_tasks_by_status(status)
#файл содержит функцию для отображения задач по статусу