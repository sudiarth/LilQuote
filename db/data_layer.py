from sqlalchemy import or_, and_
from db.base import DbManager
from db.models import User

def get_all_quotes():
    db = DbManager()
    return db.open().query(Quote).all()

def get_all_quotes_for(user_id):
    db = DbManager()
    return db.open().query(Quote).filter(Quote.user_id == user_id).all()

def get_quote(quote_id):
    db = DbManager()
    return db.open().query(Quote).filter(Quote.id == quote_id).one()

def search_by_user_or_email(query):
    db = DbManager()
    return db.open().query(User).filter(or_(User.username.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    db = DbManager()
    quote = Quote()
    quote.content = content
    return db.save(quote)

def delete_quote(quote_id):
    db = DbManager()
    quote = db.delete(get_quote(quote_id))
    db.close()
    return quote

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_name(username):
    db = DbManager()
    return db.open().query(User).filter(User.username == username).one()

def get_user_by_email(user_email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()

def create_user(email, username, password):
    db = DbManager()
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)