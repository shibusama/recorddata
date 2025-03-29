import sqlite3

# 连接数据库，若不存在则创建
conn = sqlite3.connect('./db/example.db')
# 创建游标对象
cursor = conn.cursor()

# 创建表
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                  (date text, trans text, symbol text, qty real, price real)''')

# 插入数据
cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# 提交事务
conn.commit()

# 查询数据
cursor.execute("SELECT * FROM stocks")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()