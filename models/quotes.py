from .database import sql_write, sql_select
from flask import request, session
from dotenv import load_dotenv, find_dotenv

import os
import bcrypt
import cloudinary
import cloudinary.uploader


env_file = find_dotenv(".env")
load_dotenv(env_file)

CLOUDINARY_CLOUD = os.environ.get('CLOUDINARY_CLOUD')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')


cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
)

def insert_quote():
    user_id = session.get('user_id')

    content = request.form.get('content')
    mood = request.form.get('mood')
    image_url = request.files['image']

    #upload to cloudinary
    response = cloudinary.uploader.upload(image_url, filename=image_url.filename)
    image_url = response['secure_url']

    return sql_write('INSERT INTO quotes(content, image_url, mood, user_id) VALUES (%s, %s, %s, %s)', [content, image_url, mood, user_id])

def render_quotes():
    results = sql_select('SELECT quotes.id, content, image_url, mood, user_id, name FROM quotes INNER JOIN users ON quotes.user_id = users.id ORDER BY quotes.id DESC')
    
    all_quotes = []

    for row in results:
        id, content, image_url, mood, user_id, name = row
        quote = {'id':id,'content': content, 'image_url': image_url, 'mood' : mood, 'user_id': f'{user_id}', 'name': name}
        all_quotes.append(quote)

    return all_quotes

def select_one_quote(id):
    results = sql_select('SELECT id, content, user_id from quotes WHERE id = %s', [id])

    for row in results:
        id, content, user_id = row
        quote = {'id': id,'content': content, 'user_id': f'{user_id}'}
    return quote

def delete_one_quote(id):
    return sql_write('DELETE FROM quotes WHERE id = %s', [id])

def edit_one_quote(id):
    content = request.form.get('content')
    mood = request.form.get('mood')
    image_url = request.files['image']

    #upload to cloudinary
    response = cloudinary.uploader.upload(image_url, filename=image_url.filename)
    image_url = response['secure_url']

    return sql_write('UPDATE quotes SET content = %s, image_url = %s, mood= %s WHERE id = %s', [content, image_url, mood, id])
    
def get_user(email):
    results = sql_select('SELECT id, name, email, password, avatar, isAdmin, description FROM users WHERE email = %s', [email])
    if results == []:
        user = []
    else:
        for row in results:
            id, name, email, password, avatar, isAdmin, description = row
            user = [id, name, email, password, avatar, isAdmin, description]
    return user

def check_log_in():
    email = request.form.get('email')
    password = request.form.get('password')
    user = get_user(email) #get info from sql
    if user == []:
        return user
    else:
        valid = bcrypt.checkpw(password.encode(), user[3].encode()) #check pw input hash with data
        if not valid:
            return 'Invalid Password'
        else:
            return user

def check_sign_up():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password') 
    avatar = request.files['avatar']
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    response = cloudinary.uploader.upload(avatar, filename=avatar.filename)
    avatar = response['secure_url']

    all_emails = []

    results = sql_select('SELECT email FROM users')

    for row in results:
        item = row[0]
        all_emails.append(item)

    if email in all_emails:
        return 'Email has been used'
    else:
        return sql_write('INSERT INTO users (name, email,  password, avatar) VALUES (%s, %s, %s, %s)', [name, email, password_hash, avatar])

def render_user_quotes():
    user_id = session.get('user_id')
    results = sql_select('SELECT quotes.id, image_url, content FROM quotes INNER JOIN users ON quotes.user_id = users.id WHERE quotes.user_id = %s',[user_id])
    all_quotes = []
    for row in results:
        id, image_url, content = row
        quote = {'id': id, 'image_url': image_url,'content': content}
        all_quotes.append(quote)
    return all_quotes

def change_profile_info(user_id):
    name = request.form.get('name')
    description = request.form.get('description')
    editted_avatar = request.files['avatar']

    response = cloudinary.uploader.upload(editted_avatar, filename=editted_avatar.filename)
    
    editted_avatar = response['secure_url']

    return sql_write('UPDATE users SET name = %s, avatar = %s, description = %s WHERE id = %s', [name, editted_avatar, description, user_id])

def set_cookie_session(user):
    session['user_id'] = f'{user[0]}'
    session['user_name'] = user[1]
    session['user_email'] = user[2]
    session['user_avatar'] = user[4]
    session['user_isAdmin'] = user[5]
    session['user_description'] = user[6]


def get_cookie():

    user_name = session.get('user_name', 'Unknown')
    user_avatar = session.get('user_avatar', 'Unknown')
    user_id = session.get('user_id', 'Unknown')
    user_email = session.get('user_email', 'Unknown')
    user_isAdmin = session.get('user_isAdmin', 'Unknown')
    user_description = session.get('user_description', 'Unknown')
    
    user_cookie = {'user_name': user_name, 'user_avatar': user_avatar, 'user_id': user_id, 'user_email': user_email, 'user_isAdmin': user_isAdmin, 'user_description': user_description}
    
    return user_cookie

def get_profile_user(id):
    results = sql_select('SELECT id, name, email, avatar, description FROM users WHERE id = %s', [id])
    for row in results:
        id, name, email, avatar, description = row
        user = {'id': id, 'name': name, 'email': email, 'avatar': avatar, 'description': description}
        return user

def render_profile_quotes(id):
    results = sql_select('SELECT quotes.id, content, image_url, mood, user_id, name FROM quotes INNER JOIN users ON quotes.user_id = users.id WHERE users.id = %s ORDER BY quotes.id DESC',[id])
    
    all_quotes = []

    for row in results:
        id, content, image_url, mood, user_id, name = row
        quote = {'id':id,'content': content, 'image_url': image_url, 'mood' : mood, 'user_id': f'{user_id}', 'name': name}
        all_quotes.append(quote)

    return all_quotes