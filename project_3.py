def change_task_status(tracker):
    task_id = input("Введите ID задачи для изменения статуса: ")
    if not tracker.change_task_status(task_id, input("Введите новый статус задачи (OPEN, IN_PROGRESS, COMPLETED, OVERDUE): ")):
        return
    progress = input("Введите процент выполнения задачи (0-100): ")
    if not tracker.update_task_progress(task_id, int(progress)):
        return
    print("Статус задачи и прогресс выполнения изменены.")


