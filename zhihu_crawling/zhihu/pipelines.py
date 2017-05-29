# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import datetime
from zhihu.myconfig import DbConfig

class UserPipeline(object):
    def __init__(self):
        pass
        # 清空表
        # self.cursor.execute('truncate table weather;')
        # self.conn.commit()

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(user = DbConfig['user'], passwd = DbConfig['passwd'], db = DbConfig['db'], host = DbConfig['host'], charset = 'utf8', use_unicode = True)
        self.cursor = self.conn.cursor()

        createTable = """
            create table 'users' (
                'url' VARCHAR(255) NOT NULL,
                'name' VARCHAR(255) NOT NULL,
                'bio' VARCHAR(255) NOT NULL,
                'location' VARCHAR(255) NOT NULL,
                'business' VARCHAR(255) NOT NULL,
                'gender' VARCHAR(255) NOT NULL,
                'avatar' VARCHAR(255) NOT NULL,
                'education' VARCHAR(255) NOT NULL,
                'major' VARCHAR(255) NOT NULL,
                'employment' VARCHAR(255) NOT NULL,
                'position' VARCHAR(255) NOT NULL,
                'content' VARCHAR(255) NOT NULL,
                'ask' VARCHAR(255) NOT NULL,
                'answer' VARCHAR(255) NOT NULL,
                'agree' VARCHAR(255) NOT NULL,
                'thanks' VARCHAR(255) NOT NULL,
                'create_at' VARCHAR(255) NOT NULL
            );
        """

        try:
            self.cursor.execute(createTable)
        except:
            pass


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:
            self.cursor.execute(
                """INSERT IGNORE INTO users (url, name, bio, location, business, gender, avatar, education, major, employment, position, content, ask, answer, agree, thanks, create_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['url'],
                    item['name'],
                    item['bio'],
                    item['location'],
                    item['business'],
                    item['gender'],
                    item['avatar'],
                    item['education'],
                    item['major'],
                    item['employment'],
                    item['position'],
                    item['content'],
                    item['ask'],
                    item['answer'],
                    item['agree'],
                    item['thanks'],
                    curTime
                )
            )
            self.conn.commit()
        except MySQLdb.Error, e:
            print 'Error %d %s' % (e.args[0], e.args[1])

        return item
