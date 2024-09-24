from flask import Flask,Blueprint,render_template,request,redirect,url_for,session,flash
from database import*
from flask_mail import Mail, Message
import random
import string
import smtplib
from email.mime.text import MIMEText
public=Blueprint("public",__name__)

@public.route('/')
def home():

    return render_template('index.html')

@public.route('/login',methods=['post','get'])
def login():
    if 'submit' in request.form:
        uname=request.form['username']    
        passw=request.form['password']
        s="select*from login where username='%s' and password='%s'"%(uname,passw)
        res=select(s)
        session['lid']=res[0]['login_id']
        if res:
            if res[0]['user_type']=='admin':
                return redirect(url_for('admin.ahome'))
            
            elif res[0]['user_type']=='user':
                s2="select* from users where login_id='%s'"%(session['lid'])
                res2=select(s2)
                if res2:
                    session['uid']=res2[0]['user_id']

                return redirect(url_for('user.uhome'))
            elif res[0]['user_type']=='worker':
                n="select*from deliveryboy where login_id='%s'"%(session['lid'])
                res2=select(n)
                if res2:
                    session['wid']=res2[0]['dboy_id']
                return redirect(url_for('worker.whome'))
            elif res[0]['user_type']=='shop':
                s="select*from shops where login_id='%s'"%(session['lid'])
                res1=select(s)
                if res1:
                    session['sid']=res1[0]['shop_id']
                return redirect(url_for('shop.shome'))
            else:
                return "<sript>alert</script>"
        else:
            return redirect(url_for('public.login'))
    return render_template('login.html')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@public.route('/uregister',methods=['post','get'])
def uregister():
    if request.method == 'POST':
        if 'submit' in request.form:
            fname = request.form['first_name']
            lname = request.form['last_name']
            hname = request.form['house_name']
            place = request.form['place']
            lmark = request.form['landmark']
            pcode = request.form['pincode']
            
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']

            # Generate OTP
            otp = generate_otp()

            # Send OTP to the user's email
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

                msg = MIMEText(f'Your OTP for registration is {otp}')
                msg['Subject'] = 'Your OTP for Registration'
                msg['To'] = email
                msg['From'] = 'hariharan0987pp@gmail.com'

                gmail.send_message(msg)
                gmail.quit()

                flash('An OTP has been sent to your email. Please enter it to complete your registration.')
            except smtplib.SMTPException as e:
                print("Couldn't send email: " + str(e))
                flash("Failed to send OTP. Please try again.")
                return redirect(url_for('public.uregister'))

            # Temporarily store user details and OTP in session
            session['user_details'] = {
                'first_name': fname,
                'last_name': lname,
                'house_name': hname,
                'place': place,
                'landmark': lmark,
                'pincode': pcode,
                
                'phone': phone,
                'email': email,
               
                'password': password
            }
            session['otp'] = otp

            return redirect(url_for('public.verify_otp'))

    return render_template('uregister.html')


@public.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if 'verify' in request.form:
            entered_otp = request.form['otp']
            if entered_otp == session.get('otp'):
                user_details = session.get('user_details')
                if user_details:
                    fname=user_details['first_name']
                    lname=user_details['last_name']
                    hname=user_details['house_name']
                    place=user_details['place']
                    lmark=user_details['landmark']
                    pcode=user_details['pincode']
                    phone=user_details['phone']
                    email=user_details['email']
                    passw=user_details['password']
                    d="insert into login values(null,'%s','%s','user')"%(email,passw)
                    login_id=insert(d)
                    s="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(login_id,fname,lname,hname,place,lmark,pcode,phone,email)
                    insert(s)

                    flash("Successfully Registered. Login Now!")
                    session.pop('user_details', None)
                    session.pop('otp', None)
                    return redirect(url_for('public.login'))
            else:
                flash('Invalid OTP. Please try again.')

    return render_template('verify_otp.html')

@public.route('/wregister',methods=['get','post'])
def wregister():
    if 'submit' in request.form:
        fname=request.form['fname'] 
        lname=request.form['lname']
        place=request.form['place']
        email=request.form['email']
        phn=request.form['phone']
        passw=request.form['password']
        t="insert into login values (null,'%s','%s','worker')"%(email,passw)
        login_id=insert(t)
        s="insert into deliveryboy values(null,'%s','%s','%s','%s','%s','%s')"%(login_id,fname,lname,place,email,phn)
        insert(s)
    return render_template('wregister.html')

@public.route('/sregister',methods=['get','post'])
def sregister():
    if 'submit' in request.form:
        sname=request.form['shop_name']
        place=request.form['place']
        lmark=request.form['landmark']
        phone=request.form['phone']
        email=request.form['email']
        passw=request.form['password']  
        s="insert into login values(null,'%s','%s','pending')"%(email,passw)
        login_id=insert(s)
        t="insert into shops values(null,'%s','%s','%s','%s','%s','%s','pending')"%(login_id,sname,place,lmark,phone,email)
        insert(t)
    return render_template('sregister.html')