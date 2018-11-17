import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='123',
                       db='m3800')
cursor = conn.cursor()
cursor.execute('SET CHARACTER SET utf8;')
data = cursor.execute('SELECT agt FROM employee;')
sql ="""insert into employee(first_name,last_name,agt,sex,income)values('hu','shaohang',42,'f',3000)"""
try:
    cursor.execute(sql)
    conn.commit()
except:
    conn.rollback()

conn.close()
print(data)
