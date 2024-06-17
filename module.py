import tkinter as tk
from tkinter import ttk

CurrentWindow = None

def show_main_window():
    # Создаем окно главного экрана
    root = create_window('Управление телефонным справочником', '400x300')

    # Создаем кнопку для отображения всего справочника
    create_button(root, 'Отобразить весь справочник', show_all, pady=10)

    # Создаем кнопку для импорта данных в справочник
    create_button(root, 'Добавить новый контакт', import_data, pady=10)

    # Создаем кнопку завершения работы
    create_button(root, 'Завершить работу', root.destroy, pady=10)

    # Запуск главного цикла обработки событий
    root.mainloop()

def show_all(get_iterables=False):
    def create_table(PhoneBook):
        global TableFrame

        TableFrame = tk.Frame(ShowAllWindow)
        TableFrame.pack(pady=10, padx=10, side='top')

        cols = tuple(i for i in range(len(headings)))
        cols_sizes = (100, 100, 120, 130)
        Table = ttk.Treeview(TableFrame, columns=cols, show='headings', height=12)
        
        for i in range(len(headings)):
            Table.heading(cols[i], text=headings[i])

        for i in range(len(headings)):
            Table.column(i, width=cols_sizes[i])

        for line in PhoneBook:
            Table.insert('', tk.END, values=line)

        Table.pack()

    def surname_sort():
        PhoneBook = search_by_number()
        PhoneBook = sorted(PhoneBook, key=lambda x: x[0])
        TableFrame.destroy()
        create_table(PhoneBook)

    def name_sort():
        PhoneBook = search_by_number()
        PhoneBook = sorted(PhoneBook, key=lambda x: x[1])
        TableFrame.destroy()
        create_table(PhoneBook)

    def search_by_number():
        LinesWithNumber = []
        PhoneBook = get_phone_book()
        for line in PhoneBook:
            if SearchByNumberEntry.get() in line[2]:
                LinesWithNumber.append(line)
                
        PhoneBook = LinesWithNumber
        TableFrame.destroy()
        create_table(PhoneBook)
        return PhoneBook

    def update_table():
        PhoneBook = get_phone_book()
        SearchByNumberEntry.delete(0,tk.END)
        TableFrame.destroy()
        create_table(PhoneBook)

    def change_data():
        IndexToChange = IndexToChangeEntry.get()
        if IndexToChange:
            ChangeDataWindow = create_window('Изменение данных о контакте', '500x500')
            headings = ('Индекс', 'Фамилия', 'Имя', 'Номер телефона', 'Комментарий')
            PhoneBook = get_phone_book()
            

    ShowAllWindow = create_window('Список сохраненных контактов', '700x500')

    # Получаем список сохраненных контактов
    PhoneBook = get_phone_book()

    if PhoneBook:
        # Создаем окно для взаимодействия со списком сохраненных контактов
        InteractionFrame = tk.Frame(ShowAllWindow)
        InteractionFrame.pack(pady=10, padx=10, side='top')

        # Добавляем кнопку для сортировки по фамилии
        create_button(InteractionFrame, 'Сортировать по фамилии', surname_sort, padx=10, side='left')

        # Доавляем кнопку для сортировки по имени
        create_button(InteractionFrame, 'Сортировать по имени', name_sort, padx=10, side='left')

        # Добавляем поиск по номеру
        SearchByNumberFrame, SearchByNumberEntry = create_entry(InteractionFrame, 'Поиск по номеру:', 
                                                                fside='right', lside='left', eside='left')

        create_button(SearchByNumberFrame, 'Поиск', search_by_number, side='left')
        
        # Строим таблицу
        create_table(PhoneBook)

        # Создаем кнопку для возврата таблицы в исходное состояние
        create_button(ShowAllWindow, 'Вернуть таблицу к исходному состоянию', update_table, pady=10, side='bottom')

        # Создаем кнопку для возврата на главный экран
        create_button(ShowAllWindow, 'Назад', show_main_window, pady=10, side='bottom')

        # Создаем поле для выбора контакта для редактирования
        IndexToChangeFrame, IndexToChangeEntry = create_entry(ShowAllWindow, 'Введите индекс контакта, который хотите отредактиовать', 
                                                              fside='top')
        create_button(IndexToChangeFrame, 'Выбрать', change_data)

    else:
        # Если контактов не обнаружено, сообщаем об этом
        NoContactsLabel = tk.Label(ShowAllWindow, text='Нет сохраненных контактов')
        NoContactsLabel.pack(side='top')

    ShowAllWindow.mainloop()

def import_data():
    def save_data():
        filepath = 'Saved_Data/Phone_book.txt'
        DataToSave = [SurnameEntry.get(), NameEntry.get(), PhoneNumberEntry.get(), CommentEntry.get()]

        # Получаем список уже существующих контактов, если такие есть
        PhoneBook = get_phone_book()

        # Заносим новый контакт в список, если до этого его там не было
        if DataToSave not in PhoneBook:
            PhoneBook.append(DataToSave)

        # Обновляем список контактов
        with open(filepath, 'w', encoding='utf-8') as phb:
            for line in PhoneBook:
                s = ','.join(data for data in line)
                phb.write(f'{s}\n')
    
    ImportDataWindow = create_window('Введите данные о новом контакте', '400x300')

    # Создаем поле ввода фамилии
    SurnameEntry = create_entry(ImportDataWindow, 'Введите фамилию: ', fpady=10, 
                                fpadx=20, lside='left', eside='left')[1]

    # Создаем поле ввода имени
    NameEntry = create_entry(ImportDataWindow, 'Введите имя: ', fpady=10, 
                             fpadx=20, lside='left', eside='left')[1]

    # Создаем поле ввода номера телефона
    PhoneNumberEntry = create_entry(ImportDataWindow, 'Введите номер телефона: ', fpady=10, 
                                    fpadx=20, lside='left', eside='left')[1]

    # Создаем поле ввода комментария
    CommentEntry = create_entry(ImportDataWindow, 'Введите комментарий: ', fpady=10, 
                                fpadx=20, lside='left', eside='left')[1]

    # Создаем кнопку для сохранения данных
    create_button(ImportDataWindow, 'Сохранить данные', save_data, pady=10)

    # Создаем кнопку возврата в главное меню
    create_button(ImportDataWindow, 'Назад', show_main_window, pady=10)

    # Запуск цикла обработки событий
    ImportDataWindow.mainloop()

def get_phone_book():
    data = []
    filepath = 'Saved_Data/Phone_book.txt'
    headings = ['№', 'Фамилия', 'Имя', 'Номер телефона', 'Комментарий']

    # Получаем данные о существующих контактах
    with open(filepath, 'r', encoding='utf-8') as phb:
        for line in phb:
            data.append(line.split(','))

    # Убираем переходы на другую строку
    for i in range(len(data)):
        data[i] = list(data[i])
        if '\n' in data[i][-1]:
            data[i][-1] = data[i][-1].split('\n')
            data[i][-1] = ''.join(element for element in data[i][-1])

    # Добавляем индексы
    for i in range(len(data)):
        data[i].insert(0, i)

    # Формируем словарь со всеми данными
    PhoneBook = {'№':[], 'Фамилия':[], 'Имя':[], 'Номер телефона':[], 'Комментарий':[]}
    for i in range(len(data)):
        for j in range(len(data[i])):
            PhoneBook[headings[j]].append(data[i][j])
        
    return PhoneBook

def create_window(title, geometry):
    global CurrentWindow

    def destroy_prev_window():
        if CurrentWindow is not None:
            CurrentWindow.destroy()

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

def create_entry(area, text, width=30, fside=None, lside=None, eside=None, fpady=None, fpadx=None):
    # Создаем область, в которой будут располагаться поле ввода и его пояснение
    Frame = tk.Frame(area)
    Frame.pack(side=fside, padx=fpadx, pady=fpady)

    # Создаем пояснение к полю ввода
    Label = tk.Label(Frame, text=text)
    Label.pack(side=lside)

    # Создаем поле ввода
    Entry = tk.Entry(Frame, width=width)
    Entry.pack(side=eside)

    return Frame, Entry
