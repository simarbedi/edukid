from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime
import Caption_it

with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
db = SQLAlchemy(app)
result_dic={}
local_server = True


class Events(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.String(12), nullable=True)


class Captions(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    img_file = db.Column(db.String(12), nullable=True)
    caption = db.Column(db.String(120), nullable=False)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']



@app.route("/")
def home():
    events = Events.query.filter_by().first()
    return render_template('index2.html',events=events)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/events")
def events():
    events = Events.query.filter_by().all()[0:params['no_of_posts']]

    return render_template('events.html', params=params, events=events)

@app.route("/gallery",methods=['GET','POST'])
def gallery():
    captions = Captions.query.filter_by().all()

    if request.method == 'POST':
        f = request.files['userfile']
        path = "./static/{}".format(f.filename)# ./static/images.jpg
        f.save(path)

        caption = Caption_it.caption_this_image(path)

        result_dic = {
        'image' : path,
        'caption' : caption
        }
        entry = Captions(user="simar",img_file=path,caption=caption)
        db.session.add(entry)
        db.session.commit()
        return render_template('gallery.html', params=params, your_result =result_dic, captions=captions)
    return render_template('gallery.html', params=params, captions=captions)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', params=params)


app.run(debug = False, threaded = False)

# @app.route("/contact")
# def contact():
#     return render_template('contact.html', params=params)





# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]

# local_server = True
# app = Flask(__name__)
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD=  params['gmail-password']
# )
# mail = Mail(app)
# if(local_server):
#     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# db = SQLAlchemy(app)


# class Contacts(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     phone_num = db.Column(db.String(12), nullable=False)
#     msg = db.Column(db.String(120), nullable=False)
#     date = db.Column(db.String(12), nullable=True)
#     email = db.Column(db.String(20), nullable=False)


# class Posts(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     slug = db.Column(db.String(21), nullable=False)
#     content = db.Column(db.String(120), nullable=False)
#     tagline = db.Column(db.String(120), nullable=False)
#     date = db.Column(db.String(12), nullable=True)
#     img_file = db.Column(db.String(12), nullable=True)

# @app.route("/")
# def home():
#     posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
#     return render_template('index.html', params=params, posts=posts)



# @app.route("/post/<string:post_slug>", methods=['GET'])
# def post_route(post_slug):
#     post = Posts.query.filter_by(slug=post_slug).first()
#     return render_template('post.html', params=params, post=post)

# @app.route("/about")
# def about():
#     return render_template('about.html', params=params)
