from flask import Flask
from public import public
from user import user
from shop import shop
from worker import worker
from admin import admin
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

app=Flask(__name__)
app.secret_key="abc"
app.register_blueprint(public)
app.register_blueprint(user)
app.register_blueprint(shop)
app.register_blueprint(worker)
app.register_blueprint(admin)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
app.run(debug=True,port=5009)