from api import db, User, Chat, Message


def get_chat(chat_id=None, to_dict=True):
    if chat_id is not None:
        chat = db.session.query(Chat).get(chat_id)
        if chat is None:
            return None
        return chat.to_dict() if to_dict else chat
    return [item.to_dict() if to_dict else item for item in db.session.query(Chat).all()]


def create_chat(name):
    chat = Chat()
    chat.name = name

    db.session.add(chat)
    db.session.commit()
    return chat


def add_user(user_id, chat_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    chat = db.session.query(Chat).get(chat_id)
    if chat is None:
        raise IndexError(f"Чат с id {chat_id} не найден")
    chat.users.append(user)
    user.chats.append(Chat)

    db.session.commit()


def add_message(user_id, chat_id, message):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    chat = db.session.query(Chat).get(chat_id)
    if chat is None:
        raise IndexError(f"Чат с id {chat_id} не найден")
    if chat not in user.chats:
        raise IndexError(f"Пользователь {user_id} не в {chat_id} чате")
    msg = Message(contnet=message)
    db.session.add(msg)
    chat.messages.append(msg)
    db.session.commit()


def get_chat_messages(chat_id):
    chat = db.session.query(Chat).get(chat_id)
    if chat is None:
        raise IndexError(f"Чат с id {chat_id} не найден")
    return [i.to_dict() for i in chat.messages]
