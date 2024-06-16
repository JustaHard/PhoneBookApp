import tkinter as tk

CurrentWindow = None

def destroy_prev_window():
    return

def show_main_window():
    global CurrentWindow

    # Закрываем предыдущее окно
    destroy_prev_window()

    # Создаем главное окно приложения
    root = tk.Tk()
    root.title("Управление телефонным справочником")
    root.geometry("400x300")
    CurrentWindow = root

    # Создаем кнопку для отображения всего справочника
    ShowAllButton = tk.Button(root, text='Отобразить весь справочник', command=show_all)
    ShowAllButton.pack(pady=10)

    # Создаем кнопку для экспорта данных из справочника
    ExportDataButton = tk.Button(root, text='Получить данные о существующем контакте', command=export_data)
    ExportDataButton.pack(pady=10)

    # Создаем кнопку для импорта данных в справочник
    ImportDataButton = tk.Button(root, text='Добавить новый контакт', command=import_data)
    ImportDataButton.pack(pady=10)

    # Создаем кнопку завершения работы
    CloseAppButton = tk.Button(root, text='Завершить работу', command=root.destroy)
    CloseAppButton.pack(pady=10)

    # Запуск главного цикла обработки событий
    root.mainloop()

def show_all():
    return

def import_data():
    return

def export_data():
    return