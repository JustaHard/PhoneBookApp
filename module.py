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
    create_button(root, 'Отобразить весь справочник', show_all, pady=10)

    # Создаем кнопку для экспорта данных из справочника
    create_button(root, "Взаимодействие с сохраненными контактами", export_data, pady=10)

    # Создаем кнопку для импорта данных в справочник
    create_button(root, 'Добавить новый контакт', import_data, pady=10)

    # Создаем кнопку завершения работы
    create_button(root, 'Завершить работу', root.destroy, pady=10)

    # Запуск главного цикла обработки событий
    root.mainloop()

def show_all():
    global ShowAllWindow, SearchByNumberEntry

    ShowAllWindow = create_window('Список сохраненных контактов', '700x500')

    # try:
    # Получаем список сохраненных контактов

    # Добавляем область для дополнительного взаимодействия с таблицей
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
    
    PhoneBook = get_phone_book()
    create_table(PhoneBook)

    # Создаем кнопку для возврата таблицы в исходное состояние
    create_button(ShowAllWindow, 'Вернуть таблицу к исходному состоянию', update_table, pady=10, side='bottom')

    # Создаем кнопку для возврата на главный экран
    create_button(ShowAllWindow, 'Назад', show_main_window, pady=10, side='bottom')

    # except:
    #     NoContactsLabel = tk.Label(ShowAllWindow, text='Нет сохраненных контактов')
    #     NoContactsLabel.pack(side='top')

    # Запуск цикла обработки событий
    ShowAllWindow.mainloop()

def import_data():
    global SurnameEntry, NameEntry, PhoneNumberEntry, CommentEntry
    
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

def export_data():
    return

def save_data():
    filepath = 'Saved_Data/Phone_book.txt'
    DataToSave = [SurnameEntry.get(), NameEntry.get(), PhoneNumberEntry.get(), CommentEntry.get()]

    # Получаем список уже существующих контактов, если такие есть
    try:
        PhoneBook = get_phone_book()
    except:
        pass

    # Решаем проблему с кучей пустых строк
    for i in range(len(PhoneBook)):
        PhoneBook[i] = list(PhoneBook[i])
        if '\n' in PhoneBook[i][-1]:
            PhoneBook[i][-1] = PhoneBook[i][-1].split('\n')
            PhoneBook[i][-1] = ''.join(element for element in PhoneBook[i][-1])

    # Заносим новый контакт в список, если до этого его там не было
    if DataToSave not in PhoneBook:
        PhoneBook.append(DataToSave)

    # Обновляем список контактов
    with open (filepath, 'w', encoding='utf-8') as phout:
        for line in PhoneBook:
            s = ','.join(data for data in line)
            phout.write(f'{s}\n')

def create_table(PhoneBook):
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
    PhoneBook = get_phone_book()
    PhoneBook = sorted(PhoneBook, key=lambda x: x[0])
    delete_table()
    create_table(PhoneBook)

def name_sort():
    PhoneBook = get_phone_book()
    PhoneBook = sorted(PhoneBook, key=lambda x: x[1])
    delete_table()
    create_table(PhoneBook)

def search_by_number():
    LinesWithNumber = []
    PhoneBook = get_phone_book()
    for line in PhoneBook:
        if SearchByNumberEntry.get() in line[2]:
            LinesWithNumber.append(line)

    PhoneBook = LinesWithNumber
    delete_table()
    create_table(PhoneBook)

def delete_table():
    global TableFrame
    if TableFrame:
        TableFrame.destroy()
        TableFrame = None

def get_phone_book():
    PhoneBook = []
    filepath = 'Saved_Data/Phone_book.txt'

    with open (filepath, 'r', encoding='utf-8') as phb:
        for line in phb:
            PhoneBook.append(tuple(line.split(',')))
        
    return PhoneBook

def update_table():
    PhoneBook = get_phone_book()
    delete_table()
    create_table(PhoneBook)

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

def create_entry(area, text, width=30, fside=None, lside=None, eside=None, fpady=None, fpadx=None):
    Frame = tk.Frame(area)
    Frame.pack(side=fside, padx=fpadx, pady=fpady)

    Label = tk.Label(Frame, text=text)
    Label.pack(side=lside)

    Entry = tk.Entry(Frame, width=width)
    Entry.pack(side=eside)

    return Frame, Entry
