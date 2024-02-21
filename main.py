from flask import Flask, request, render_template
import sqlite3
from random import randint, shuffle

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def q():
    return render_template('start.html')
@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
   if request.method == 'POST':
       Login = request.form.get('Login')
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
       return render_template('successfulauth.html')

   return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)
       cursor_db.execute(sql_insert)
       cursor_db.close()
       db_lp.commit()
       db_lp.close()
       return render_template('successfulregis.html')
   return render_template('registration.html')
@app.route('/1',methods=['GET', 'POST'])
def it():
    t = randint(1,2)
    return render_template('play1.html',name="static/img/"+str(t)+".jpg",n=str(t))

@app.route('/2',methods=['GET', 'POST'])
def foo():
    x = [i for i in range(3,6)]
    shuffle(x)
    for i in range(3):
        print(x[i]-2)
    return render_template('play2.html',x=x, n=randint(1,3))
if __name__ == "__main__":
 app.run()