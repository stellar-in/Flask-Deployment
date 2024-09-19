import math, time, sqlite3, random, re

from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Reading DB Problem')
        return []

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT count() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("This Post with url exists")
                return False
            base = url_for('static', filename='images_html')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                "\\g<tag>" + base + "/\\g<url>>", text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as error:
            print(f"Promlem in DB: {error}")
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res

            
        except sqlite3.Error as e:
            print(f"Problem: {e}")
        
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print(f"Problem: {e}")
        
        return []