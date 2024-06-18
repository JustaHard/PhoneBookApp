import tkinter as tk
import os
from tkinter import ttk

CurrentWindow = None

def show_main_window():
    '''
    Главное окно, с которого начинается программа
    '''

    # Создаем окно главного экрана
    root = create_window('Управление телефонным справочником', '400x300')

    # Создаем кнопку для отображения всего справочника
    create_button(root, 'Отобразить весь справочник', show_all, pady=10)

    # Создаем кнопку для импорта данных в справочник
    create_button(root, 'Добавить новый контакт', create_new_contact, pady=10)

    # Создаем кнопку для клонирования данных из другого файла
    create_button(root, 'Импортировать данные из другого файла', import_data, pady=10)

    # Создаем кнопку завершения работы
    create_button(root, 'Завершить работу', root.destroy, pady=10)

    # Запускаем цикл обработки событий
    root.mainloop()

def show_all():
    '''
    Просмотр и изменение списка сохраненных контактов
    '''

    def create_table(data):
        """
        Создаем таблицу с заданными данными

        data(dict) - Словарь с данными, которые нужно отобразить в таблице
        """

        global TableFrame

        # Создаем область, в которой располагается таблица
        TableFrame = tk.Frame(ShowAllWindow)
        TableFrame.pack(pady=10, padx=10, side='top')

        # Задаем параметры таблицы
        cols = tuple(i for i in range(len(data)))
        cols_sizes = (30, 100, 100, 120, 130)
        Table = ttk.Treeview(TableFrame, columns=cols, show='headings', height=12)

        # Указываем заголовки таблицы
        for i in range(len(data)):
            Table.heading(cols[i], text=list(data.keys())[i])

        # Указываем размеры столбцов таблицы
        for i in range(len(data)):
            Table.column(i, width=cols_sizes[i])

        # Заносим данные в таблицу
        for i in range(len(list(data.values())[0])):
            for key in data.keys():
                if key == '№':
                    Line = []
                Line.append(data[key][i])
            Table.insert('', tk.END, values=Line)

        # Выводим таблицу в окне
        Table.pack()

    def surname_sort():
        """
        Сортировка таблицы по фамилии контакта
        """

        # Получаем данные о сохраненных контактах
        PhoneBook = search_by_number()

        # Сортируем данные по фамилии
        PhoneBook = dict_to_list(PhoneBook)
        PhoneBook = sorted(PhoneBook, key=lambda x: x[1])
        PhoneBook = list_to_dict(PhoneBook)

        # Обновляем таблицу
        TableFrame.destroy()
        create_table(PhoneBook)

    def name_sort():
        """
        Сортировка таблицы по имени контакта
        """

        # Получаем данные о сохраненных контактах
        PhoneBook = search_by_number()

        # Сортируем данные по имени
        PhoneBook = dict_to_list(PhoneBook)
        PhoneBook = sorted(PhoneBook, key=lambda x: x[2])
        PhoneBook = list_to_dict(PhoneBook)

        # Обновляем таблицу
        TableFrame.destroy()
        create_table(PhoneBook)

    def search_by_number():
        """
        Фильтруем данные таблицы по введенному фрагменту номера телефона
        """

        # Получаем данные о сохраненных контактах
        PhoneBook = get_phone_book()

        # Указываем переменную, в которую будем сохранять подходящие контакты
        LinesWithNumber = dict()
        for key in PhoneBook.keys():
            LinesWithNumber[key] = []
        
        # Ищем контакты с указанным номером
        for i in range(len(list(PhoneBook.values())[0])):
            if SearchByNumberEntry.get() in PhoneBook["Номер телефона"][i]:
                for key in PhoneBook.keys():
                    LinesWithNumber[key].append(PhoneBook[key][i])
                
        # Меняем таблицу на измененную
        TableFrame.destroy()
        create_table(LinesWithNumber)
        return LinesWithNumber

    def rebuild_table():
        """
        Возвращаем таблицу к исходному состоянию
        """

        # Получаем данные о сохраненных контактах
        PhoneBook = get_phone_book()

        # Очищаем поле ввода для фильтрации таблицы по номеру
        SearchByNumberEntry.delete(0,tk.END)

        # Обновляем таблицу
        TableFrame.destroy()
        create_table(PhoneBook)

    def change_data():
        """
        Внесение изменений в данные об указанном контакте
        """

        def save_changes():
            """
            Сохранение внесенных изменений
            """

            # Вносим изменения в список контактов
            for i in range(len(PhoneBook)):
                PhoneBook[list(PhoneBook.keys())[i]][IndexToChange] = EntriesToChange[i].get()

            # Сохраняем изменения в файл и возвращаемся к списку контактов
            update_data(PhoneBook)
            show_all()

        def delete_data():
            """
            Удаление указанного контакта из базы данных
            """

            # Удаляем контакт из списка
            for i in range(len(PhoneBook)):
                PhoneBook[list(PhoneBook.keys())[i]].pop(IndexToChange)

            # Сохраняем изменения в файл и возвращаемся к списку контактов
            update_data(PhoneBook)
            show_all()
        
        # Проверяем что поле для указания индекса контакта не пустое
        if IndexToChangeEntry.get():

            # Если введенную информацию нельзя представить в виде int, сообщаем об этом
            try:
                # Получаем данные о сохраненных контактах и индекс контакта, 
                # который нужно изменить
                IndexToChange = int(IndexToChangeEntry.get())
                PhoneBook = get_phone_book()

                # Проверяем, что контакт с указанным индексом существует
                if IndexToChange in PhoneBook['№']:
                    # Создаем новое окно для редактирования контакта
                    ChangeDataWindow = create_window('Изменение данных о контакте', '500x500')

                    # Создаем кнопку для удаления контакта
                    create_button(ChangeDataWindow, 'Удалить контакт', delete_data, pady=10)

                    # Даем пользователю возможность изменить данные о контакте
                    PhoneBook.pop('№')
                    EntriesToChange = []
                    for key in PhoneBook.keys():
                        entry = create_entry(ChangeDataWindow, key, fpady=10)[1]
                        entry.insert(0, PhoneBook[key][IndexToChange])
                        EntriesToChange.append(entry)

                    # Создаем кнопки для сохранения и отмены изменений
                    create_button(ChangeDataWindow, 'Сохранить', save_changes)
                    create_button(ChangeDataWindow, 'Отменить', show_all, pady=10)
                
                else:
                    # Создаем окно для вывода ошибки
                    IndexErrorWindow = create_window('Ошибка', '300x100')

                    # Выводим сообщение об ошибке
                    IndexErrorLabel = tk.Label(IndexErrorWindow, 
                                            text='Контакт с указанным индексом не существует')
                    IndexErrorLabel.pack(pady=10)

                    # Создаем кнопку для возврата к таблице с контактами
                    create_button(IndexErrorWindow, 'Назад', show_all, pady=10)
            except ValueError:
                # Создаем окно для вывода ошибки
                DataTypeErrorWindow = create_window('Ошибка', '300x100')

                # Выводим сообщение об ошибке
                DataTypeErrorLabel = tk.Label(DataTypeErrorWindow, 
                                              text='Введенная информация не является индексом')
                DataTypeErrorLabel.pack(pady=10)

                # Создаем кнопку для возврата к таблице с контактами
                create_button(DataTypeErrorWindow, 'Назад', show_all, pady=10)
            
    # Создаем окно для вывода списка сохраненных контактов
    ShowAllWindow = create_window('Список сохраненных контактов', '700x500')

    # Получаем список сохраненных контактов
    PhoneBook = get_phone_book()

    # Проверяем, есть ли сохраненные контакты
    if PhoneBook['№']:
        # Создаем окно для взаимодействия со списком сохраненных контактов
        InteractionFrame = tk.Frame(ShowAllWindow)
        InteractionFrame.pack(pady=10, padx=10, side='top')

        # Добавляем кнопку для сортировки по фамилии
        create_button(InteractionFrame, 'Сортировать по фамилии', 
                      surname_sort, padx=10, side='left')

        # Добавляем кнопку для сортировки по имени
        create_button(InteractionFrame, 'Сортировать по имени', 
                      name_sort, padx=10, side='left')

        # Добавляем поиск по номеру
        SearchByNumberFrame, SearchByNumberEntry = create_entry(InteractionFrame, 
                                                                'Поиск по номеру:', 
                                                                fside='right', lside='left', 
                                                                eside='left')
        create_button(SearchByNumberFrame, 'Поиск', search_by_number, side='left')
        
        # Строим таблицу
        create_table(PhoneBook)

        # Создаем кнопку для возврата на главный экран
        create_button(ShowAllWindow, 'Назад', show_main_window, pady=10, side='bottom')

        # Создаем кнопку для возврата таблицы в исходное состояние
        create_button(ShowAllWindow, 'Вернуть таблицу к исходному состоянию', 
                      rebuild_table, pady=10, side='bottom')

        # Создаем поле для выбора контакта для редактирования
        IndexToChangeFrame, IndexToChangeEntry = create_entry(ShowAllWindow, 
            'Введите индекс контакта, который хотите отредактиовать', fside='bottom')
        create_button(IndexToChangeFrame, 'Выбрать', change_data, pady=5)

    else:
        # Если контактов не обнаружено, сообщаем об этом
        NoContactsLabel = tk.Label(ShowAllWindow, text='Нет сохраненных контактов')
        NoContactsLabel.pack(side='top', pady=20)

        # Создаем кнопку для возврата на главный экран
        create_button(ShowAllWindow, 'Назад', show_main_window, pady=10, side='bottom')

def create_new_contact():
    """
    Сохранение нового контакта
    """

    def save_data():
        """
        Внесение нового контакта в базу данных
        """

        # Получаем данные о ранее сохраненных контактах и приводим их в удобный вид
        PhoneBook = get_phone_book()
        PhoneBook.pop('№')
        comments = PhoneBook.pop('Комментарий')
        PhoneBook = dict_to_list(PhoneBook)

        # Получаем данные о контакте, который нужно сохранить
        DataToSave = [data.get() for data in Entries]

        # Заносим новый контакт в список, если до этого его там не было
        if DataToSave[:-1] not in PhoneBook:
            PhoneBook.append(DataToSave[:-1])
            comments.append(DataToSave[-1])

            for i in range(len(PhoneBook)):
                PhoneBook[i].append(comments[i])

            # Обновляем список контактов
            update_data(PhoneBook)
            create_new_contact()

        else:
            # Создаем окно, чтобы сообщить пользователю, что контакт уже существует
            ContactAlreadyExistsWindow = create_window('Контакт уже существует', '300x100')

            # Выводим сообщение
            ContactAlreadyExistsLabel = tk.Label(ContactAlreadyExistsWindow, 
                                                text='Данный контакт уже существует')
            ContactAlreadyExistsLabel.pack(pady=10)

            # Создаем кнопку для возврата к окну введения данных о новом контакте
            create_button(ContactAlreadyExistsWindow, 'Назад', create_new_contact, pady=10)

    # Создаем окно для создания нового контакта
    CreateNewContactWindow = create_window('Введите данные о новом контакте', '400x300')
    
    # Создаем поля ввода для указания данных о новом контакте
    Entries = []
    for i in ['Фамилия', 'Имя', 'Номер телефона', 'Комментарий']:
        entry = create_entry(CreateNewContactWindow, i, fpady=10, fpadx=20, lside='left', 
                             eside='left')[1]
        Entries.append(entry)

    # Создаем кнопку для сохранения данных
    create_button(CreateNewContactWindow, 'Сохранить данные', save_data, pady=10)

    # Создаем кнопку возврата в главное меню
    create_button(CreateNewContactWindow, 'Назад', show_main_window, pady=10)

def import_data():
    """
    Импорт данных из стороннего файла
    """

    def choose_lines():
        """
        Выбор линий, которые надо импортировать из файла
        """

        def import_from_file():
            """
            Получаем данные из файла и сохраняем в базу данных
            """

            # Проверяем, что поле для ввода не пустое
            if ChooseLinesEntry.get():
                # Преобразуем введенные данные в массив
                LinesToImport = list(set(ChooseLinesEntry.get().replace(' ', '').split(',')))

                # Получаем список сохраненных контактов
                PhoneBook = get_phone_book()

                # Получаем информацию из указанного файла
                FileData = get_phone_book(filepath=FilePath)

                # Импортируем строки, которые можно импортировать
                BadLines = {'Line':[], 'Reason':[]}
                for i in range(len(LinesToImport)):
                    try:
                        if int(LinesToImport[i]) in FileData['№']:
                            for key in PhoneBook.keys():
                                PhoneBook[key].append(FileData[key][int(LinesToImport[i])])
                        else:
                            BadLines['Line'].append(LinesToImport[i])
                            BadLines['Reason'].append('Строка не найдена')
                    except ValueError:
                        BadLines['Line'].append(LinesToImport[i])
                        BadLines['Reason'].append('Неверный тип данных')

                # Обновляем данные
                update_data(PhoneBook.pop('№'))

                # Если не все указанные линии получилось импортировать, сообщаем об этом
                if BadLines:
                    # Создаем окно
                    BadLinesWindow = create_window('Не все линии получилось импортировать')
                    
                    # Выводим сообщение
                    BadLinesLabel = tk.Label(BadLinesWindow, 
                                        text=f'Не удалось импортировать линии {BadLines}')
                    BadLinesLabel.pack(pady=10)

                    # Создаем кнопку возврата
                    create_button(BadLinesWindow, 'Назад', import_data, pady=10)

                else:
                    import_data()

        # Проверяем, что поле для ввода не пустое
        if GetFilePathEntry.get():
            FilePath = GetFilePathEntry.get()

            # Проверяем, существует ли указанный файл
            if os.path.exists(FilePath):
                # Создаем окно
                ChooseLinesWindow = create_window('Импорт данных из другого файла',
                                                  '300x200')
                
                # Создаем поле ввода
                ChooseLinesFrame, ChooseLinesEntry = create_entry(ChooseLinesWindow,
                        'Укажите линии, которые хотите импортировать', 
                        fpady=10)
                create_button(ChooseLinesFrame, 'Выбор', import_from_file, pady=10)

                # Создаем кнопку для возврата
                create_button(ChooseLinesWindow, 'Назад', import_data, pady=10)

            else:
                # Создаем окно
                FileNotFoundWindow = create_window('Ошибка', '300x100')

                # Выводим сообщение
                FileNotFoundLabel = tk.Label(FileNotFoundWindow, 
                                             text='Указанный файл не найден')
                FileNotFoundLabel.pack(pady=10)

                # Создаем кнопку для возврата
                create_button(FileNotFoundWindow, 'Назад', import_data, pady=10)

    # Создаем окно
    ImportDataWindow = create_window('Импорт данных из другого файла', '400x150')
    
    # Создаем поле ввода для указания пути стороннего файла
    GetFilePathFrame, GetFilePathEntry = create_entry(ImportDataWindow, 
                            'Укажите путь к файлу, из которого хотите импортировать данные', 
                            fpady=10)
    create_button(GetFilePathFrame, 'Ввод', choose_lines, pady=10)

    # Создаем кнопку для возврата на главный экран
    create_button(ImportDataWindow, 'Назад', show_main_window)

def get_phone_book(filepath='Saved_Data/Phone_book.txt'):
    """
    Получение данных об уже сохраненных контактах

    filepath(Path) - Путь к файлу, из которого нужно получить данные
    """
    
    data = []

    # Проверяем, существует ли указанный файл
    if os.path.exists(filepath):
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
    PhoneBook = list_to_dict(data)
        
    return PhoneBook

def update_data(data, filepath='Saved_Data/Phone_book.txt'):
    """
    Обновляем список сохраненных контактов
    
    data - Данные, которые мы сохраняем вместо предыдущих
    filepath(Path) - Путь к файлу, в который нужно загрузить данные
    """

    # Если данные записаны в виде словаря, переводим их в вид массива
    if type(data) == dict:
        data = dict_to_list(data)

    DirsToFile = '/'.join(filepath.split('/')[:-1])

    # Проверяем, есть ли дополнительные папки в пути к указанному файлу
    if DirsToFile:
        # Если указанного файла не существует, создаем папки к этому файлу
        if not os.path.exists(DirsToFile):
            os.makedirs(DirsToFile)

    # Записываем данные в указанный файл
    with open(filepath, 'w', encoding='utf-8') as phb:
            for line in data:
                s = ','.join(str(data) for data in line)
                phb.write(f'{s}\n')

def create_window(title, geometry):
    """
    Создаем новое окно и удаляем предыдущее

    title(str) - Заголовок окна

    geometry('WIDTHxHEIGHT') - Размер окна в пикселях
    """

    global CurrentWindow

    # Удаляем предыдущее окно
    if CurrentWindow is not None:
        CurrentWindow.destroy()

    # Создаем новое окно
    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
    CurrentWindow = window
    return window

def create_button(area, text, func, pady=None, padx=None, side=None):
    """
    Создаем кнопку
    area(window or frame) - Область, в которой будет располагаться кнопка
    text(str) - Текст на кнопке
    func - Функция, которая будет выполняться при нажатии на кнопку
    pady(int) - Вертикальный отступ кнопки
    padx(int) - Горизонтальный отступ кнопки
    side['top', 'bottom', 'left', 'right'] - Сторона area, к которой будет 
        стремиться кнопка
    """

    Button = tk.Button(area, text=text, command=func)
    Button.pack(pady=pady, padx=padx, side=side)

def create_entry(area, text, width=30, fside=None, lside=None, eside=None, 
                 fpady=None, fpadx=None):
    """
    Создаем поле ввода
    area(window or frame) - Область, в которой будет располагаться поле
    text(str) - Текст рядом с полем ввода
    width(int) - Ширина поля ввода
    fside['top', 'bottom', 'left', 'right'] - Сторона area, к которой будет 
        стремиться созданная область
    lside['top', 'bottom', 'left', 'right'] - Сторона frame, к которой будет 
        стремиться текст рядом с полем ввода
    fside['top', 'bottom', 'left', 'right'] - Сторона frame, к которой будет 
        стремиться поле ввода
    fpady(int) - Вертикальный отступ созданной области
    fpadx(int) - Горизонтальный отступ созданной области
    """

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

def dict_to_list(Dict):
    """
    Из словаря с данными создаем массив с данными
    
    Dict - Словарь, из которого нужно сделать массив
    """

    List = []
    for i in range(len(list(Dict.values())[0])):
        List.append(list())
        for key in Dict.keys():
            List[i].append(Dict[key][i])

    return List

def list_to_dict(List):
    """
    Из массива с данными создаем словарь с данными
    
    List - Массив, из которого нужно сделать словарь
    """

    Dict = {'№':[], 'Фамилия':[], 'Имя':[], 'Номер телефона':[], 'Комментарий':[]}
    for i in range(len(List)):
        for j in range(len(List[i])):
            Dict[list(Dict.keys())[j]].append(List[i][j])

    return Dict
