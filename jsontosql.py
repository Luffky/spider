import json
import pymysql

def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS review")  # 习惯性
    sql = """CREATE TABLE review (
             author  VARCHAR(100),
             title  VARCHAR(100),
             comment_count INT,
             exceprt VARCHAR(10000),
             ans_url VARCHAR(100)
             )"""
    cursor.execute(sql)  # 根据需要创建一个表格


def reviewdata_insert(db):

    with open(r'./answer-Copy.json', encoding='utf-8') as f:
        i = 0
        while True:
            i += 1
            print(u'正在载入第%s行......' % i)
            try:
                lines = f.readline()  # 使用逐行读取的方法
                review_text = json.loads(lines)  # 解析每一行数据
                result = []
                result.append((review_text['author'], review_text['title'],review_text['comment_count'],review_text['exceprt'], review_text['ans_url']
                ))
                print(result)

                inesrt_re = "insert into review(author, title, comment_count, exceprt, ans_url) values (%s, %s, %s, %s,%s)"
                cursor = db.cursor()
                cursor.executemany(inesrt_re, result)
                db.commit()
            except Exception as e:
                db.rollback()
                print(str(e))
                break


if __name__ == "__main__":  # 起到一个初始化或者调用函数的作用
    db = pymysql.connect("localhost", "root", password="fky1996214", db="zm'sTable",use_unicode=True,charset='utf8')
    cursor = db.cursor()
    prem(db)
    reviewdata_insert(db)
    cursor.close()