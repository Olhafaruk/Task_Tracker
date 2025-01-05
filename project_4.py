#файл содержит функцию для отображения всех задач
#Запрашивает у пользователя, нужно ли показывать выполненные задачи,
# и отображает все задачи в зависимости от выбора пользователя.

def view_all_tasks(tracker):
    show_completed = input("Показать выполненные задачи? (да/нет): ").lower() == 'да'
    tracker.display_tasks(show_completed)

def generate_report(tracker):
    tracker.generate_report()

def report_menu(tracker):
    while True:
        print("\nМеню отчетов:")
        print("1. Сгенерировать отчет по задачам")
        print("2. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            generate_report(tracker)
        elif choice == "2":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию от 1 до 2.")
