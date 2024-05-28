import eel
from flask import Flask, request, render_template, session,redirect, jsonify
import sqlite3
from random import randint, shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
nomertr = 0
tr = 0
sp = ["/1",'/2','/3',"/1"]
awcolor=['static/img/медальки/первая медаль цв.jpg','static/img/медальки/5 трен цв.jpg','static/img/медальки/10 тр цв.jpg']
awblack=['static/img/медальки/первая медаль чб.jpg','static/img/медальки/5 трен чб.jpg','static/img/медальки/10 тр чб.jpg']
@app.route('/get-text',methods=['POST'])#pзаменить что и куда это вывод подсет для пользователя
def pri():
    # Получаем данные из тела запроса
    data = request.json
    # Получаем значение из данных
    value = data.get('data')
    f = open("static/text/test.txt", 'r',encoding='utf-8')
    file = f.read()
    file+='\n'+value
    f.close()
    with open('static/text/test.txt', 'w',encoding='utf-8') as f:
        f.write(file)
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
    f = open("static/text/ch_tr.txt", 'r',encoding='utf-8')
    file = f.read()
    file+='\n'+value
    f.close()
    with open('static/text/ch_tr.txt', 'w',encoding='utf-8') as f:
        f.write(file)
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
    st=[""]*len(awblack)
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
    status = status[0][0].split(",")
    for i in range(len(awblack)):
        if status[i] == '0':
            st[i]=awblack[i]
        else:
            st[i]=awcolor[i]
    return render_template('awards_log.html',m=session['username'],st=st)
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
       Roll = request.form.get('Roll')
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
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
       roll_db.close()
       try:
           if pas[0][0] != Password:
               return render_template('auth_bad.html', name = "Вход")
       except:
           return render_template('auth_bad.html', name = "Вход")

       db_lp.close()
       if session['roll'] == "Учитель":
           return redirect('/1')
       elif session['roll'] == "Ученик":
           return redirect('/2')
       else:
           return redirect('/')

   return render_template('index.html', name = "Вход")

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        session['username'] = Login
        Password = request.form.get('Password')
        Roll = request.form.get('Roll')
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
        return render_template('exit.html',name=session['username'])
@app.route('/1',methods=['GET', 'POST'])
def it():
    global tr
    if tr == 1:
        t = randint(0, 1)
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p1")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT po FROM p1")
        prav_otvet = cursor_db.fetchall()
        cursor_db.execute("SELECT npo FROM p1")
        ne_prav_otvet = cursor_db.fetchall()
        cursor_db.close()
        r = prav_otvet[t][0]
        nr = ne_prav_otvet[t][0].split(",")
        n = [r, nr[0], nr[1], nr[2]]
        shuffle(n)
        f = open("static/text/ch_tr.txt", 'r', encoding='utf-8')
        file = f.read()
        file = file.split('\n')
        nomer = 0
        for i in file:
            if i == "правильно":
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
        f.close()
        return render_template('play1_tr.html', p=name[t][0], nr=n, n=r,n1=n1,n2=n2)
    else:
        t = randint(0,1)
        db_lp = sqlite3.connect('rez.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT n FROM p1")
        name = cursor_db.fetchall()
        cursor_db.execute("SELECT po FROM p1")
        prav_otvet = cursor_db.fetchall()
        cursor_db.execute("SELECT npo FROM p1")
        ne_prav_otvet = cursor_db.fetchall()
        cursor_db.close()
        r = prav_otvet[t][0]
        nr = ne_prav_otvet[t][0].split(",")
        n = [r,nr[0],nr[1],nr[2]]
        shuffle(n)
        f = open("static/text/test.txt", 'r', encoding='utf-8')
        file = f.read()
        file = file.split('\n')
        nomer = 0
        for i in file:
            if i == "правильно":
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
        f.close()
        return render_template('play1.html',p = name[t][0],nr=n,n=r,nomer=nomer,n1=n1,n2=n2)

@app.route('/2',methods=['GET', 'POST'])
def foo():
    global tr
    if tr == 1:
        x = [i for i in range(3, 6)]
        shuffle(x)
        for i in range(3):
            print(x[i] - 2)
        return render_template('play2_tr.html', x=x, n=randint(1, 4))
    else:
        x = [i for i in range(3,7)]
        shuffle(x)
        for i in range(4):
            print(x[i]-2)
        return render_template('play2.html',x=x, n=randint(1,4))

@app.route('/3',methods=['GET', 'POST'])
def play3():
    global tr
    if tr == 1:
        x = [i for i in range(3, 6)]
        shuffle(x)
        for i in range(3):
            print(x[i] - 2)
        return render_template('play3_tr.html', x=x, n=randint(1, 3))
    else:
        x = [i for i in range(3, 6)]
        shuffle(x)
        for i in range(3):
            print(x[i] - 2)
        return render_template('play3.html', x=x, n=randint(1, 3))


@app.route('/tr', methods=['GET', 'POST'])
def trenirovka():
    global nomertr
    print(nomertr)
    global sp
    if nomertr == 0:#тут переход на страницу с началом тренировки
        global tr
        tr = 1
        nomertr +=1
        with open('static/text/ch_tr.txt', 'w', encoding='utf-8') as f:
            f.write("")
        return render_template('t.html')
    elif nomertr == 4:
        print("все хватит")
        nomertr = 0
        sp = ["/1", '/2', "/3",'/1']
        return redirect('/tr_och')
    else:
        n = randint(0,len(sp)-1)
        print(sp, n)
        ht = sp.pop(n)
        if 'username' not in session:
            return redirect('/authorization')
        else:
            t = nomertr +1
            nomertr = t
            return redirect(ht)
@app.route('/tr_och', methods=['GET', 'POST'])
def trenirovka_och():
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
    f = open("static/text/ch_tr.txt", 'r', encoding='utf-8')
    file = f.read()
    for i in file.split("\n"):
        print(i)
        if i == "правильно":
            p += 1
        elif i == "":
            pass
        else:
            np += 1
    f.close()
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    print(session['username'])
    sql_insert = '''INSERT INTO rez_tr VALUES('{}','{}','{}','{}');'''.format(session['username'], str(np + p), str(p),
                                                                              str(np))
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    with open('static/text/ch_tr.txt', 'w', encoding='utf-8') as f:
        f.write("")
    return render_template('tr_och.html',m =session['username'],medal=medal, n_m =n_medal,p=p,v=p+np)
@app.route('/yp', methods=['GET', 'POST'])
def qqq():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        global tr
        tr = 0
        return render_template('awards_aut.html',m =session['username'])
@app.route('/otc', methods=['GET', 'POST'])
def ot():
    if 'username' not in session:
        return redirect('/authorization')
    else:
        Login = session['username']
        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT kol FROM rez WHERE login = '{}'; ''').format(Login))
        pas = cursor_db.fetchall()
        cursor_db.execute(('''SELECT raid FROM rez WHERE login = '{}'; ''').format(Login))
        raid = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        sum_p=0
        p=""
        sum_r=0
        for i in range(len(pas)):
            sum_p+=pas[i][0]
            sum_r+=raid[i][0]
            if pas[i][0]==0:
                pass
            else:
                rr = raid[i][0]/pas[i][0]
                nn = (pas[i][0]-raid[i][0])/pas[i][0]
            print(round(nn, 2)*100)
            p += str(i+1)+";"+str(round(rr, 1))+";"+str(round(nn, 1))+str("/")
        print(p)
        if sum_p == 0:
            r=0
            pas="0;0;0"
        else:
            r = int(sum_r/sum_p*100)
        return render_template('statis.html',m=r,name=Login,p=p,l=len(pas))

@app.route('/vid', methods=['GET', 'POST'])
def vid():
    print(session['username'])
    np=0
    p=0
    f = open("static/text/test.txt", 'r', encoding='utf-8')
    file = f.read()
    print(file.split("\n"))
    for i in file.split("\n"):
        print(i)
        if i == "не правильно":
            np +=1
        elif i == "правильно":
            p+=1
    f.close()
    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    sql_insert = '''INSERT INTO rez VALUES('{}','{}','{}','{}');'''.format(session['username'], str(np+p), str(p),str(np))
    cursor_db.execute(sql_insert)
    db_lp.commit()
    cursor_db.close()
    db_lp.close()
    with open('static/text/test.txt', 'w', encoding='utf-8') as f:
        f.write("")
    return render_template('otch_vid.html',name=session['username'])
if __name__ == "__main__":
    app.run()
