import threading

from sqlalchemy import Column, String

from KratosXBot.modules.sql import BASE, SESSION


class KratosChats(BASE):
    __tablename__ = "kratos_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


KratosChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_kratos(chat_id):
    try:
        chat = SESSION.query(KratosChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_kratos(chat_id):
    with INSERTION_LOCK:
        kratoschat = SESSION.query(KratosChats).get(str(chat_id))
        if not kratoschat:
            kratoschat = KratosChats(str(chat_id))
        SESSION.add(kratoschat)
        SESSION.commit()


def rem_kratos(chat_id):
    with INSERTION_LOCK:
        kratoschat = SESSION.query(KratosChats).get(str(chat_id))
        if kratoschat:
            SESSION.delete(kratoschat)
        SESSION.commit()
