import sqlite3

# 连接到主数据库
conn = sqlite3.connect('.db/main_database.db')
cursor = conn.cursor()

# 创建主数据库中的表
cursor.execute('''
CREATE TABLE IF NOT EXISTS main_table (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')
conn.commit()

# 附加另一个数据库
cursor.execute("ATTACH DATABASE 'another_database.db' AS another")

# 创建附加数据库中的表
cursor.execute('''
CREATE TABLE IF NOT EXISTS another.another_table (
    id INTEGER PRIMARY KEY,
    value REAL
)
''')
conn.commit()

# 从主数据库和附加数据库中查询数据
cursor.execute("SELECT * FROM main.main_table")
print("Main database table:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM another.another_table")
print("Another database table:")
for row in cursor.fetchall():
    print(row)

# 分离附加的数据库
cursor.execute("DETACH DATABASE another")

# 关闭连接
conn.close()