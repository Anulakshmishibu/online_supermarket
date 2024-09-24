from flask import Flask,Blueprint,render_template,request,redirect,url_for
from database import *
from flask_mail import Mail, Message
import random
import string
import smtplib
from email.mime.text import MIMEText
admin=Blueprint("admin",__name__)
@admin.route('/ahome')
def ahome():
    return render_template('ahome.html')

@admin.route('/vshops',methods=['post','get'])
def vshops():
    data={}
    s="select * from shops"
    res=select(s)
    data['shops']=res
    if 'action' in request.args:
        action=request.args['action']
        shop_id=request.args['shop_id']
        if action=='Accept':
            s="update login set user_type='shop' where login_id='%s'"%(shop_id)
            update(s)
            s1="update shops set status='updated' where login_id='%s'"%(shop_id)
            update(s1)
        elif action=='Remove':
            t="delete from login where login_id='%s'"%(shop_id)
            delete(t)
            t1="delete from shops where login_id='%s'"%(shop_id)
            delete(t1)
    return render_template('vshops.html',data=data)

@admin.route('/acategory',methods=['get','post'])
def acategory():
    data={}
    if 'submit' in request.form:
        category=request.form['category_name']
        s="insert into product_category values(null,'%s')"%(category)
        insert(s)
    t="select*from product_category "
    data['cat']=select(t)
    if 'action' in request.args:
        action=request.args['action']
        category_id=request.args['category_id']
    else:
        action=None
    if action=='delete':
        m="delete from product_category where category_id='%s'"%(category_id)
        delete(m)
    elif action=='update':
        n="select*from product_category where category_id='%s'"%(category_id)
        data['up']=select(n)
    if 'update' in request.form:
        category_name=request.form['category_name']
        category_id=request.args['category_id']
        m="update product_category set category_name='%s' where category_id='%s'"%(category_name,category_id)
        update(m)
        return redirect(url_for('admin.acategory'))
    return render_template('acategory.html',data=data)

@admin.route('/aproduct')
def aproduct():
    data={}
    if 'action' in request.args:
        category_id=request.args['category_id']
        s= "select* from products where category_id='%s'"%(category_id)
        data['pro']=select(s)
    return render_template('aproduct.html',data=data)

@admin.route('/ausers')
def ausers():
    data={}
    s="select*from order_master inner join shops using(shop_id) inner join users using(user_id)"
    data['user']=select(s)
    return render_template('ausers.html',data=data)


@admin.route('/avcustomers')
def avcustomers():
    data={}
    s="select * from users"
    data['use']=select(s)
    return render_template('avcustomers.html',data=data)