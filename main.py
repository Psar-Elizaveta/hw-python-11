from collections import UserDict
from datetime import datetime, date
import string

class NameTooShortError(Exception):
    pass

class NameTooLongError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
        
        
    def __str__(self):
        return str(self.__value)
        
        
    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value
        
        
class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        if len(name) < 3:
            raise NameTooShortError('Name is too short, need more than 3 symbols. Try again.')
        if len(name) > 10:
            raise NameTooLongError('Name is too long, need only 10 symbols. Try again.')
    
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        
        
    @Field.value.setter
    def value(self, value: str):
        # self.__value = datetime.strptime(value, '%Y, %m, %d').date()
        if value is not None:
            self.__value = datetime.strptime(value, '%Y, %m, %d').date()


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        self.__value = value 
        if len(self.__value) != 10 or not self.__value.isdigit():
            raise ValueError('Invalid phone number')
        
        
class Record:
    def __init__(self, name, birthday_value=None):
        self.name = Field(name)
        self.birthday = Birthday(birthday_value)
        self.phones = []
        
        
    def __str__(self) -> str:
        return f'Contact name: {self.name.value}, phones: {";".join(str(p) for p in self.phones)}'
    
    
    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        # phone.validation(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)


    def remove_phone(self, phone):
        for ph in self.phones:
            if isinstance(ph, Field) and ph.value == phone:
                self.phones.remove(ph)


    def find_phone(self, search_phone):
        for phone in self.phones:
            if isinstance(phone, Field) and phone.value == search_phone:
                return phone
        return None
    
    
    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}"

        
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if old_phone == phone.value:
                self.phones.remove(phone)
                self.phones.append(Phone(new_phone))
                return
        raise ValueError


    def days_to_birthday(self):
        if self.birthday.value is None:
            return 'No contact with this birthday'
        else:
            today = date.today()
            next_birthday = date(today.year, self.birthday.month, self.birthday.day)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)                
            days_to_birthday = (next_birthday - today).days
            return days_to_birthday
        
        
class AddressBook(UserDict):
                                                                                            
    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
            return counter
        
    
    def find(self, search_name):
        for name, phone  in self.data.items():
            if name == search_name:
                return phone
        # return self.data.get(name)
        return None
            
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
                
if __name__ == "__main__":

    book = AddressBook()

    john_record = Record("John", '2006, 01, 12')
    print(john_record)
    john_record.add_phone("1234567890")
    print(john_record)
    john_record.add_phone("5555555555")
    print(john_record)
    print(john_record.days_to_birthday())

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")  

    print(john)  

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  

    book.delete("Jane")
    
    