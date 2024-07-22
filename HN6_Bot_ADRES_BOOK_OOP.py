from collections import UserDict

class Field:
    def __init__(self, value):
        # Ініціалізація базового класу поля з значенням
        self.value = value

    def __str__(self):
        # Повернення рядкового представлення значення
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        # Ініціалізація класу Name з перевіркою на непорожнє значення
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        # Ініціалізація класу Phone з валідацією номера телефону
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        # Перевірка, чи складається номер телефону з 10 цифр
        return phone.isdigit() and len(phone) == 10


class Record:
    def __init__(self, name):
        # Ініціалізація запису з ім'ям і порожнім списком телефонів
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Додавання нового телефону до запису
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видалення телефону з запису
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефону у записі
        old_phone_obj = self.find_phone(old_phone)
        if old_phone_obj:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("Old phone number not found")

    def find_phone(self, phone):
        # Пошук телефону у записі
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        # Повернення рядкового представлення запису
        phones_str = '; '.join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Додавання запису до адресної книги
        self.data[record.name.value] = record

    def find(self, name):
        # Пошук запису за ім'ям
        return self.data.get(name, None)

    def delete(self, name):
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found")

    def __str__(self):
        # Повернення рядкового представлення адресної книги
        return '\n'.join(str(record) for record in self.data.values())


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє помилки типу KeyError, ValueError, IndexError.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Invalid command format."
    return inner


def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.

    :param user_input: Введений користувачем рядок
    :return: Кортеж з команди та аргументів
    """
    cmd, *args = user_input.strip().lower().split()
    return cmd, args


@input_error
def add_contact(args, contacts):
    """
    Додає новий контакт до словника контактів.

    :param args: Список з імені та номеру телефону
    :param contacts: Словник контактів
    :return: Повідомлення про результат операції
    """
    if len(args) != 2:
        raise ValueError("Command requires exactly 2 arguments (name and phone).")
    name, phone = args
    if contacts.find(name):
        raise ValueError("Contact already exists.")
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Змінює номер телефону існуючого контакту.

    :param args: Список з імені та нового номеру телефону
    :param contacts: Словник контактів
    :return: Повідомлення про результат операції
    """
    if len(args) != 2:
        raise ValueError("Command requires exactly 2 arguments (name and new phone).")
    name, new_phone = args
    record = contacts.find(name)
    if record:
        old_phone = record.phones[0].value  # Припустимо, що змінюємо перший номер
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")


@input_error
def show_phone(args, contacts):
    """
    Показує номер телефону для заданого імені.

    :param args: Список з одного елементу - імені
    :param contacts: Словник контактів
    :return: Повідомлення про результат операції
    """
    if len(args) != 1:
        raise IndexError("Command requires exactly 1 argument (name).")
    name = args[0]
    record = contacts.find(name)
    if record:
        return f"{name}: {', '.join(phone.value for phone in record.phones)}"
    else:
        raise KeyError("Contact not found.")


@input_error
def show_all(contacts):
    """
    Показує всі збережені контакти.

    :param contacts: Словник контактів
    :return: Повідомлення з усіма контактами
    """
    if contacts:
        return str(contacts)
    else:
        return "No contacts found."


def main():
    """
    Основна функція програми, що управляє основним циклом обробки команд.
    """
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "help":
            print("Available commands: hello, add, change, phone, all, close, exit")
        else:
            print("Invalid command. Type 'help' to see the list of available commands.")

if __name__ == "__main__":
    main()