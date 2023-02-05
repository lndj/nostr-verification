from replit import db


def get_publickey_by_name(name: str) -> str:
    return db.get(name)


def get_name_by_publickey(public_key: str) -> str:
    return db.get(public_key)


def set_publickey_by_name(name: str, public_key: str):
    db[name] = public_key
    db[public_key] = name
