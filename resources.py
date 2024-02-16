import os
import json



def print_with_indent(value, indent=0):
    """
    Эта функция возвращает значение value * на количество пробелов в indentation
    :param value:
    :param indent:
    :return:
    """
    indentation = '\t' * indent
    print(indentation + str(value))

class Entry:
    def __init__(self, title: str, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        """
        Добавлет в список entries значение entry
        :param entry: Объект класса Entry
        :return: None
        """
        self.entries.append(entry)
        entry.parent = self #тут назначаем родительский класс

    def json(self):
        """
        Этот метод преобразовывает наши значения в списке enties в словарь result, c вложенностями
        :return: dict result
        """
        result = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return result

    def save(self, path: str):
        """
        Этот метод сохраняет в файл, что возвращает метот self.json()
        :param path: путь для создания файла и сохранения в нем
        :return: None
        """
        with open(os.path.join(path, f'{self.title}.json'), 'w') as file:
            json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        """
        Этот метод открывает файл с json-объектом и преобразовывает через метод from_json в объект класса Entry
        :param filename: имя файла с json-объектом
        :return: экземпляр класса Entry
        """
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
            return cls.from_json(content)

    @classmethod
    def from_json(cls, some_json) -> 'Entry':
        """
        Этот метод создает новый объект класса Entry используя JSON объек
        :param some_json: JSON объект
        :return: объъект класса Entry
        """
        new_entry = cls(some_json.get('title'))
        for item in some_json.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def print_entries(self, indent=0):
        """
        Этот метод позволяет нам заглянуть в список self.entries
        и вывести значения в каждой строке используя функцию print_with_indent!
        :return print(self * indent):
        """
        print_with_indent(self, indent=indent)
        for item in self.entries:
            item.print_entries(indent + 1)




class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        """
        Метод проходит по полному пути заданный в data_path, проверяет каждый элемент в директории, если елемент формата
        json, то вызывает метод Entry.load(). В итоге добавляет полученный объект класса Entry в entries
        :return: None
        """
        for item in os.listdir(self.data_path):
            if item.endswith('.json'):
                item = Entry.load(os.path.join(self.data_path, item))
                self.entries.append(item)

    def add_entry(self, title: str):
        """
        Этот метод создает добавляет в список entries объект класса Entry
        :param title: наименование
        :return: None
        """
        new_entry = Entry(title)
        self.entries.append(new_entry)