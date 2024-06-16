import tkinter as tk

CurrentWindow = None

def destroy_prev_window():
    return

def show_main_window():
    return

def show_all():
    return

def import_data():
    global CurrentWindow
    
    # Закрываем предыдущее окно
    destroy_prev_window()

    # Создаем вспомогательное окно для ввода данных о новом контакте
    global SurnameEntry, NameEntry, PhoneNumberEntry, CommentEntry

    ImportDataWindow = tk.Tk()    
    ImportDataWindow.title("Введите данные о новом контакте")
    ImportDataWindow.geometry("400x300")
    CurrentWindow = ImportDataWindow

    # Создаем поле ввода фамилии
    SurnameFrame = tk.Frame(ImportDataWindow)
    SurnameFrame.pack(pady=10, padx=20)

    SurnameLabel = tk.Label(SurnameFrame, text='Введите фамилию: ')
    SurnameLabel.pack(side='left')

    SurnameEntry = tk.Entry(SurnameFrame, width=30)
    SurnameEntry.pack(side="left")

    # Создаем поле ввода имени
    NameFrame = tk.Frame(ImportDataWindow)
    NameFrame.pack(pady=10, padx=20)

    NameLabel = tk.Label(NameFrame, text='Введите имя: ')
    NameLabel.pack(side='left')

    NameEntry = tk.Entry(NameFrame, width=30)
    NameEntry.pack(side="left")

    # Создаем поле ввода номера телефона
    PhoneNumberFrame = tk.Frame(ImportDataWindow)
    PhoneNumberFrame.pack(pady=10, padx=20)

    PhoneNumberLabel = tk.Label(PhoneNumberFrame, text='Введите номер телефона: ')
    PhoneNumberLabel.pack(side='left')

    PhoneNumberEntry = tk.Entry(PhoneNumberFrame, width=30)
    PhoneNumberEntry.pack(side="left")

    # Создаем поле ввода комментария
    CommentFrame = tk.Frame(ImportDataWindow)
    CommentFrame.pack(pady=10, padx=20)

    CommentLabel = tk.Label(CommentFrame, text='Введите комментарий: ')
    CommentLabel.pack(side='left')

    CommentEntry = tk.Entry(CommentFrame, width=30)
    CommentEntry.pack(side="left")

    # Создаем кнопку для сохранения данных
    SaveDataButton = tk.Button(ImportDataWindow, text='Сохранить данные', command=save_data)
    SaveDataButton.pack(pady=10)

    # Создаем кнопку возврата в главное меню
    BackToMainButton = tk.Button(ImportDataWindow, text='Назад', command=show_main_window)
    BackToMainButton.pack(pady=10)

    # Запуск цикла обработки событий
    ImportDataWindow.mainloop()

def export_data():
    return

def save_data():
    return