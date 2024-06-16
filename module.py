import tkinter as tk
from tkinter import ttk

CurrentWindow = None

def destroy_prev_window():
    global CurrentWindow
    if CurrentWindow is not None:
        CurrentWindow.destroy()

def show_main_window():
    # Создаем окно главного экрана
    root = create_window('Управление телефонным справочником', '400x300')

    # Создаем кнопку для отображения всего справочника
    ShowAllButton = create_button(root, 'Отобразить весь справочник', show_all, pady=10)

    # Создаем кнопку для экспорта данных из справочника
    ExportDataButton = create_button(root, "Взаимодействие с сохраненными контактами", export_data, pady=10)

    # Создаем кнопку для импорта данных в справочник
    ImportDataButton = create_button(root, 'Добавить новый контакт', import_data, pady=10)

    # Создаем кнопку завершения работы
    CloseAppButton = create_button(root, 'Завершить работу', root.destroy, pady=10)

    # Запуск главного цикла обработки событий
    root.mainloop()

def show_all():
    global ShowAllWindow, SearchByNumberEntry

    ShowAllWindow = create_window('Список сохраненных контактов', '700x500')

    try:
    # Получаем список сохраненных контактов
        # Добавляем область для дополнительного взаимодействия с таблицей
        InteractionFrame = tk.Frame(ShowAllWindow)
        InteractionFrame.pack(pady=10, padx=10, side='top')

        # Добавляем кнопку для сортировки по фамилии
        SurnameSortButton = create_button(InteractionFrame, 'Сортировать по фамилии', surname_sort, padx=10, side='left')

        # Доавляем кнопку для сортировки по имени
        NameSortButton = create_button(InteractionFrame, 'Сортировать по имени', name_sort, padx=10, side='left')

        # Добавляем поиск по номеру
        SearchByNumberFrame = tk.Frame(InteractionFrame)
        SearchByNumberFrame.pack(side='right')

        SearchByNumberLabel = tk.Label(SearchByNumberFrame, text='Поиск по номеру:')
        SearchByNumberLabel.pack(side='left')

        SearchByNumberEntry = tk.Entry(SearchByNumberFrame, width=30)
        SearchByNumberEntry.pack(side='left')

        SearchByNumberButton = create_button(SearchByNumberFrame, 'Поиск', search_by_number, side='left')

        get_phone_book()
        create_table()

        # Создаем кнопку для возврата таблицы в исходное состояние
        UpdateTableButton = create_button(ShowAllWindow, 'Вернуть таблицу к исходному состоянию', update_table, pady=10, side='bottom')

        # Создаем кнопку для возврата на главный экран
        ShowMainWindowButton = create_button(ShowAllWindow, 'Назад', show_main_window, pady=10, side='bottom')

    except:
        NoContactsLabel = tk.Label(ShowAllWindow, text='Нет сохраненных контактов')
        NoContactsLabel.pack(side='top')

    # Запуск цикла обработки событий
    ShowAllWindow.mainloop()

def import_data():
    global SurnameEntry, NameEntry, PhoneNumberEntry, CommentEntry
    
    ImportDataWindow = create_window('Введите данные о новом контакте', '400x300')

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
    SaveDataButton = create_button(ImportDataWindow, 'Сохранить данные', save_data, pady=10)

    # Создаем кнопку возврата в главное меню
    BackToMainButton = create_button(ImportDataWindow, 'Назад', show_main_window, pady=10)

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
            PhoneBook[i][-1] = PhoneBook[i][-1].split('\n')
            PhoneBook[i][-1] = ''.join(element for element in PhoneBook[i][-1])

    # Заносим новый контакт в список, если до этого его там не было
    if DataToSave not in PhoneBook:
        PhoneBook.append(DataToSave)

    # Обновляем список контактов
    with open (filepath, 'w') as phout:
        for line in PhoneBook:
            s = ','.join(data for data in line)
            phout.write(f'{s}\n')

def create_table():
    global TableFrame

    TableFrame = tk.Frame(ShowAllWindow)
    TableFrame.pack(pady=10, padx=10, side='top')

    columns = (1, 2, 3, 4)
    Table = ttk.Treeview(TableFrame, columns=columns, show='headings', height=len(PhoneBook))
    
    Table.heading(1, text='Фамилия')
    Table.heading(2, text='Имя')
    Table.heading(3, text='Номер телефона')
    Table.heading(4, text='Комментарий')    

    Table.column(1, width=100)
    Table.column(2, width=100)
    Table.column(3, width=110)
    Table.column(4, width=110)

    for line in PhoneBook:
        Table.insert('', tk.END, values=line)

    Table.pack()

def surname_sort():
    global PhoneBook

    PhoneBook = sorted(PhoneBook, key=lambda x: x[0])
    delete_table()
    create_table()

def name_sort():
    global PhoneBook

    PhoneBook = sorted(PhoneBook, key=lambda x: x[1])
    delete_table()
    create_table()

def search_by_number():
    global PhoneBook

    LinesWithNumber = []
    for line in PhoneBook:
        if SearchByNumberEntry.get() in line[2]:
            LinesWithNumber.append(line)

    PhoneBook = LinesWithNumber
    delete_table()
    create_table()

def delete_table():
    global TableFrame
    if TableFrame:
        TableFrame.destroy()
        TableFrame = None

def get_phone_book():
    global PhoneBook

    PhoneBook = []
    filepath = 'Saved_Data/Phone_book.txt'

    with open (filepath, 'r') as phb:
        for line in phb:
            PhoneBook.append(tuple(line.split(',')))

def update_table():
    get_phone_book()
    delete_table()
    create_table()

def create_window(title, geometry):
    global CurrentWindow

    destroy_prev_window()
    name = tk.Tk()
    name.title(title)
    name.geometry(geometry)
    CurrentWindow = name
    return name

def create_button(area, text, func, pady=None, padx=None, side=None):
    Button = tk.Button(area, text=text, command=func)
    Button.pack(pady=pady, padx=padx, side=side)
    return Button