# -*- coding: utf-8 -*-
import sys
sys.path.append('venv/lib/python2.7/site-packages')

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os,sys,random
import MySQLdb,hashlib
import MySQLdb.cursors


db_host = 'localhost'
db_user = 'root'
db_password = '123456'
db_name = 'zhanqun'
db_port = 3306
article_dir = '/root/wwwroot/zhanqun/static/txt'
image_dir = '/Users/Arnoldnuo/Documents/python/zhanqun/static/images'

def addArticle(title,content):
    title_md5 = hashlib.md5(title).hexdigest() 
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name,port=db_port,charset='utf8')
    cur = conn.cursor()
    insertSql = "insert ignore into article(id,title,content) values(%s, %s, %s)"
    cur.execute(insertSql, (title_md5, title, content))
    conn.commit()
    cur.close()
    conn.close()

def readArticle(article_dir):
    file_list = os.listdir(article_dir)
    for file_name in file_list:
        file_detail = {}
        filepath = os.path.join(article_dir,file_name)
        if os.path.isfile(filepath):
            with open (filepath, "r") as myfile:
                file_detail["base_content"] = myfile.read().decode('gbk','ignore').encode('utf-8')
                file_detail["content"] = "<br />".join(file_detail['base_content'].split())
                file_detail["title"] = file_name.decode('gbk','ignore').encode('utf-8').replace('\.txt','');
                file_detail["filepath"] = filepath
                # 保存文章到数据库
                addArticle(file_detail["title"], file_detail["content"])
                print u'添加成功'
                # 删除文件
                #os.remove(file_detail["filepath"])

# addArticle('我是第一个文章','我是第一个内容')
# getArticle('d626a9444c1c281d4bcfbf9b7b77a3d6')
readArticle(article_dir)
