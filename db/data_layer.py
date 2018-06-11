from sqlalchemy import or_, and_, desc
from db.base import DbManager
from db.models import User, Quote

def get_all_quotes():
    db = DbManager()
    return db.open().query(Quote).order_by(desc(Quote.created_at)).all()

def get_all_quotes_for(user_id):
    db = DbManager()
    return db.open().query(Quote).order_by(desc(Quote.created_at)).filter(Quote.user_id == user_id).all()

def get_quote(quote_id):
    try:
        db = DbManager()
        return db.open().query(Quote).filter(Quote.id == quote_id).one()
    except:
        pass

def search_by_user_or_email(query):
    try:
        db = DbManager()
        return db.open().query(User).filter(or_(User.name.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()
    except:
        pass

def create_quote(user_id, content):
    try:
        db = DbManager()
        quote = Quote()
        quote.user_id = user_id
        quote.content = content
        return db.save(quote)
    except:
        pass

def delete_quote(quote_id):
    try:
        db = DbManager()
        quote = db.open().query(Quote).filter(Quote.id == quote_id).one()
        return db.delete(quote)
    except:
        pass

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_name(name):
    db = DbManager()
    return db.open().query(User).filter(User.name == name).one()

def get_user_by_email(email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()

def create_user(email, name, password):
    db = DbManager()
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)