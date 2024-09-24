from flask import Flask,Blueprint,render_template,request,session,redirect,url_for
import uuid
from database import *
shop=Blueprint("shop",__name__)
@shop.route('/shome')
def shome():
    return render_template('shome.html')

@shop.route('/scategory')
def scategory():
    data={}
    n="select*from product_category"
    data['cat']=select(n)
    return render_template('scategory.html',data=data)

@shop.route('/sproduct',methods=['post','get'])
def sproduct():
    data={}
    s="select*from product_category "
    data['cat']=select(s)
    cat_id=request.args['category_id']
    if 'submit' in request.form:
        product_name=request.form['product_name']
        details=request.form['details']
        price=request.form['price']
        photo=request.files['image']
        path="static/images/"+str(uuid.uuid4())+photo.filename
        photo.save(path)
        s="insert into products values(null,'%s','%s','%s','%s','%s','%s')"%(cat_id,session['sid'],product_name,details,price,path)
        insert(s)
    p="select*from products inner join product_category using (category_id) where category_id='%s'"%(cat_id)
    data['pro']=select(p) 
    if 'action' in request.args:
        action=request.args['action']
        product_id=request.args['product_id']
    else:
        action=None
    if action=='delete':
        m="delete from products where product_id='%s'"%(product_id)
        delete(m)
        return redirect(url_for('shop.sproduct'))
    if action=='update':
        n="select * from products inner join product_category using(category_id) where product_id='%s'"%(product_id)
        data['up']=select(n) 
    if 'update' in request.form:
        product_name=request.form['product_name']
        details=request.form['details']
        price=request.form['price']
        photo=request.files['image']    
        path="static/images/"+str(uuid.uuid4())+photo.filename
        photo.save(path)      
        s="update products set product_name='%s',details='%s',price='%s',image='%s' where product_id='%s'"%(product_name,details,price,path,product_id)
        update(s)  
        return redirect(url_for('shop.sproduct'))      
    return render_template('sproduct.html',data=data)


@shop.route('/svorders')
def svorders():
    data={}
    s="select*from order_details inner join order_master using(order_master_id) where status<>'delivered' and shop_id='%s'"%(session['sid'])
    data['acc']=select(s)
    if 'action' in request.args:
        action=request.args['action']
        om_id=request.args['om_id']
    else:
        action=None
    if action=='acceptorder':
        s="update order_master set status='acceptorder' where order_master_id='%s'"%(om_id)
        update(s)
        return redirect(url_for('shop.svorders'))
    elif action=='viewpayment':
        return redirect(url_for('shop.spayment'))
    return render_template('svorders.html',data=data)

@shop.route('/spayment')
def spayment():
    data={}
    om_id=request.args['om_id']
    s="select*from payment inner join order_master using(order_master_id) where order_master_id='%s'"%(om_id)
    data['ord']=select(s)
    if 'action' in request.args:
        action=request.args['action']
        om_id=request.args['om_id']
    else:
        action=None
    if action=='dispatched':
        n="update order_master set status='dispatched' where order_master_id='%s'"%(om_id)
        update(n)
        return(redirect(url_for('shop.shome')))
    return render_template('spayment.html',data=data)


@shop.route('/svdelivery',methods=['get','post'])
def svdelivery():
    data={}
    s="SELECT*FROM order_master INNER JOIN delivery ON(order_master.order_master_id=delivery.order_master_id) WHERE order_master.status='pickup'"
    data['deli']=select(s)
    if 'action' in request.args:
        action=request.args['action']
        om_id=request.args['om_id']
    else:
        action=None
    if action=='deliverd':
        n="update order_master set status='deliverd' where order_master_id='%s'"%(om_id)
        update(n)
        return redirect(url_for('shop.svdelivery'))
    return render_template('svdelivery.html',data=data)

@shop.route('/srating')
def srating():
    data={}
    s="select*from ratings"
    data['rate']=select(s)
    return render_template('srating.html',data=data)

@shop.route('/svcomplaint')
def svcomplaint():
    data={}
    s="select* from complaints inner join users using(user_id)"
    data['com']=select(s)  
    return render_template('svcomplaint.html',data=data)

@shop.route('/scomplaint',methods=['get','post'])
def scomplaint():
    data={}
    s="select* from complaints"
    data['com']=select(s)  
    if'action' in request.args:
        action=request.args['action']
        user_id=request.args['user_id']
    else:
        action=None
    if action=='reply':
        n="select*from complaints where user_id='%s'"%(user_id)
        data['rep']=select(n)
    if 'reply' in request.form:
        reply=request.form['reply']
        user_id=request.args['user_id']
        d="update complaints set reply='%s' where user_id='%s'"%(reply,user_id)
        update(d)
        return redirect(url_for('shop.svcomplaint'))
    return render_template('scomplaint.html',data=data)
