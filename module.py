import tkinter as tk
from tkinter import ttk

CurrentWindow = None

def destroy_prev_window():
    return

def show_main_window():
    return

def show_all():
    global CurrentWindow, PhoneBook, ShowAllWindow, SearchByNumberEntry

    # Закрываем предыдущее окно
    destroy_prev_window

    # Создаем новое окно для отображения списка контактов
    ShowAllWindow = tk.Tk()
    ShowAllWindow.title('Список всех сохраненных контактов')
    ShowAllWindow.geometry('700x500')
    CurrentWindow = ShowAllWindow

    try:
    # Получаем список сохраненных контактов
        get_phone_book()

        # Добавляем область для дополнительного взаимодействия с таблицей
        InteractionFrame = tk.Frame(ShowAllWindow)
        InteractionFrame.pack(pady=10, padx=10, side='top')

        # Добавляем кнопку для сортировки по фамилии
        SurnameSortButton = tk.Button(InteractionFrame, text='Сортировать по фамилии', command=surname_sort)
        SurnameSortButton.pack(padx=10, side='left')

        # Доавляем кнопку для сортировки по имени
        NameSortButton = tk.Button(InteractionFrame, text='Сортировать по имени', command=name_sort)
        NameSortButton.pack(padx=10, side='left')

        # Добавляем поиск по номеру
        SearchByNumberFrame = tk.Frame(InteractionFrame)
        SearchByNumberFrame.pack(side='right')

        SearchByNumberLabel = tk.Label(SearchByNumberFrame, text='Поиск по номеру:')
        SearchByNumberLabel.pack(side='left')

        SearchByNumberEntry = tk.Entry(SearchByNumberFrame, width=30)
        SearchByNumberEntry.pack(side='left')

        SearchByNumberButton = tk.Button(SearchByNumberFrame, text='Поиск', command=search_by_number)
        SearchByNumberButton.pack(side='left')

        create_table()

        # Создаем кнопку для возврата таблицы в исходное состояние
        UpdateTableButton = tk.Button(ShowAllWindow, text='Вернуть таблицу к исходному состоянию', command=update_table)
        UpdateTableButton.pack(pady=10)

        # Создаем кнопку для возврата на главный экран
        ShowMainWindowButton = tk.Button(ShowAllWindow, text='Назад', command=show_main_window)
        ShowMainWindowButton.pack(pady=10)

    except:
        NoContactsLabel = tk.Label(ShowAllWindow, text='Нет сохраненных контактов')
        NoContactsLabel.pack(side='top')

    # Запуск цикла обработки событий
    ShowAllWindow.mainloop()

def import_data():
    return

def export_data():
    return

def save_data():
    return

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
    PhoneBook = []
    filepath = 'Saved_Data/Phone_book.txt'

    with open (filepath, 'r') as phb:
        for line in phb:
            PhoneBook.append(tuple(line.split(',')))