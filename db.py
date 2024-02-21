import sqlite3
db_lp = sqlite3.connect('login_password.db')# подключаемся к бд
cursor_db = db_lp.cursor()#объект для взаимодействия
#SQL-запрос для создания таблицы с логинами и паролями;
sql_create = '''CREATE TABLE passwords( 
login TEXT PRIMARY KEY,
password TEXT NOT NULL);'''

cursor_db.execute(sql_create)
db_lp.commit()#Сохраняем изменения в БД методом commit();

cursor_db.close()
db_lp.close()