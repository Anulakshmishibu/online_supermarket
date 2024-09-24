from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from database import*
user=Blueprint("user",__name__)

@user.route('/uhome')
def uhome():
    return render_template('uhome.html')

@user.route('/ushops')
def ushops():
    data={}
    s="select * from shops where status='updated' "
    data['shops']=select(s)
    return render_template('ushops.html',data=data)

@user.route('/uproducts',methods=['get','post'])
def uproducts():
    data={}
    if 'search' in request.form:
        productname=request.form['search'] +"%"
        n="select*from products inner join product_category using(category_id) where product_name like'%s'"%(productname)
        print("/////////////////////////",n)
        data['pro']=select(n)
    else:
        n="select*from products inner join product_category using(category_id)"
        data['pro']=select(n)
    # return redirect(url_for('user.uproducts'))
    return render_template('uproducts.html',data=data)

@user.route('/ucart',methods=['get','post'])
def ucart():
    data={}
    if 'submit' in request.form:
        product_name=request.form['product_name']
        amount=request.form['amount']
        quantity=request.form['quantity']
        total=request.form['total']
        product_id=request.args['product_id']
        shop_id=request.args['shop_id']
        print("mjjjjjjjjjjjjj",session['uid'])
        w="select * from order_master where user_id='%s' and status='pending'"%(session['uid'])
        res=select(w)
        print('res is ',res)
       
        if res:
            om_id=res[0]['order_master_id']
            m="update order_master set total='%s' + total where order_master_id='%s'"%(total,om_id)
            update(m)
            
            
        else:
            r="insert into order_master values(null,'%s','%s',curdate(),'%s','pending')"%(session['uid'],shop_id,total)
            om_id=insert(r)
           
        se="select * from order_details where product_id='%s' and order_master_id='%s'"%(product_id,om_id)
        res1=select(se)
        
        if res1:
            omdetails=res1[0]['order_details_id']
            print(quantity,'quantity is ')
            print(quantity,'quantity is ')

            t="update order_details set quantity='%s'+quantity , amount='%s' where order_details_id='%s'"%(quantity,amount,omdetails)
            update(t)
        else:
            n="insert into order_details values(null,'%s','%s','%s','%s')"%(om_id,product_id,quantity,amount)
            insert(n)
    product_id=request.args['product_id']
    s="SELECT * FROM products WHERE products.product_id='%s'"%(product_id)
    data['pro']=select(s)
    return render_template('ucart.html',data=data)


@user.route('/vucart')
def vucart():
    data={}
    s="select* from order_master where user_id='%s'"%(session['uid'])
    data['cart']=select(s)
    
    return render_template('vucart.html',data=data)

@user.route('/payment',methods=['get','post'])
def payment():
    data={}
    if 'btn' in request.form:
        
        om_id=request.args['order_master_id']
        total=request.args['total']
        s="insert into payment values(null,'%s',curdate(),'%s')"%(om_id,total)
        insert(s)
        e="select*from payment"
        data['res']=select(e)
        n="update order_master set status='paid' where order_master_id='%s'"%(om_id)
        update(n)
        return redirect(url_for('user.vucart'))        
    return render_template('payment.html',data=data)


@user.route('/uohistory',methods=['get','post'])
def uohistory():
    data={}
    s="select*from order_details inner join order_master using(order_master_id) inner join products using(product_id) inner join payment on(order_master.order_master_id=payment.order_master_id) where user_id='%s'"%(session['uid'])
    data['his']=select(s)
    return render_template('uohistory.html',data=data)


@user.route('/udelivery')
def udelivery():
    data={}
    om_id=request.args['om_id']
    s="select* from delivery inner join deliveryboy on(delivery.deliveryboy_id=deliveryboy.dboy_id) where order_master_id='%s'"%(om_id)
    data['deli']=select(s)
    return render_template('udelivery.html',data=data)

@user.route('/rating',methods=['get','post'])
def rating():
    data={}
    s="select*from ratings inner join users using(user_id) inner join products on (ratings.product_id=products.product_id) where user_id='%s'"%(session['uid'])
    data['rate']=select(s)
    if 'submit' in request.form:
        product_id=request.args['product_id']
        rate=request.form['rate']
        review=request.form['review']
        n="insert into ratings values(null,'%s','%s','%s','%s',curdate())"%(session['uid'],product_id,rate,review)
        insert(n)
        return redirect(url_for('user.uhome'))
    return render_template('rating.html',data=data)

@user.route('/vratings')
def vratings():
    data={}
    product_id=request.args['product_id']
    s="select*from ratings inner join users using(user_id) inner join products on (ratings.product_id=products.product_id) where products.product_id='%s' order by rate"%(product_id)
    data['rate']=select(s)
    return render_template('vratings.html',data=data)

@user.route('/ucomplaint',methods=['get','post'])
def ucomplaint():
    data={}
    s="select* from complaints where user_id='%s'"%(session['uid'])
    data['com']=select(s)
    if 'submit' in request.form:
        comp=request.form['complaint']
        n="insert into complaints values(null,'%s','%s','pending',curdate())"%(session['uid'],comp)
        insert(n)
        return redirect(url_for('user.uhome'))
    return render_template('ucomplaint.html',data=data)