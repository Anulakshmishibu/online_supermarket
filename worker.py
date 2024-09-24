from flask import Flask,Blueprint,render_template,request,session,redirect,url_for
from database import *
worker=Blueprint("worker",__name__)
@worker.route('/whome')
def whome():
    return render_template('whome.html')

@worker.route('/worders')
def worders():
    data={}
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    s="select*from order_details inner join order_master using(order_master_id) inner join products using(product_id) inner join users using(user_id) inner join product_category using(category_id) where order_master.status='dispatched'"
    data['dis']=select(s)
    if 'action' in request.args:
        print("iiiiiiiiiiiiiiiiiiiiiiiiiii")
        action=request.args['action']
        ogs_id=request.args['order_master_id']

        om_id=request.args['order_details_id']
    else:
        action=None
    if action=='pickup':
        oms_id=request.args['order_master_id']
        k="insert into delivery values(null,'%s','%s','pending')"%(oms_id,session['wid'])
        insert(k)
        print("kiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        n="update order_master inner join order_details using(order_master_id) set status='pickup' where order_details_id='%s'"%(om_id)
        update(n)
        return redirect(url_for('worker.whome'))
    return render_template('worders.html',data=data)


@worker.route('/wpick')
def wpick(): 
    data={}
    # s="select*from order_details inner join order_master using(order_master_id) inner join products using(product_id) inner join users using(user_id)"
    s="SELECT*FROM order_details INNER JOIN order_master USING(order_master_id) INNER JOIN products USING(product_id) INNER JOIN users USING(user_id)INNER JOIN delivery WHERE delivery.status='pending' AND deliveryboy_id='%s'"%(session['wid'])
    data['pick']=select(s)
    if 'action' in request.args:
        action=request.args['action']
        deliy_id=request.args['deliy_id']
    else:
        action=None
    if action=='delivered':
        n="update delivery set status='deliverd' where deliy_id='%s'"%(deliy_id)
        update(n)
        return redirect(url_for('worker.wpick'))
    return render_template('wpick.html',data=data)

@worker.route('/wvorder_details')
def wvorder_details():
    data={}
    om_id=request.args['om_id']
    s="select * from order_details inner join order_master using(order_master_id) inner join products using (product_id) where order_master_id='%s' "%(om_id)
    data['res']=select(s)
    print(s)

    return render_template('wvorder_details.html',data=data)

