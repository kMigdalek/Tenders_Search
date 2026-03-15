import requests
from unidecode import unidecode
import datetime
import calendar
import pandas as pd

class Tender():

    discount = 0


    def __init__(self, id, title, date, description, value):
        self.id = id
        self.title = unidecode(title)
        self.date = date
        self.description = unidecode(description)
        self.value = value

    @classmethod
    def set_discount_class(cls, discount):
        cls.discount = int(discount)

    def apply_discount(self):
        split_value = self.value.split(' ')
        self.value = str(round(float(split_value[0]) * ((100 - self.discount)/100), 2))

    @property
    def is_day(self):
        return calendar.day_name[datetime.datetime.strptime(self.date, '%Y-%m-%d').weekday()]

my_tender_list = []





def first_page():
     while True:
        user_input = input('\nDo you want to see Poland Tenders? Yes/No: ').lower()
        if user_input == 'no':
            print('\nOkay, bye bye\n')
            break
        elif user_input == 'yes':
            print('\nok, welcome')
            choose_page()
            break
        else: 
            print('\nI do not understand')
            continue






def menu():
    print('\nMENU:')   
    print('1. Poland Tender List')
    print('2. My Tender list')
    print('3. Export/import csv My Tender List')
    print('4. Quit')

    while True:
        user_input = input('\nInput option number: ').lower()
        try:
            if  int(user_input) == 1:
                choose_page()
                break
            elif int(user_input) == 2:
                my_tender_list_menu()
                break
            elif int(user_input) == 3: 
                csv_menu()
                break
            elif int(user_input) == 4: 
                print('\nbye bye!\n')
                break
            else: 
                print('\nProvided value is incorrect')
        except ValueError:
            print('\nCould you repeat?')
            continue






def choose_page():
    while True:
        user_input = input('\nChoose page from 1 to 99 or write "menu" to move to the menu: ').lower()
        try:
            if  1 <= int(user_input) <= 99:
                page_print(user_input)
                break
            else: 
                print('\nProvided value is incorrect')
                continue
        except ValueError:
            if user_input.lower() == 'menu':
                menu()
                break
            else: 
                print('\nCould you repeat?')
                continue









def page_print(page):
    print('\nPlease find the polish tender list\n')

    payload = {'page': page}
    r = requests.get('https://tenders.guru/api/pl/tenders', params=payload)
    r_dict = r.json()
    x = 1
    tender_list = []

    for group in r_dict['data']:
        print(str(x) + '. ' + unidecode(group['title']))
        tender_list.append(group['id'])
        x += 1
    
    print('\n')
    while True:
        user_input = input('\nChoose number of transaction if you want to see details or write "back" to move to the previous page: ').lower()
        try:
            if  1 <= int(user_input) <= 100:
                r = requests.get(f'https://tenders.guru/api/pl/tenders/{str(tender_list[int(user_input) - 1])}')
                r_dict = r.json()
                searching_tender = Tender(r_dict['id'], r_dict['title'], r_dict['date'], r_dict['description'], r_dict['awarded_value'])
                print('\n')
                print('ID :' + searching_tender.id)
                print('TITLE :' + unidecode(searching_tender.title))
                print('DATE :' + searching_tender.date)
                print('DESCRIPTION :' + unidecode(searching_tender.description))
                print('VALUE :' + searching_tender.value + ' PLN')
                single_tender_managment(searching_tender)
                break
            else: 
                print('\nProvided value is incorrect')
                continue
        except ValueError:
            if user_input.lower() == 'back':
                choose_page()
                break
            else: 
                print('\nCould you repeat?')
                continue






def single_tender_managment(tender):
    while True:
        user_input = input('\nDo you want to add the tender to your tender list? Yes/No: ').lower()
        if user_input == 'yes':
            my_tender_list.append(tender)
            print(f'\nTender number {tender.id} has been added')
            menu()
            break
        elif user_input == 'no':
            choose_page()
            break
        else: 
            print('I do not understand')
            continue
        







def my_tender_list_menu():
    x = 1
    print('\nTHE LIST OF TENDERS')
    if len(my_tender_list) == 0:
        print ('The list of tenders is empty :(')
    for tender in my_tender_list:
        print(str(x) + '. ' + tender.title)
        x += 1
    print('\nMENU')
    print('1) details of tender')
    print('2) delete tender')
    print('3) Back to main Menu')
    while True:
        user_input = input('\nInput option number: ')
        try:
            if  int(user_input) == 1:
                tender_preview()
                break
            elif int(user_input) == 2:
                if len(my_tender_list) == 0:
                    print('No tenders to delete')
                    continue
                else:
                    delete_tender()
                    break
            elif int(user_input) == 3: 
                menu()
                break
            else: 
                print('\nProvided value is incorrect')
                continue
        except ValueError:
            print('\nCould you repeat?')
            continue
      






def tender_preview():
    while True:
        user_input = input('\nChoose the tender number you want to preview or write "back" to move to the previous page: ').lower()
        try:
            if 0 < int(user_input) <= len(my_tender_list):
                for i in range(len(my_tender_list)):
                    if int(user_input) == i + 1:
                        print('\n')
                        print('ID :' + str(my_tender_list[int(user_input) - 1].id))
                        print('TITLE :' + str(unidecode(my_tender_list[int(user_input) - 1].title)))
                        print('DATE :' + str(my_tender_list[int(user_input) - 1].date))
                        print('DESCRIPTION :' + str(unidecode(my_tender_list[int(user_input) - 1].description)))
                        print('VALUE :' + str(my_tender_list[int(user_input) - 1].value + ' PLN'))
                        tender_modify(int(user_input))
                        break
                break
            else:
                print('\nProvided value is incorrect') 
                continue           
        except ValueError:
            if user_input == 'back':
                my_tender_list_menu()
                break
            else: 
                print('\nI do not understand')
                continue




def tender_modify(index):
    print('\nMENU:')
    print('1) Check day of the week')
    print('2) Set discount')
    print('3) Back to My Tenders Menu')
    while True:
        user_input = input('\nChoose option: ').lower()
        try:
            if  int(user_input) == 1:
                print(f'\nTender took place on {my_tender_list[index - 1].is_day}')
                tender_modify(index)
                break
            elif int(user_input) == 2:
               set_discount(index)
               break
            elif int(user_input) == 3: 
                my_tender_list_menu()
                break
            else: 
                print('\nProvided value is incorrect')
                continue
        except ValueError:
            print('\nCould you repeat?')
            continue





def delete_tender():
    while True:
        user_input = input('\nChoose the tender number you want delete or write "back" to move to the previous page: ').lower()
        try:
            if 0 < int(user_input) <= len(my_tender_list):
                for i in range(len(my_tender_list)):
                    if int(user_input) == i + 1:
                        del my_tender_list[i]
                        print(f'\nTender number {i + 1} has been deleted')
                        my_tender_list_menu()
                        break
                break
            else:
                print('\nProvided value is incorrect') 
                continue           
        except ValueError:
            if user_input == 'back':
                my_tender_list_menu()
                break
            else: 
                print('\nI do not understand')
                continue



def set_discount(index):
    while True:
        user_input = input('\nWrite the percent number you want to discount the value or write "back" to move to the previous page: ').lower()
        try:
            if 1 <= int(user_input) <= 100:
                Tender.set_discount_class(user_input)
                my_tender_list[index - 1].apply_discount()
                print(f'\nThe discount {user_input}% has been applied, the new value is {my_tender_list[index - 1].value} PLN')
                tender_modify(index)
                break
            else:
                print('\nProvided value is incorrect') 
                continue           
        except ValueError:
            if user_input == 'back':
                my_tender_list_menu()
                break
            else: 
                print('\nI do not understand')
                continue







def csv_menu():
    print('\nCSV MENU:')
    print('1) Export CSV')
    print('2) Import csv')
    print('3) Back to menu')
    
    while True:
        user_input = input('\nChoose option: ').lower()
        try:
            if  int(user_input) == 1:
                export_csv()
                break
            elif int(user_input) == 2:
                import_csv()
                
                break
            elif int(user_input) == 3: 
                menu()
                break
            else: 
                print('\nProvided value is incorrect')
                continue
        except ValueError:
            print('\nCould you repeat?')
            continue



        
def export_csv():
    tenders_dict = []
    for tender in my_tender_list:
        tenders_dict.append(tender.__dict__)

    df = pd.DataFrame(tenders_dict)
    df.to_csv('tenders.csv', index=False)

    print('\nYour Tenders List has been saved as tenders.csv')
    menu()




def import_csv():
    my_tender_list.clear()
    df = pd.read_csv('tenders.csv')
    print('\nYour Tenders List has been imported')
    for  index, row in df.iterrows():
        tender = Tender(
            id=row['id'],
            title=row['title'],
            date=row['date'],
            description=row['description'],
            value=str(row['value'])
        )
        my_tender_list.append(tender)
    menu()





first_page()

