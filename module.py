import tkinter as tk

CurrentWindow = None

def destroy_prev_window():
    global CurrentWindow
    if CurrentWindow is not None:
        CurrentWindow.destroy()

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
    global CurrentWindow, SurnameEntry, NameEntry, PhoneNumberEntry, CommentEntry
    
    # Закрываем предыдущее окно
    destroy_prev_window()

    # Создаем вспомогательное окно для ввода данных о новом контакте
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
    PhoneBook = []
    DataToSave = [SurnameEntry.get(), NameEntry.get(), PhoneNumberEntry.get(), CommentEntry.get()]
    filepath = 'Saved_Data/Phone_book.txt'

    # Получаем список уже существующих контактов, если такие есть
    try:
        with open (filepath, 'r') as phb:
            for line in phb:
                PhoneBook.append(line.split(','))
    except:
        pass

    # Решаем проблему с кучей пустых строк
    for i in range(len(PhoneBook)):
        if '\n' in PhoneBook[i][-1]:
            PhoneBook[i][-1] = PhoneBook[i][-1][:-2]

    # Заносим новый контакт в список, если до этого его там не было
    if DataToSave not in PhoneBook:
        PhoneBook.append(DataToSave)

    # Обновляем список контактов
    with open (filepath, 'w') as phout:
        for line in PhoneBook:
            s = ''
            for data in line:
                s = s + data + ','
            phout.write(f'{s[:-1]}\n')