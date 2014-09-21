# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from werkzeug.contrib.fixers import ProxyFix
import os,sys,random
import MySQLdb,hashlib
import MySQLdb.cursors
from flask import Flask, render_template

db_host = 'localhost'
db_user = 'root'
db_password = '123456'
db_name = 'zhanqun'
db_port = 3306
article_dir = '/root/wwwroot/zhanqun/static/txt/4'
image_dir = '/root/wwwroot/zhanqun/static/images'

# 数据库连接
def addArticle(title,content):
    title_md5 = hashlib.md5(title).hexdigest() 
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name,port=db_port,charset='utf8')
    cur = conn.cursor()
    insertSql = "insert ignore into article(id,title,content) values(%s, %s, %s)"
    cur.execute(insertSql, (title_md5, title, content))
    conn.commit()
    cur.close()
    conn.close()

def getArticle(id):
    selectSql = 'select * from article where id = "%s"' % id
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name,port=db_port,cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')
    cur = conn.cursor()
    count = cur.execute(selectSql)
    articleObj = cur.fetchone()
    return articleObj

def getRandomArticles(count):
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name,port=db_port,cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')
    cur = conn.cursor()
    getCountSql = "select count(*) count from article"
    cur.execute(getCountSql)
    row_count = cur.fetchone()["count"]
    start_row_index = random.randint(0, row_count - count)
    selectSql = "select id, title from article order by id limit %d, %d" % (start_row_index, count)
    cur.execute(selectSql)
    articleList = cur.fetchall()
    return articleList

def getRandomImagesName(count):
    image_list = os.listdir(image_dir)
    randomIndex = random.randint(0, len(image_list)-count)
    return image_list[randomIndex:randomIndex+count]

def readArticle(article_dir):
    file_list = os.listdir(article_dir)
    for file_name in file_list:
        file_detail = {}
        filepath = os.path.join(article_dir,file_name)
        if os.path.isfile(filepath):
            with open (filepath, "r") as myfile:
                file_detail["base_content"] = myfile.read().decode('gbk','ignore').encode('utf-8')
                file_detail["content"] = "<br />".join(file_detail['base_content'].split())
                file_detail["title"] = file_name.replace('\.txt','');
                file_detail["filepath"] = filepath
                # 保存文章到数据库
                addArticle(file_detail["title"], file_detail["content"])
                # 删除文件
                # os.remove(file_detail["filepath"])

# addArticle('我是第一个文章','我是第一个内容')
# getArticle('d626a9444c1c281d4bcfbf9b7b77a3d6')
# readArticle(article_dir)

app = Flask(__name__, static_folder="static")

@app.route('/')
def indexHtml():
    articleList = getRandomArticles(200)
    images = getRandomImagesName(36)
    for index in range(len(images)):
        images[index] = '/static/images/' + images[index]

    return render_template('index.html', images=images,news = articleList, hots = articleList[0:15], tuijians = articleList[15:25], yueshangs = articleList[25:35], guangzhous = articleList[35:45],  pingluns=articleList[45:55], news_old=articleList[55:90])

@app.route('/page/<id>')
def pageHtml(id):
    articleList = getRandomArticles(200)
    article = getArticle(id)
    images = getRandomImagesName(10)
    article['title'] = article['title'].replace('.txt','')
    return render_template('page.html',article = article, images = images, news=articleList[0:10], hots = articleList[10:20]) 


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    #app.debug = True
    app.run(host="0.0.0.0")
