import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_id, get_user_by_name, get_user_by_email, create_user, get_all_quotes, get_all_quotes_for, get_quote, search_by_user_or_email, create_quote, delete_quote

# '''
# USAGE:        db.<function_name>
# EXAMPLES:     db.search_by_user_or_email('Smith')
#               db.search_by_user_or_email('gmail.com')
# '''

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

def is_blank(name, field):
    if len(field) == 0:
        flash('{} cannot be blank'.format(name))
        return True
    return False

@app.route('/')
def index():
    quotes = get_all_quotes()
    return render_template('index.html', all_quotes=quotes)

@app.route('/create_quote', methods=['POST'])
def write_quote():
    user = get_user_by_id(session['user_id'])
    content = request.form['html_content']
    create_quote(user.id,content)
    return redirect(url_for('index'))

@app.route('/delete/<quote_id>')
def remove_quote(quote_id):
    delete_quote(quote_id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    return redirect(url_for('search_users', query=request.args['html_query']))
    
@app.route('/results/<query>')
def search_users(query):
    users = search_by_user_or_email(query)
    return render_template('search.html', results=users)

@app.route('/user/<user_id>')
def user_quotes(user_id):
    quotes=get_all_quotes_for(user_id)
    return render_template('quote.html', all_quotes=quotes)

@app.route('/authenticate/<type>')
def authenticate(type):
    if type == 'login':
        return render_template('login.html')
    elif type == 'register':
        return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['html_fullname']
    email = request.form['html_email']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    is_valid = True

    is_valid = not is_blank('fullname', fullname)
    is_valid = not is_blank('email', email)
    is_valid = not is_blank('password', password)
    is_valid = not is_blank('confirm', confirm)

    if password != confirm:
        flash('password not match')
        is_valid = False
    if len(password) < 6:
        flash('pass to short')
    if not EMAIL_REGEX.match(email):
        flash('email is not right format')
    
    if is_valid:
        try:
            user = create_user(email, fullname, password)
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))
        except:
            flash('email already registered dude')
    
    return redirect(url_for('authenticate', type='register'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['html_email']
    password = request.form['html_password']

    try:
        user = get_user_by_email(email)
        
        if password == user.password:
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            flash('Password not match')
    except:
        flash('Invalid login')

    return redirect(url_for('authenticate', type='login'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def setup_web_session(user):
    pass


app.run(debug=True)