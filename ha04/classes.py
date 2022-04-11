class User:
    def __init__(self, login: str, phone: str, email: str):
        self.messages = []
        self.chats = []
        self.__login = login
        self.__phone = phone
        self.__email = email

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login):
        self.__login = login

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email


class Message:
    def __init__(self, user: User, chat, text: str):
        self.__user = user
        self.__chat = chat
        self.__text = text

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def chat(self):
        return self.__chat

    @chat.setter
    def chat(self, chat):
        self.__chat = chat

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text


class Chat:
    def __init__(self, chat_name: str):
        self.name = chat_name
        self.users = []
        self.messages = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def add_user(self, user: User):
        self.users.append(user)

    def add_message(self, message: Message):
        self.messages.append(message)


class Messenger:
    def __init__(self, messenger_name: str):
        self.name = messenger_name
        self.chats = {}
        self.users = []
        self.messages = []

    def add_chat(self, chat_name: str):
        if chat_name not in self.chats:
            new_chat = Chat(chat_name)
            self.chats[chat_name] = new_chat
        else:
            print("ERROR - The chat with such name already exists")

    def registrate_user(self, user: User):
        self.users.append(user)
        print(f"Ok. The user {user.login} is registered in messenger {self.name}")

    def add_user_to_chat(self, user: User, chat_name: str):
        if chat_name not in self.chats:
            print("ERROR - Not exist chat with such name ")
        else:
            self.chats[chat_name].users.append(user)
            if user not in self.users:
                self.users.append(user)
                print(f"Ok. The user {user.login} is registered in messenger {self.name}")
            user.chats.append(self.chats[chat_name])
            print(f'Ok. User {user.login} added in {chat_name}')

    def add_message(self, message_text: str, chat_name: str, user: User):
        if chat_name in self.chats:
            if user in self.chats[chat_name].users:
                new_message = Message(user, chat_name, message_text)
                self.messages.append(new_message)
                self.chats[chat_name].messages.append(new_message)
                user.messages.append(new_message)
                print(f'Ok. Message {message_text} added to chat {chat_name}')
            else:
                print(f"ERROR - User {user.login} not in chat {chat_name}")
        else:
            print(f"ERROR - Not exist chat with name {chat_name}")

    def find_word_in_messages(self, word: str):
        counter = 0
        for mess in self.messages:
            if word in mess.text:
                counter += 1
        print(f'Word: {word} is found in messenger {self.name} - {counter} times')

    def shared_chats(self, *args):
        user_1 = args[0]
        if user_1 in self.users:
            r = set(user_1.chats)
            for user in args[1:]:
                if user in self.users:
                    r = r.intersection(user.chats)
                else:
                    print(f'User {user.login} is not registered in messenger {self.name}')
            print(f'Shared_chats:')
            for chat in r:
                print(chat.name)
        else:
            print(f'User {user_1.login} is not registered in messenger {self.name}')

    @staticmethod
    def compare_messengers(obj1, obj2):
        if (len(obj1.users) != len(obj2.users)) or \
                (len(obj1.chats) != len(obj2.chats)) or \
                (len(obj1.messages) != len(obj2.messages)):
            print(f'Messengers not equal')
            return False
        else:
            print(f'Messengers is equal')
            return True

    @staticmethod
    def get_from_messengers(obj1, obj2, subject: str, item: str):
        set1 = set()
        set2 = set()
        if item == 'phone':
            for user in obj1.users:
                set1.add(user.phone)
            for user in obj2.users:
                set2.add(user.phone)
        elif item == 'email':
            for user in obj1.users:
                set1.add(user.email)
            for user in obj2.users:
                set2.add(user.email)

        if subject == 'intersection':
            result = set1.intersection(set2)
        elif subject == 'difference':
            result = set1.difference(set2)
        elif subject == 'union':
            result = set1.union(set2)
        else:
            result = set()

        return result


if __name__ == '__main__':
    wapp = Messenger('wapp')
    wapp.add_chat("chat_MIPT_SD")
    wapp.add_chat("chat_MIPT_MO")
    wapp.add_chat("chat_MIPT_ML")
    user1 = User('swarm', "+79149453676", "swarm@gmail.com")
    user2 = User('tramp', "+79149462682", "tramp@gmail.com")
    wapp.registrate_user(user1)
    wapp.add_user_to_chat(user1, 'chat_MIPT_SD')
    wapp.add_user_to_chat(user1, 'chat_MIPT_MO')
    wapp.registrate_user(user2)
    wapp.add_user_to_chat(user2, 'chat_MIPT_SD')
    wapp.add_user_to_chat(user2, 'chat_MIPT_ML')

    wapp.add_message('Yes', 'chat_MIPT_SD', user1)
    wapp.add_message('Yes', 'chat_MIPT_SD', user1)
    wapp.add_message('No', 'chat_MIPT_MO', user2)
    wapp.add_message('Yes', 'chat_MIPT_SD', user2)

    wapp.find_word_in_messages('Yes')
    wapp.shared_chats(user1, user2)

    tel = Messenger('tel')
    user3 = User('tank', "+79149462682", "swarm@gmail.com")
    tel.registrate_user(user3)

    Messenger.compare_messengers(wapp, tel)
    Messenger.compare_messengers(wapp, wapp)

    print(Messenger.get_from_messengers(wapp, tel, 'union', 'phone'))
    print(Messenger.get_from_messengers(wapp, tel, 'union', 'email'))
    print(Messenger.get_from_messengers(wapp, tel, 'difference', 'phone'))
    print(Messenger.get_from_messengers(wapp, tel, 'difference', 'email'))
    print(Messenger.get_from_messengers(wapp, tel, 'intersection', 'phone'))
    print(Messenger.get_from_messengers(wapp, tel, 'intersection', 'email'))