def jdn(jdn): #функция считающая григорианскую дату (формула из википедии)
    c = (jdn + 32082)//1
    d = (4*c+3)//1461
    e = c - (1461*d)//4
    m = (5*e+2)//153
#

    month = m + 3 - 12*(m//10)
    year = d - 4800 + (m//10)
    hour0 = jdn%1*60
    hour = hour0-hour0%1 + 12
    if hour  > 24: # если часов в дне получилось больше 24, то прибавляем сутки
        day = e - ((153 * m + 2) // 5) + 2
        houri = hour - 24
    else:
        day = e - ((153 * m + 2) // 5) + 1
    minute0 = hour0%1*60
    minute = minute0 - minute0%1
    second0 = minute0%1*60
    second = second0 - second0%1
    return f'{int(day)}.{int(month)}.{int(year)} {int(houri)}.{int(minute)}.{int(second)}'

file = open("star.txt", "r")
stars = file.read().split('\n') # читаем весь файл и делим его на строки
file.close()

first = [] # временный массив
for elem in stars: # перебираем все ряды(элементы массива)
    first.append(elem.split()) # разделяем ряды по пробелам

first = first[1:] # удалил нам первую строку с названиями столбцов
stars = first # заменяем изначальный массив временным

objects = set() # имена объектов в виде множества
filters = set() # фильтры
dates = []
for elem in stars:
    name = '' # формируем одинаковое имя
    if len(elem) > 4:
        name = elem[0] + ' ' + elem[1]
        elem = [name] + elem[2:]
    elif len(elem) < 4:
        continue
    else:
        name = elem[0]

    #тут мы хотим, что программа любыве написания имени воспринимала как одно и то же, приводим все к одному виду
    name = name.replace('_', '') #удаляем нижнее подчеркивание межлу словами
    name = name.replace(' ', '') #удаляем пробел между словами
    name = name.lower() #делаем все буквы маленькими
    name = name[:2].upper() + ' ' + name[2:].title() # suhor = SU Hor -> приводим названия к одному виду
    elem[0] = name #первый элемент каждой строчки - имя объекта

    if len(elem) > 4:
        elem[2] = float('24' + elem[2])  # преобразуем юлианскую дату и звездную величину в числа из строк
    else:
        elem[1] = float('24' + elem[1])
    elem[3] = float(elem[3])

    objects.add(elem[0]) # проверяем на новое имя объекта
    dates.append(elem[1]) #заносим в список даты
    filters.add(elem[2].title()) # проверяем на новый фильтр

print('Объекты:', objects)
print('Фильтры:', filters)

# последняя чатсь задания

object_name = input('Введите имя объекта: ')  # просим пользователя ввести имя объекта

filters_names = set()
while len(filters.intersection(
        filters_names)) == 0:  # пересечение введенных фильтров и filters_names - корректные фильтры
    inp = input('Введите фильтры, разделенные запятой: ')  # то же самое, но с фильтрами
    filters_names = set(inp.split(',')) #разделение запятой

filters_names = filters.intersection(filters_names) #находит одинаковые элементы в двух списках

processed = {}  # словарь с обработанной информацией из stars
for entry in stars:
    if len(entry) == 0: # список пуст - пропускаем
        continue
    if entry[0] != object_name: # объект не введенный пользователем - пропускаем
        continue
    if entry[2] not in filters_names:  # фильтр не введенный пользователем - пропускаем
        continue
    if entry[1] not in processed:
        processed[entry[1]] = {'date': jdn(entry[1])} #с помощью функции считаем григорианскую дату
        for filter_name in filters_names:
            processed[entry[1]][filter_name] = '-'  # назначаем всем столбцам-фильтрам значение '-'
        processed[entry[1]][entry[2]] = entry[3]

flo = open(f'{object_name}.dat', 'w')  # создаем файл с нужным именем
headers = 'Date\tHJD\t\t'  # создаем ряд-заголовок
for filter in filters_names:
    headers += filter + '\t'  # добавляем столбцы-фильтры
headers = headers[:-1] + '\n'  # удаляем лишнюю табуляцию и добавляем переход строки
flo.write(headers)  # записываем

#dates = list(processed.keys())  # переводим ключи в словаре processed в список, чтобы можно было его отсортировать
dates.sort()  # сортировка

for date in dates:  # проходимся по списку dates в порядке возрастания
    if date not in processed: # дата относится к другому объекту или фильтру - пропускаем
        continue
    value = processed[date]  # получаем соответствующую информацию из словаря processed
    s = value['date'] + '\t' + str(date) + '\t'  # первый столбец - григорианская дата, второй - JD
    for filter in filters_names:
        s += str(value[filter]) + '\t'  # добавляем столбцы-фильтры в порядке, в котором они были в сете filters_names
    s = s[:-1] + '\n'  # удаляем лишнюю табуляцию, переход строки
    flo.write(s)  # запись

flo.close()  # закрытие файла