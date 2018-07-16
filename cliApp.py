import json
import re

__module__ = 'cli'


class CliApp:
    ACTION_ADD: str = 'add'
    ACTION_EDIT: str = 'edit'
    ACTION_DELETE: str = 'delete'
    ACTION_EXIT: str = 'exit'

    MESSAGE_EXIT: str = 'Bye! :)'
    MESSAGE_WELCOME: str = 'Welcome to User Registration System\nPlease, choose an action:\n'

    def __init__(self, config: dict):
        self._actions_msg = "* add user:\t\t\tadd\n* edit user:\t\tedit\n* delete user:\t\tdelete\n* exit " \
                            "application:\texit\n"

        self._running = False
        self._data_file = config.get('data_file')

        try:
            with open(self._data_file, 'rt') as json_file:
                self._data_list = json.load(json_file)
        except FileNotFoundError as error:
            print('Error loading data file "{0}": {1}'.format(config.get('data_file'), error.strerror))
            exit(1)
        except json.decoder.JSONDecodeError:
            print('Error parsing JSON data: file is corrupted or incorrect format')
            exit(1)

    def run(self):
        self._running = True

        print(CliApp.MESSAGE_WELCOME)

        while self._running:
            print(self._actions_msg)
            user_input: str = input().strip()

            if user_input == CliApp.ACTION_ADD:
                self.add_user()

            elif user_input == CliApp.ACTION_EDIT:
                self.edit_user()

            elif user_input == CliApp.ACTION_DELETE:
                self.delete_user()

            elif user_input == CliApp.ACTION_EXIT:
                self.exit()

            if user_input == (CliApp.ACTION_ADD or CliApp.ACTION_EDIT or CliApp.ACTION_DELETE):
                self.ask_continue()

    def ask_continue(self):
        print("Do you want to continue?[Y/n]")
        user_input = input().strip()
        if user_input == 'n':
            self.exit()

    @staticmethod
    def email_validation(message):
        while True:
            try:
                regex = re.compile(r'(?P<email>[a-z\d][a-z\d._+]*@(?P<domain>(?:[a-z\d](?:-?[a-z\d]+)+\.)+[a-z]{2,}))')
                email = input(message).strip()
                match = re.fullmatch(regex, email)
                if not match:
                    print('Entered email format is invalid. Please enter valid email')
                else:
                    return match.group('email')
            except ValueError:
                break

    def number_validation(self, message):
        while True:
            try:
                phone_number = int(input(message).strip())
            except ValueError:
                print('The entered number is incorrect. Please enter valid phone number.')
            else:
                return phone_number

    def add_user(self):
        first_name = input("Type in first name: ").strip()
        last_name = input("Type in last name: ").strip()
        email = self.email_validation("Type in email: ")
        phone_number1 = self.number_validation("Type in main phone number: ")
        phone_number2 = self.number_validation("Type in additional phone number: ")
        comments = input("Type in any comments: ").strip()

        keys = ["firstName", "lastName", "email", "mainPhoneNumber", "additionalPhoneNumber", "comments"]
        values = [first_name, last_name, email, phone_number1, phone_number2, comments]
        self._data_list.append(dict(zip(keys, values)))

        with open("data.json", "w") as json_file:
            json.dump(self._data_list, json_file, indent=2)

    def edit_user(self):
        email = input("Type in email of user you want to edit: ").strip()
        for user in self._data_list:
            if user['email'] == email:
                first_name = input("Type in first name: ").strip()
                last_name = input("Type in last name: ").strip()
                phone_number1 = self.number_validation("Type in main phone number: ")
                phone_number2 = self.number_validation("Type in additional phone number: ")
                comments = input("Type in any comments: ").strip()

                user['firstName'] = first_name
                user['lastName'] = last_name
                user['mainPhoneNumber'] = phone_number1
                user['additionalPhoneNumber'] = phone_number2
                user['comments'] = comments

                print('The chosen user was updated successfully')

                with open("data.json", "w") as json_file:
                    json.dump(self._data_list, json_file, indent=2)

                break
        else:
            print("No user was found")

    def delete_user(self):
        email = input("Type in email of user you want to delete: ").strip()

        for user in self._data_list:
            if user['email'] == email:
                self._data_list.remove(user)
                print("The chosen user was deleted successfully")

                with open("data.json", "w") as json_file:
                    json.dump(self._data_list, json_file, indent=2)

                break
        else:
            print("No user was found")

    def exit(self):
        print(CliApp.MESSAGE_EXIT)
        self._running = False
