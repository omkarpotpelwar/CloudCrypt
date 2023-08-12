import struct

import pandas as pd
import string
import os
import  json
from flask import *
import mysql.connector
import numpy as np
from datetime import timedelta
from base64 import  b64encode
#from Crypto.Cipher import ChaCha20
#from Crypto.Random import get_random_bytes
import sys
from PIL import Image
import base64
import io
import re
import PIL.Image
import numpy as np
import random
# from random import *
import secrets
from flask import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readmore")
def readmore():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route('/regback',methods=['POST','GET'])
def regback():

    if request.method=='POST':
        print("gekjhiuth")
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        print(email)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="secure_outsourcing"
        )
        mycursor = mydb.cursor()
        from datetime import datetime
        currentDay = datetime.now().strftime('%d/%m/%Y')
        print(currentDay)
        sql="select * from reg"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('reg.html', msg="email existed")
        if(pwd==cpwd):
            sql = "INSERT INTO reg (name,email,pwd,addr,date) VALUES (%s,%s,%s,%s,%s)"
            val = (name,email,pwd,addr,currentDay)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Sucessfully registered","success")
            return render_template('reg.html', msg="registered successfully")
        else:
            flash("Password and Confirm Password not same")
    return render_template('reg.html',msg="somthing wrong")

@app.route("/dp")
def dp():
    return render_template("dp.html")
@app.route('/dpback',methods=['POST', 'GET'])
def dpback():
    global name, name1
    global r
    if request.method == "POST":

        email = request.form['email']
        password1 = request.form['pwd']
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="secure_outsourcing")
        cursor = mydb.cursor()


        sql = "select * from reg where email='%s' and pwd='%s' and status='Accepted' "% (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        session['email'] = email
        #session['r']=r
        if len(results) > 0:
            print('r')
            # session['user'] = username
            # session['id'] = results[0][0]
            # print(id)
            # print(session['id'])
            flash("Sucessfully Login to the Page", "Success")
            return render_template('dphome.html', msg=results[0][1])

        else:
            flash("Invalid Email/Password", "Danger")
            return render_template('dp.html', msg="Login Failure!!!")

    return render_template('dp.html')

@app.route("/cp")
def cp():
    return render_template("cp.html")


@app.route('/cpback',methods=['POST', 'GET'])
def cpback():
    print("aaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaa")


        username = request.form['email']
        password1 = request.form['pwd']
        if username == 'cp@gmail.com' and password1 == 'cp' :
            return render_template('cphome.html', msg="Login Success")
        else:
            flash("Invalid Email/Password", "Danger")
            return render_template('cp.html', msg="Login Failure!!!")

    return render_template('cp.html')

@app.route("/cphome")
def cphome():
    return render_template("cphome.html")
@app.route("/dphome")
def dphome():
    return render_template("dphome.html")

@app.route("/viewuser")
def viewuser():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from user where status='pending' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    x = x.drop(['ph'], axis=1)
    x = x.drop(['status'], axis=1)

    return render_template("viewuser.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route('/accept/<s1>/<s2>')
def accept(s1=0,s2=''):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    status='Accepted'
    otp = "Your Registration request accepted."
    m="Now you can login into the website."
    email=s2
    mail_content = otp + ' ' + m
    sender_address = 'omkar.potpelwar@moderncoe.edu.in'
    sender_pass = 'Vrockpokey@543'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Secure Outsourcing and Sharing of Cloud Data Using a User-Side Encrypted File System'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update user set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Accepted","Warning")


    return render_template("accept.html",msg="accepted")
@app.route('/reject/<s1>/<s2>')
def reject(s1=0,s2=''):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    status='Rejected'
    otp = "Your Registration request Rejected Due to some issues:"
    m = "Try again."
    email = s2
    mail_content = otp + ' ' + m
    sender_address = 'nagamchenchulakshmi@gmail.com'
    sender_pass = 'lakshmi@506'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Secure Outsourcing and Sharing of Cloud Data Using a User-Side Encrypted File System'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update user set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Rejected","Warning")
    return render_template("reject.html", msg="reject")

@app.route("/viewdp")
def viewdp():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from reg where status='waiting' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    x = x.drop(['status'], axis=1)

    return render_template("viewdp.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route('/accept1/<s1>/<s2>')
def accept1(s1=0,s2=''):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    status='Accepted'
    otp = "Your Registration request accepted."
    m = "Now you can login into the website."
    email = s2
    mail_content = otp + ' ' + m
    sender_address = 'omkar.potpelwar@moderncoe.edu.in'
    sender_pass = 'Vrockpokey@543'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Secure Outsourcing and Sharing of Cloud Data Using a User-Side Encrypted File System'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update reg set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Accepted","Warning")


    return render_template("owneracpt.html",msg="accept")
@app.route('/reject1/<s1>/<s2>')
def reject1(s1=0,s2=''):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    status='Rejected'
    otp = "Your Registration request Rejected Due to some issues:"
    m = "Try again."
    email = s2
    mail_content = otp + ' ' + m
    sender_address = 'nagamchenchulakshmi@gmail.com'
    sender_pass = 'lakshmi@506'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Secure Outsourcing and Sharing of Cloud Data Using a User-Side Encrypted File System'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update reg set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Rejected","Warning")
    return render_template("ownert.html",msg="reject")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route('/upback',methods=['POST','GET'])
def upback():
    print("gekjhiuth")
    if request.method=='POST':
        print("gekjhiuth")
        name=request.form['fname']
        file=request.form['file']




        dd="D:/Secure Outsourcing/text_file/"+file
        f = open(dd, "r")
        data = f.read()

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="secure_outsourcing"
        )
        mycursor = mydb.cursor()
        sql = "select * from upload where fname='%s'"%(name)
        result = pd.read_sql_query(sql, mydb)
        fname1 = result['fname'].values
        #prm1 = result['sname'].values

        if name in fname1:
            flash("File with this name already exists","danger")
            return render_template('upload.html')
        else:
            from datetime import datetime
            import datetime

            x = datetime.datetime.now()
            otp = random.randint(000000, 999999)
            skey = secrets.token_hex(4)
            print("secret key",skey)
            # currentDay = datetime.now().strftime('%d/%m/%Y')

            email = session.get('email')
            sql = "INSERT INTO upload (email,fname,file,skey,date) VALUES (%s,%s,AES_ENCRYPT(%s,'lakshmi'),%s,%s)"

            val = (email, name, data,skey,x)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("File uploaded successfully", "Warning")
            print("Successfully Registered")
            return render_template('upload.html', msg="file uploaded successfully")

    return render_template('upload.html',msg="somthing wrong")


@app.route("/viewfile")
def viewfile():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from upload where email='%s'" %(session['email'])
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['file'], axis=1)
    x = x.drop(['email'], axis=1)

    return render_template("viewfile.html", col_name=x.columns.values, row_val=x.values.tolist())


@app.route("/ureg")
def ureg():
    return render_template("ureg.html")

@app.route('/uregback',methods=['POST','GET'])
def uregback():

    if request.method=='POST':
        print("gekjhiuth")
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        print(email)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="secure_outsourcing"
        )
        mycursor = mydb.cursor()
        currentDay = datetime.now().strftime('%d/%m/%Y')
        status='Request'
        print(currentDay)
        sql="select * from user"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('ureg.html', msg="email existed")
        if(pwd==cpwd):
            sql = "INSERT INTO user (name,email,pwd,addr,date) VALUES (%s,%s,%s,%s,%s)"
            val = (name,email,pwd,addr,currentDay)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Sucessfully registered","success")
            return render_template('ureg.html', msg="registered successfully")
        else:
            flash("Password and Confirm Password are not same")
    return render_template('ureg.html',msg="somthing wrong")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/userlog',methods=['POST', 'GET'])
def userlog():
    print("user login page")
    if request.method=='POST':
        print("user login page")
        email = request.form['email']
        password1 = request.form['pwd']
        print('p')

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="secure_outsourcing")
        cursor = mydb.cursor()
        sql = "select * from user where email='%s' and pwd='%s'" % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        session['email'] = email


        if len(results) > 0:
            print('r')
            flash("Sucessfully Login to the Page", "primary")
            return render_template('userhome.html',msg=results[0][1])
        else:
            flash("Invalid Email/Password ", "primary")
            return render_template('user.html')
    return render_template('user.html')

@app.route("/userhome")
def userhome():
    return render_template("userhome.html")

@app.route("/vfiles")
def vfiles():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from upload "
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['file'], axis=1)
    x = x.drop(['skey'], axis=1)
    x = x.drop(['date'], axis=1)

    return render_template("vfile.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/vdata/<s1>/<s2>")
def vdata(s1=0,s2=''):
    print("dfhlksokhso")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
        )
    mycursor = mydb.cursor()

    sql = "select * from upload where id='%s' "%(s1)
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['fname'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['date'], axis=1)
    x = x.drop(['skey'], axis=1)
    x = x.drop(['id'], axis=1)

    return render_template("vdata.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route('/request1/<s1>/<s2>/<s3>')
def request1(s1=0,s2='',s3=''):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    global fname,email,id
    dpemail=s2
    fname=s3
    fid=s1

    currentDay = datetime.now().strftime('%d/%m/%Y')
    mycursor = mydb.cursor()
    status='Request'
    uemail = session.get('email')
    sql = "insert into request(id,email,uemail,fname,date) values(%s,%s,%s,%s,%s)"
    val=(fid,s2,uemail,fname,currentDay,)
    mycursor.execute(sql,val)
    mydb.commit()
    flash("Request sended to the Key Generation Center","Warning")


    return render_template("req.html",msg="request")

@app.route("/au")
def au():
    return render_template("au.html")
@app.route('/auback',methods=['POST', 'GET'])
def auback():
    print("aaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaa")


        username = request.form['email']
        password1 = request.form['pwd']
        if username == 'authority@gmail.com' and password1 == 'authority' :
            flash("Sucessfully Login to the Page", "primary")
            return render_template('auhome.html', msg="Login Success")
        else:
            flash("Invalid Email/Password ", "Danger")
            return render_template('au.html', msg="Login Failure!!!")

    return render_template('au.html')

@app.route("/auhome")
def auhome():
    return render_template("auhome.html")


@app.route("/viewreq")
def viewreq():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from request where status='waiting' "
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)

    x = x.drop(['status'], axis=1)
    x = x.drop(['pkey'], axis=1)
    x = x.drop(['action'], axis=1)

    return render_template("viewreq.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route('/gkey/<s1>/<s2>')
def gkey(s1=0,s2=0):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    global n,fid

    fid=s2
    n=s1
    from random import getrandbits
    import random
    status="Accepted"
    hash=random.getrandbits(20)
    print(hash)

    mycursor = mydb.cursor()
    sql1="update request set status='%s', pkey='%s' where sno = '%s' "%(status,hash,n)
    mycursor.execute(sql1)
    mydb.commit()

    return render_template("gkey.html",msg="accepted")

@app.route("/vr")
def vr():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from request where status='Accepted' "
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)

    x = x.drop(['status'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['action'], axis=1)

    return render_template("vr.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/sendkey/<s1>/<s2>/<s3>")
def sendkey(s1=0, s2='', s3=''):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    global n,m,f
    n=s1
    m=s3
    email=s2
    status='Accepted'
    action="Completed"
    otp="Your secret key is:"

    mail_content = otp + ' ' + m
    sender_address = 'omkar.potpelwar@moderncoe.edu.in'
    sender_pass = 'Vrockpokey@543'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Secure Outsourcing and Sharing of Cloud Data Using a User-Side Encrypted File System'


    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    mycursor = mydb.cursor()
    sql1 = "update request set action='%s' where id='%s'" % (action, n)
    mycursor.execute(sql1)
    mydb.commit()
    return render_template("sku.html",msg="sended")

@app.route("/down")
def down():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    email = session.get('email')

    sql = "select * from request where status='Accepted' and uemail='%s' " %(session['email'])
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['pkey'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['date'], axis=1)
    x = x.drop(['uemail'], axis=1)
    x = x.drop(['action'], axis=1)
    return render_template("down.html", col_name=x.columns.values, row_val=x.values.tolist())


@app.route("/download/<s1>/<s2>")
def download(s1=0,s2=0):
    global g,f1
    g=s1
    f1=s2
    return render_template("download.html",g=g,f1=f1)

@app.route("/downfile",methods=['POST','GET'])
def downfile():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        gkey = request.form['pkey']
        fid = request.form['id']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="secure_outsourcing",
            charset='utf8'
        )
        mycursor = mydb.cursor()
        print(gkey)

        sql = "select count(*),aes_decrypt(file,'lakshmi') from upload,request where request.id='"+fid+"' and upload.id='"+fid+"' and request.pkey='"+gkey+"'"
        x = pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        print(count)
        asss=x.values[0][1]

        print("^^^^^^^^^^^^^")
        if count==0:
            msg="Enter valid key"
            return render_template("down.html",msg=msg)
        if count==1:

            return render_template("hdfs.html", msg=asss)
        print(type(x))
        print(x)


        return render_template("searchback.html", col_name=x.columns.values, row_val=x.values.tolist())
    return render_template("searchback.html")

@app.route("/viewrequest")
def viewrequest():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="secure_outsourcing",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from request where email='%s' " %(session['email'])
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)

    x = x.drop(['status'], axis=1)
    x = x.drop(['pkey'], axis=1)
    x = x.drop(['action'], axis=1)
    x = x.drop(['email'], axis=1)

    return render_template("viewrequest.html", col_name=x.columns.values, row_val=x.values.tolist())


def ChaCha_decrypt_file(key, filename, chunk_size=24 * 1024):
    output_filename = os.path.splitext(filename)[0]
    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        #decryptor = ChaCha20.new(key, ChaCha20.MODE_CBC, iv)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


def ChaCha_encrypt_file(key, filename, chunk_size=64 * 1024):
    output_filename = filename + '.encrypted'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    #encryptor = ChaCha20.new(key, ChaCha20.MODE_CBC, iv)
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(iv)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outputfile.write(encryptor.encrypt(chunk))


if __name__ == "__main__":
    app.run(debug=True)
