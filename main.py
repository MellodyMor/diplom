import eel
import re,os,copy
from datetime import date
from flask import Flask, request, render_template, session,redirect, jsonify,flash,url_for
import sqlite3
from random import randint, shuffle
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
nomertr = 0
tr = 0
sp = ["/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3']
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

app.config['UPLOAD_FOLDER'] = 'static/img/медальки'  # Папка для сохранения загруженных изображений
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла - 16 MB
app.secret_key = 'supersecretkey'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

awcolor=['static/img/медальки/первая медаль цв.jpg','static/img/медальки/5 трен цв.jpg','static/img/медальки/10 тр цв.jpg']
awblack=['static/img/медальки/первая медаль чб.jpg','static/img/медальки/5 трен чб.jpg','static/img/медальки/10 тр чб.jpg']
@app.route('/pict',methods=['POST'])#pзаменить что и куда это вывод подсет для пользователя
def pict():
    # Получаем данные из тела запроса
    data = request.json
    # Получаем значение из данных
    value = data.get('data')
    print(value)
    img = Image.open(value)
    img = img.convert("L")
    img.show()
    db_lp = sqlite3.connect('pict.db')
    cursor_db = db_lp.cursor()
    sql_insert = '''INSERT INTO color VALUES('{}','{}');'''.format(value,'')
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    global awblack
    awblack.append(value)
    print(awblack)
    return jsonify({'message': 'Данные успешно получены и обработаны'})
@app.route('/get-text',methods=['POST'])#pзаменить что и куда это вывод подсет для пользователя
def pri():
    # Получаем данные из тела запроса
    data = request.json
    # Получаем значение из данных
    value = data.get('data')
    db_lp = sqlite3.connect(session['username']+'.db')
    cursor_db = db_lp.cursor()
    sql_insert = '''INSERT INTO ypr VALUES('{}');'''.format(value)
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    # Делаем что-то с полученным значением, например, выводим его
    print("Получено значение:", value)

    # Возвращаем ответ об успешной обработке запроса
    return jsonify({'message': 'Данные успешно получены и обработаны'})
@app.route('/get-text-tr',methods=['POST'])#pзаменить что и куда это вывод подсет для пользователя
def pri_tr():
    # Получаем данные из тела запроса
    data = request.json
    # Получаем значение из данных
    value = data.get('data')
    db_lp = sqlite3.connect(session['username']+'.db')
    cursor_db = db_lp.cursor()
    sql_insert = '''INSERT INTO tren VALUES('{}');'''.format(value)
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    # Делаем что-то с полученным значением, например, выводим его
    print("Получено значение:", value)

    # Возвращаем ответ об успешной обработке запроса
    return jsonify({'message': 'Данные успешно получены и обработаны'})
@app.route('/process', methods=['POST'])
def process():
    username = request.form["uname"]
    print("Hello {}!".format(username))
@app.route('/logout')#выход
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/')
@app.route('/', methods=['GET', 'POST'])
def q():
    if 'username' not in session:
        return render_template('start.html', m="Вход")
    else:
        return render_template('start.html',m=session['username'])
@app.route('/awards', methods=['GET', 'POST'])
def awards():
    print(session)
    global awblack, awcolor
    st = [""] * len(awblack)
    if session['roll']== "Учитель":
        db_lp = sqlite3.connect('pict.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT color FROM p1")
        color = cursor_db.fetchall()
        cursor_db.execute("SELECT black FROM p1")
        black = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        status = ['0']*len(black)
        st = [""] * len(black)
        sts=''
        for i in range(len(black)):
            if status[i] == '0':
                st[i] = 'static/img/медальки/'+black[i][0]
                sts += 'static/img/медальки/'+black[i][0]+','
            else:
                st[i] = 'static/img/медальки/'+color[i][0]
                sts +='static/img/медальки/'+color[i][0]+','
        print(st)
        if request.method == 'POST':
            return render_template('awards_log_tich.html', m=session['username'], st=sts)
        return render_template('awards_log_tich.html',m=session['username'],st=sts)
    else:
        if 'username' not in session:
            return render_template('awards_log_hb.html',m="Вход")
        Login = session['username']
        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT status FROM awards WHERE login = '{}'; ''').format(Login))
        status = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        print(status[0][0])
        db_lp = sqlite3.connect('pict.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT color FROM p1")
        color = cursor_db.fetchall()
        cursor_db.execute("SELECT black FROM p1")
        black = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        status = status[0][0].split(",")
        st = [""] * len(black)
        sts = ''
        while len(status)<len(black):
            status.append('0')
        for i in range(len(black)):
            if status[i] == '0':
                st[i] = 'static/img/медальки/' + black[i][0]
                sts += 'static/img/медальки/' + black[i][0] + ','
            else:
                st[i] = 'static/img/медальки/' + color[i][0]
                sts += 'static/img/медальки/' + color[i][0] + ','
        print(sts)
        return render_template('awards_log.html',m=session['username'],st=st,sts=sts)
@app.route('/aut_awards', methods=['GET', 'POST'])
def aut_awards():
   if request.method == 'POST':
       Login = request.form.get('Login')
       session['username'] = Login
       Password = request.form.get('Password')
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
       pas = cursor_db.fetchall()
       cursor_db.close()
       try:
           if pas[0][0] != Password:
               return render_template('auth_bad.html')
       except:
           return render_template('auth_bad.html')
       db_lp.close()
       return redirect('/')
   return render_template('index.html')

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')
       session['username'] = Login
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       cursor_db.execute("SELECT login FROM passwords")
       all_login = cursor_db.fetchall()
       if (Login,) not in all_login:
           return redirect("/registration")
       cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
       pas = cursor_db.fetchall()
       cursor_db.close()
       roll_db = db_lp.cursor()
       roll_db.execute(('''SELECT roll FROM passwords 
                                            WHERE login = '{}'; 
                                            ''').format(Login))
       rol = roll_db.fetchall()
       session['roll'] = rol[0][0]
       print(session['roll'])
       roll_db.close()
       try:
           if pas[0][0] != Password:
               return render_template('auth_bad.html', name = "Вход")
       except:
           return render_template('auth_bad.html', name = "Вход")
       return redirect('/')
       db_lp.close()
   return render_template('index.html', name = "Вход")

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        session['username'] = Login
        Password = request.form.get('Password')
        Roll = request.form.get('Roll')
        session['roll']=Roll
        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT INTO passwords VALUES('{}','{}','{}');'''.format(Login, Password, Roll)
        cursor_db.execute(sql_insert)
        db_lp.commit()
        sql_insert = '''INSERT INTO awards VALUES('{}','{}');'''.format(Login, "0,0,0")
        cursor_db.execute(sql_insert)
        db_lp.commit()
        cursor_db.close()
        db_lp.close()
        db_lp = sqlite3.connect(session['username']+'.db')
        cursor_db = db_lp.cursor()
        sql_create = '''CREATE TABLE tren(total TEXT);'''
        cursor_db.execute(sql_create)
        db_lp.commit()
        cursor_db = db_lp.cursor()
        sql_create = '''CREATE TABLE ypr(total TEXT);'''
        cursor_db.execute(sql_create)
        db_lp.commit()
        cursor_db.close()
        db_lp.close()
        return render_template('successfulregis.html')
    return render_template('registration.html')

@app.route('/proba',methods=['GET', 'POST'])
def proba():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        return render_template('2.html')
@app.route('/exit',methods=['GET', 'POST'])
def exit():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        if request.method == 'POST':
            Email = request.form.get('Email')
            db_lp = sqlite3.connect('login_password.db')
            cursor_db = db_lp.cursor()
            global regex
            if (re.fullmatch(regex, Email)):
                sql_insert = '''INSERT INTO Email VALUES('{}','{}');'''.format(session['username'], Email)
                cursor_db.execute(sql_insert)
                db_lp.commit()
                cursor_db.close()
                db_lp.close()
                return render_template('exit_t.html', name=session['username'], message="Спасибо что подписались на нашу рассылку")
            else:
                return render_template('exit.html', name=session['username'], message="неправильно введена почта")
        return render_template('exit.html',name=session['username'],message="")
@app.route('/1',methods=['GET', 'POST'])
def first_task():
    global tr
    if tr == 1:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p1")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT po FROM p1")
        prav_otvet = cursor_db.fetchall()
        cursor_db.execute("SELECT npo FROM p1")
        ne_prav_otvet = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0, len(name)-1)
        r = prav_otvet[t][0]
        nr = ne_prav_otvet[t][0].split(",")
        n = [r, nr[0], nr[1], nr[2]]
        shuffle(n)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM tren")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer += 1
        n1 = "static/img/0.png"
        n2 = "static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1 = "static/img/1.png"
            elif str(nomer)[0] == '2':
                n1 = "static/img/2.png"
            elif str(nomer)[0] == '3':
                n1 = "static/img/3.png"
            elif str(nomer)[0] == '4':
                n1 = "static/img/4.png"
            elif str(nomer)[0] == '5':
                n1 = "static/img/5.png"
            elif str(nomer)[0] == '6':
                n1 = "static/img/6.png"
            elif str(nomer)[0] == '7':
                n1 = "static/img/7.png"
            elif str(nomer)[0] == '8':
                n1 = "static/img/8.png"
            elif str(nomer)[0] == '9':
                n1 = "static/img/9.png"
            if str(nomer)[1] == '0':
                n2 = "static/img/0.png"
            elif str(nomer)[1] == '1':
                n2 = "static/img/1.png"
            elif str(nomer)[1] == '2':
                n2 = "static/img/2.png"
            elif str(nomer)[1] == "3":
                n2 = "static/img/3.png"
            elif str(nomer)[1] == "4":
                n2 = "static/img/4.png"
            elif str(nomer)[1] == "5":
                n2 = "static/img/5.png"
            elif str(nomer)[1] == "6":
                n2 = "static/img/6.png"
            elif str(nomer)[1] == "7":
                n2 = "static/img/7.png"
            elif str(nomer)[1] == "8":
                n2 = "static/img/8.png"
            elif str(nomer)[1] == "9":
                n2 = "static/img/9.png"
        else:
            if nomer == 0:
                n2 = "static/img/0.png"
            elif nomer == 1:
                n2 = "static/img/1.png"
            elif nomer == 2:
                n2 = "static/img/2.png"
            elif nomer == 3:
                n2 = "static/img/3.png"
            elif nomer == 4:
                n2 = "static/img/4.png"
            elif nomer == 5:
                n2 = "static/img/5.png"
            elif nomer == 6:
                n2 = "static/img/6.png"
            elif nomer == 7:
                n2 = "static/img/7.png"
            elif nomer == 8:
                n2 = "static/img/8.png"
            elif nomer == 9:
                n2 = "static/img/9.png"
        #f.close()
        return render_template('play1_tr.html', p=name[t][0], nr=n, n=r,n1=n1,n2=n2, q=q)
    else:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p1")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT po FROM p1")
        prav_otvet = cursor_db.fetchall()
        cursor_db.execute("SELECT npo FROM p1")
        ne_prav_otvet = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0,len(name)-1)
        r = prav_otvet[t][0]
        nr = ne_prav_otvet[t][0].split(",")
        n = [r,nr[0],nr[1],nr[2]]
        shuffle(n)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM ypr")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer+=1
        n1="static/img/0.png"
        n2="static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1="static/img/1.png"
            elif str(nomer)[0] == '2':
                n1="static/img/2.png"
            elif str(nomer)[0] == '3':
                n1="static/img/3.png"
            elif str(nomer)[0] == '4':
                n1="static/img/4.png"
            elif str(nomer)[0] == '5':
                n1="static/img/5.png"
            elif str(nomer)[0] == '6':
                n1="static/img/6.png"
            elif str(nomer)[0] == '7':
                n1="static/img/7.png"
            elif str(nomer)[0] == '8':
                n1="static/img/8.png"
            elif str(nomer)[0] == '9':
                n1="static/img/9.png"
            if str(nomer)[1] == '0':
                n2="static/img/0.png"
            elif str(nomer)[1] == '1':
                n2="static/img/1.png"
            elif str(nomer)[1] == '2':
                n2="static/img/2.png"
            elif str(nomer)[1] == "3":
                n2="static/img/3.png"
            elif str(nomer)[1] == "4":
                n2="static/img/4.png"
            elif str(nomer)[1] == "5":
                n2="static/img/5.png"
            elif str(nomer)[1] == "6":
                n2="static/img/6.png"
            elif str(nomer)[1] == "7":
                n2="static/img/7.png"
            elif str(nomer)[1] == "8":
                n2="static/img/8.png"
            elif str(nomer)[1] == "9":
                n2="static/img/9.png"
        else:
            if nomer == 0:
                n2="static/img/0.png"
            elif nomer == 1:
                n2="static/img/1.png"
            elif nomer == 2:
                n2="static/img/2.png"
            elif nomer == 3:
                n2="static/img/3.png"
            elif nomer == 4:
                n2="static/img/4.png"
            elif nomer == 5:
                n2="static/img/5.png"
            elif nomer == 6:
                n2="static/img/6.png"
            elif nomer == 7:
                n2="static/img/7.png"
            elif nomer == 8:
                n2="static/img/8.png"
            elif nomer == 9:
                n2="static/img/9.png"
        #f.close()
        return render_template('play1.html',p = name[t][0],nr=n,n=r,nomer=nomer,n1=n1,n2=n2)

@app.route('/2',methods=['GET', 'POST'])
def second_task():
    global tr
    if tr == 1:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p2")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT n2 FROM p2")
        name1 = cursor_db.fetchall()
        cursor_db.execute("SELECT n3 FROM p2")
        name2 = cursor_db.fetchall()
        cursor_db.execute("SELECT n4 FROM p2")
        name3 = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0, len(name) - 1)
        print(t)
        otvet = [name[t][0], name1[t][0], name2[t][0], name3[t][0]]
        shuffle(otvet)
        ind_r = otvet.index(name[t][0])
        r = otvet[ind_r].split('/')
        r = r[-1]
        r = r.split('.')
        print(otvet)
        print(ind_r, r)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM tren")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer += 1
        n1 = "static/img/0.png"
        n2 = "static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1 = "static/img/1.png"
            elif str(nomer)[0] == '2':
                n1 = "static/img/2.png"
            elif str(nomer)[0] == '3':
                n1 = "static/img/3.png"
            elif str(nomer)[0] == '4':
                n1 = "static/img/4.png"
            elif str(nomer)[0] == '5':
                n1 = "static/img/5.png"
            elif str(nomer)[0] == '6':
                n1 = "static/img/6.png"
            elif str(nomer)[0] == '7':
                n1 = "static/img/7.png"
            elif str(nomer)[0] == '8':
                n1 = "static/img/8.png"
            elif str(nomer)[0] == '9':
                n1 = "static/img/9.png"
            if str(nomer)[1] == '0':
                n2 = "static/img/0.png"
            elif str(nomer)[1] == '1':
                n2 = "static/img/1.png"
            elif str(nomer)[1] == '2':
                n2 = "static/img/2.png"
            elif str(nomer)[1] == "3":
                n2 = "static/img/3.png"
            elif str(nomer)[1] == "4":
                n2 = "static/img/4.png"
            elif str(nomer)[1] == "5":
                n2 = "static/img/5.png"
            elif str(nomer)[1] == "6":
                n2 = "static/img/6.png"
            elif str(nomer)[1] == "7":
                n2 = "static/img/7.png"
            elif str(nomer)[1] == "8":
                n2 = "static/img/8.png"
            elif str(nomer)[1] == "9":
                n2 = "static/img/9.png"
        else:
            if nomer == 0:
                n2 = "static/img/0.png"
            elif nomer == 1:
                n2 = "static/img/1.png"
            elif nomer == 2:
                n2 = "static/img/2.png"
            elif nomer == 3:
                n2 = "static/img/3.png"
            elif nomer == 4:
                n2 = "static/img/4.png"
            elif nomer == 5:
                n2 = "static/img/5.png"
            elif nomer == 6:
                n2 = "static/img/6.png"
            elif nomer == 7:
                n2 = "static/img/7.png"
            elif nomer == 8:
                n2 = "static/img/8.png"
            elif nomer == 9:
                n2 = "static/img/9.png"
        return render_template('play2_tr.html',x=otvet, n=ind_r,r=r[0],n1=n1,n2=n2)
    else:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p2")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT n2 FROM p2")
        name1 = cursor_db.fetchall()
        cursor_db.execute("SELECT n3 FROM p2")
        name2 = cursor_db.fetchall()
        cursor_db.execute("SELECT n4 FROM p2")
        name3 = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0, len(name)-1)
        print(t)
        otvet = [name[t][0], name1[t][0], name2[t][0], name3[t][0]]
        shuffle(otvet)
        ind_r = otvet.index(name[t][0])
        r = otvet[ind_r].split('/')
        r = r[-1]
        r = r.split('.')
        print(otvet)
        print(ind_r,r)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM ypr")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer += 1
        n1 = "static/img/0.png"
        n2 = "static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1 = "static/img/1.png"
            elif str(nomer)[0] == '2':
                n1 = "static/img/2.png"
            elif str(nomer)[0] == '3':
                n1 = "static/img/3.png"
            elif str(nomer)[0] == '4':
                n1 = "static/img/4.png"
            elif str(nomer)[0] == '5':
                n1 = "static/img/5.png"
            elif str(nomer)[0] == '6':
                n1 = "static/img/6.png"
            elif str(nomer)[0] == '7':
                n1 = "static/img/7.png"
            elif str(nomer)[0] == '8':
                n1 = "static/img/8.png"
            elif str(nomer)[0] == '9':
                n1 = "static/img/9.png"
            if str(nomer)[1] == '0':
                n2 = "static/img/0.png"
            elif str(nomer)[1] == '1':
                n2 = "static/img/1.png"
            elif str(nomer)[1] == '2':
                n2 = "static/img/2.png"
            elif str(nomer)[1] == "3":
                n2 = "static/img/3.png"
            elif str(nomer)[1] == "4":
                n2 = "static/img/4.png"
            elif str(nomer)[1] == "5":
                n2 = "static/img/5.png"
            elif str(nomer)[1] == "6":
                n2 = "static/img/6.png"
            elif str(nomer)[1] == "7":
                n2 = "static/img/7.png"
            elif str(nomer)[1] == "8":
                n2 = "static/img/8.png"
            elif str(nomer)[1] == "9":
                n2 = "static/img/9.png"
        else:
            if nomer == 0:
                n2 = "static/img/0.png"
            elif nomer == 1:
                n2 = "static/img/1.png"
            elif nomer == 2:
                n2 = "static/img/2.png"
            elif nomer == 3:
                n2 = "static/img/3.png"
            elif nomer == 4:
                n2 = "static/img/4.png"
            elif nomer == 5:
                n2 = "static/img/5.png"
            elif nomer == 6:
                n2 = "static/img/6.png"
            elif nomer == 7:
                n2 = "static/img/7.png"
            elif nomer == 8:
                n2 = "static/img/8.png"
            elif nomer == 9:
                n2 = "static/img/9.png"
        return render_template('play2.html',x=otvet, n=ind_r,r=r[0],n1=n1,n2=n2)

@app.route('/3',methods=['GET', 'POST'])
def play3():
    global tr
    if tr == 1:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p3")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT n2 FROM p3")
        name1 = cursor_db.fetchall()
        cursor_db.execute("SELECT n3 FROM p3")
        name2 = cursor_db.fetchall()
        cursor_db.execute("SELECT n4 FROM p3")
        name3 = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0, len(name) - 1)
        print(t)
        otvet = [name[t][0], name1[t][0], name2[t][0], name3[t][0]]
        shuffle(otvet)
        ind_r = otvet.index(name[t][0])
        r = otvet[ind_r].split('/')
        r = r[-1]
        r = r.split('.')
        print(otvet)
        print(ind_r, r)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM tren")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer += 1
        n1 = "static/img/0.png"
        n2 = "static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1 = "static/img/1.png"
            elif str(nomer)[0] == '2':
                n1 = "static/img/2.png"
            elif str(nomer)[0] == '3':
                n1 = "static/img/3.png"
            elif str(nomer)[0] == '4':
                n1 = "static/img/4.png"
            elif str(nomer)[0] == '5':
                n1 = "static/img/5.png"
            elif str(nomer)[0] == '6':
                n1 = "static/img/6.png"
            elif str(nomer)[0] == '7':
                n1 = "static/img/7.png"
            elif str(nomer)[0] == '8':
                n1 = "static/img/8.png"
            elif str(nomer)[0] == '9':
                n1 = "static/img/9.png"
            if str(nomer)[1] == '0':
                n2 = "static/img/0.png"
            elif str(nomer)[1] == '1':
                n2 = "static/img/1.png"
            elif str(nomer)[1] == '2':
                n2 = "static/img/2.png"
            elif str(nomer)[1] == "3":
                n2 = "static/img/3.png"
            elif str(nomer)[1] == "4":
                n2 = "static/img/4.png"
            elif str(nomer)[1] == "5":
                n2 = "static/img/5.png"
            elif str(nomer)[1] == "6":
                n2 = "static/img/6.png"
            elif str(nomer)[1] == "7":
                n2 = "static/img/7.png"
            elif str(nomer)[1] == "8":
                n2 = "static/img/8.png"
            elif str(nomer)[1] == "9":
                n2 = "static/img/9.png"
        else:
            if nomer == 0:
                n2 = "static/img/0.png"
            elif nomer == 1:
                n2 = "static/img/1.png"
            elif nomer == 2:
                n2 = "static/img/2.png"
            elif nomer == 3:
                n2 = "static/img/3.png"
            elif nomer == 4:
                n2 = "static/img/4.png"
            elif nomer == 5:
                n2 = "static/img/5.png"
            elif nomer == 6:
                n2 = "static/img/6.png"
            elif nomer == 7:
                n2 = "static/img/7.png"
            elif nomer == 8:
                n2 = "static/img/8.png"
            elif nomer == 9:
                n2 = "static/img/9.png"
        return render_template('play2_tr.html', x=otvet, n=ind_r, r=r[0], n1=n1, n2=n2)
    else:
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p3")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT n2 FROM p3")
        name1 = cursor_db.fetchall()
        cursor_db.execute("SELECT n3 FROM p3")
        name2 = cursor_db.fetchall()
        cursor_db.execute("SELECT n4 FROM p3")
        name3 = cursor_db.fetchall()
        cursor_db.close()
        t = randint(0, len(name) - 1)
        print(t)
        otvet = [name[t][0], name1[t][0], name2[t][0], name3[t][0]]
        shuffle(otvet)
        ind_r = otvet.index(name[t][0])
        r = otvet[ind_r].split('/')
        r = r[-1]
        r = r.split('.')
        print(otvet)
        print(ind_r, r)
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM ypr")
        all = cursor_db.fetchall()
        cursor_db.close()
        nomer = 0
        for i in all:
            if i[0] == "правильно":
                nomer += 1
        n1 = "static/img/0.png"
        n2 = "static/img/0.png"
        if nomer > 9:
            if str(nomer)[0] == '0':
                n1 = "static/img/0.png"
            elif str(nomer)[0] == '1':
                n1 = "static/img/1.png"
            elif str(nomer)[0] == '2':
                n1 = "static/img/2.png"
            elif str(nomer)[0] == '3':
                n1 = "static/img/3.png"
            elif str(nomer)[0] == '4':
                n1 = "static/img/4.png"
            elif str(nomer)[0] == '5':
                n1 = "static/img/5.png"
            elif str(nomer)[0] == '6':
                n1 = "static/img/6.png"
            elif str(nomer)[0] == '7':
                n1 = "static/img/7.png"
            elif str(nomer)[0] == '8':
                n1 = "static/img/8.png"
            elif str(nomer)[0] == '9':
                n1 = "static/img/9.png"
            if str(nomer)[1] == '0':
                n2 = "static/img/0.png"
            elif str(nomer)[1] == '1':
                n2 = "static/img/1.png"
            elif str(nomer)[1] == '2':
                n2 = "static/img/2.png"
            elif str(nomer)[1] == "3":
                n2 = "static/img/3.png"
            elif str(nomer)[1] == "4":
                n2 = "static/img/4.png"
            elif str(nomer)[1] == "5":
                n2 = "static/img/5.png"
            elif str(nomer)[1] == "6":
                n2 = "static/img/6.png"
            elif str(nomer)[1] == "7":
                n2 = "static/img/7.png"
            elif str(nomer)[1] == "8":
                n2 = "static/img/8.png"
            elif str(nomer)[1] == "9":
                n2 = "static/img/9.png"
        else:
            if nomer == 0:
                n2 = "static/img/0.png"
            elif nomer == 1:
                n2 = "static/img/1.png"
            elif nomer == 2:
                n2 = "static/img/2.png"
            elif nomer == 3:
                n2 = "static/img/3.png"
            elif nomer == 4:
                n2 = "static/img/4.png"
            elif nomer == 5:
                n2 = "static/img/5.png"
            elif nomer == 6:
                n2 = "static/img/6.png"
            elif nomer == 7:
                n2 = "static/img/7.png"
            elif nomer == 8:
                n2 = "static/img/8.png"
            elif nomer == 9:
                n2 = "static/img/9.png"
        return render_template('play2.html', x=otvet, n=ind_r, r=r[0], n1=n1, n2=n2)


@app.route('/tr', methods=['GET', 'POST'])
def workout():
    global nomertr
    print(nomertr)
    global sp, tr
    tr = 1
    if nomertr == 0:#тут переход на страницу с началом тренировки
        if 'username' not in session:
            return render_template('te.html',name="Вход")
        else:
            nomertr +=1
            with open('static/text/ch_tr.txt', 'w', encoding='utf-8') as f:
                f.write("")
            return render_template('t.html',name = session['username'])
    elif nomertr == 16:
        print("все хватит")
        return redirect('/tr_och')
    else:
        n = randint(0,len(sp)-1)
        print(sp, n)
        ht = sp.pop(n)
        t = nomertr +1
        nomertr = t
        return redirect(ht)
@app.route('/tr_och', methods=['GET', 'POST'])
def training_report():
    global nomertr, sp
    nomertr = 0
    sp = ["/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3',"/1",'/2','/3']
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    cursor_db.execute(('''SELECT status FROM awards 
                                                WHERE login = '{}'; 
                                                ''').format(session['username']))
    status = cursor_db.fetchall()
    cursor_db.close()
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    cursor_db.execute(('''SELECT kol FROM rez_tr WHERE login = '{}'; ''').format(session['username']))
    kol = cursor_db.fetchall()
    print(status[0][0])
    print(kol)
    medal=""
    n_medal=""
    if len(kol) == 0:
        sql_update_query = """Update awards set status = ? where login = ?"""
        data = ("1,0,0", session['username'])
        cursor_db.execute(sql_update_query, data)
        db_lp.commit()
        medal = "static/img/медальки/первая медаль цв.jpg"
        n_medal = "Получена новая медаль"
    elif len(kol) == 4:
        sql_update_query = """Update awards set status = ? where login = ?"""
        data = ("1,1,0", session['username'])
        cursor_db.execute(sql_update_query, data)
        db_lp.commit()
        medal = "static/img/медальки/5 трен цв.jpg"
        n_medal = "Получена новая медаль"
    elif len(kol) == 9:
        sql_update_query = """Update awards set status = ? where login = ?"""
        data = ("1,1,1", session['username'])
        cursor_db.execute(sql_update_query, data)
        db_lp.commit()
        medal = "static/img/медальки/10 тр цв.jpg"
        n_medal = "Получена новая медаль"
    cursor_db.close()
    np = 0
    p = 0
    db_lp = sqlite3.connect(session['username']+'.db')
    cursor_db = db_lp.cursor()
    cursor_db.execute("SELECT total FROM tren")
    all = cursor_db.fetchall()
    cursor_db.close()
    for i in all:
        print(i[0])
        if i[0] == "правильно":
            p += 1
        else:
            np += 1
    if p/(p+np)>0.8:
        mess="Отличный результат"
    elif p/(p+np)>0.5:
        mess='Хороший результат'
    else:
        mess='Результат не очень надо еще позаниматься'
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    date_now = date.today()
    sql_insert = '''INSERT INTO rez_tr VALUES('{}','{}','{}','{}','{}');'''.format(session['username'], str(np + p), str(p),
                                                                              str(np),date_now)
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    db_lp = sqlite3.connect(session['username'] + '.db')
    cursor_db = db_lp.cursor()
    sql_update_query = """DELETE from tren where total = ?"""
    cursor_db.execute(sql_update_query, ("правильно",))
    db_lp.commit()
    cursor_db.execute(sql_update_query, ("не правильно",))
    db_lp.commit()
    cursor_db.close()
    return render_template('tr_och.html',name=session['username'],medal=medal, n_m =n_medal,p=p,v=p+np,mess=mess)

@app.route('/check_yp', methods=['GET', 'POST'])
def ck_yp():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        db_lp = sqlite3.connect(session['username'] + '.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT total FROM ypr")
        all_ypr = cursor_db.fetchall()
        cursor_db.close()

        if len(all_ypr) > 0:  # проверить что упражнение начато
            return render_template('check.html', m=session['username'])
        else:
            return redirect("/yp")
@app.route('/ck_yp_del', methods=['GET', 'POST'])
def ck_yp_del():
    db_lp = sqlite3.connect(session['username'] + '.db')
    cursor_db = db_lp.cursor()
    sql_update_query = """DELETE from ypr where total = ?"""
    cursor_db.execute(sql_update_query, ("правильно",))
    db_lp.commit()
    cursor_db.execute(sql_update_query, ("не правильно",))
    db_lp.commit()
    cursor_db.close()
    return redirect("/yp")
@app.route('/yp', methods=['GET', 'POST'])
def exercises():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        global tr
        tr = 0
        return render_template('awards_aut.html',m =session['username'])
@app.route('/otc', methods=['GET', 'POST'])
def report():
    if 'username' not in session:
        p = "2024-06-03;066;033/2024-06-03;033;066/2024-06-03;000;100/2024-06-03;050;050/2024-06-03;100;000/"
        p_t = "2024-06-03;066;033/2024-06-03;033;066/2024-06-03;000;100/2024-06-03;050;050/2024-06-03;100;000/"
        return render_template('statis.html',m=0,name="Вход",p=p,l=len(p),pt=p_t)
    else:
        Login = session['username']
        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT kol FROM rez WHERE login = '{}'; ''').format(Login))
        pas = cursor_db.fetchall()
        cursor_db.execute(('''SELECT raid FROM rez WHERE login = '{}'; ''').format(Login))
        raid = cursor_db.fetchall()
        cursor_db.execute(('''SELECT date FROM rez WHERE login = '{}'; ''').format(Login))
        date = cursor_db.fetchall()
        cursor_db.execute(('''SELECT kol FROM rez_tr WHERE login = '{}'; ''').format(Login))
        all_tr = cursor_db.fetchall()
        cursor_db.execute(('''SELECT rid FROM rez_tr WHERE login = '{}'; ''').format(Login))
        raid_tr = cursor_db.fetchall()
        cursor_db.execute(('''SELECT date FROM rez_tr WHERE login = '{}'; ''').format(Login))
        date_tr = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        sum_p=0
        p=""
        sum_r=0
        sum_p_tr = 0
        sum_r_tr = 0
        rr=0
        nn=0
        rr_tr=0
        nn_tr=0
        p_t=''
        for i in range(len(pas)):
            sum_p+=pas[i][0]
            sum_r+=raid[i][0]
            if pas[i][0]==0:
                pass
            else:
                rr = int(raid[i][0]*100/pas[i][0])
                nn = int((pas[i][0]-raid[i][0])*100/pas[i][0])
            if rr<10:
                strr="00"+str(rr)
            elif rr>=10 and rr<100:
                strr="0"+str(rr)
            else:
                strr=str(rr)
            if nn<10:
                strn="00"+str(nn)
            elif nn>=10 and nn<100:
                strn="0"+str(nn)
            else:
                strn=str(nn)
            p += str(date[i][0])+";"+strr+";"+strn+str("/")
        print(p)
        for i in range(len(all_tr)):
            sum_p_tr += all_tr[i][0]
            sum_r_tr += raid_tr[i][0]
            if all_tr[i][0] == 0:
                pass
            else:
                rr_tr = int(raid_tr[i][0] * 100 / all_tr[i][0])
                nn_tr = int((all_tr[i][0] - raid_tr[i][0]) * 100 / all_tr[i][0])
            if rr_tr<10:
                strr_tr="00"+str(rr_tr)
            elif rr_tr>=10 and rr_tr<100:
                strr_tr="0"+str(rr_tr)
            else:
                strr_tr=str(rr_tr)
            if nn_tr<10:
                strn_tr="00"+str(nn_tr)
            elif nn_tr>=10 and nn_tr<100:
                strn_tr="0"+str(nn_tr)
            else:
                strn_tr=str(nn_tr)
            p_t += str(date_tr[i][0]) + ";" + strr_tr + ";" + strn_tr + str("/")
        if sum_p == 0:
            r=0
            pas="0;0;0"
        else:
            r = int((sum_r+sum_r_tr)/(sum_p+sum_p_tr)*100)
        print(p_t)
        return render_template('statis.html',m=r,name=Login,p=p,l=len(pas),pt=p_t,)

@app.route('/vid', methods=['GET', 'POST'])
def exercise_report():
    print(session['username'])
    np=0
    p=0
    db_lp = sqlite3.connect(session['username']+'.db')
    cursor_db = db_lp.cursor()
    cursor_db.execute("SELECT total FROM ypr")
    all = cursor_db.fetchall()
    cursor_db.close()
    for i in all:
        print(i[0])
        if i[0] == "правильно":
            p += 1
        else:
            np += 1
    if p/(p+np)>0.8:
        mess="Отличный результат"
    elif p/(p+np)>0.5:
        mess='Хороший результат'
    else:
        mess='Результат не очень надо еще позаниматься'
    dt_now = date.today()
    print(mess)
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    sql_insert = '''INSERT INTO rez VALUES('{}','{}','{}','{}','{}');'''.format(session['username'], str(np+p), str(p),str(np),dt_now)
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    db_lp = sqlite3.connect(session['username'] + '.db')
    cursor_db = db_lp.cursor()
    sql_update_query = """DELETE from ypr where total = ?"""
    cursor_db.execute(sql_update_query, ("правильно",))
    db_lp.commit()
    cursor_db.execute(sql_update_query, ("не правильно",))
    db_lp.commit()
    cursor_db.close()
    return render_template('otch_vid.html',name=session['username'],p=p,np=np,mess=mess)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file_color = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_color)
        flash('File successfully uploaded')
        file_black = file_color.split('.')[0]+'1.jpg'
        color_image = Image.open(file_color)
        bw = color_image.convert('L')
        bw.save(file_black)
        color_img = ''
        for i in (file_black.split("/")):
            if "медальки" in i:
                color_img = i[9:]
        db_lp = sqlite3.connect('pict.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT INTO p1 VALUES('{}','{}');'''.format(filename, color_img)
        cursor_db.execute(sql_insert)
        db_lp.commit()
        cursor_db.close()
        db_lp.close()
        return redirect('/awards')

if __name__ == "__main__":
    app.run()
