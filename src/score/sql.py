# -*- coding: utf-8 -*-

import sys
import aiomysql
import datetime
from score.global_var import get_value


class SQL():
    def __init__(self):
        self.config = get_value('config')
        self.logger = get_value('logger')
        self.sql_host = self.config.sql_host
        self.sql_port = self.config.sql_port
        self.sql_username = self.config.sql_username
        self.sql_password = self.config.sql_password
        self.sql_database = self.config.sql_database
        self.pool = None

    async def get_curosr(self):
        '''获取db连接和cursor对象，用于db的读写操作'''
        if self.pool is None:
            # 实例化连接池
            self.pool = await aiomysql.create_pool(
                maxsize=20,
                host=self.sql_host,
                port=self.sql_port,
                user=self.sql_username,
                password=self.sql_password,
                db=self.sql_database,
                charset='utf8mb4',
                autocommit=False
            )

        conn = await self.pool.acquire()
        cursor = await conn.cursor(aiomysql.DictCursor)
        return conn, cursor

    async def insertUsers(self, info_dict):
        conn, cursor = await self.get_curosr()

        try:
            sql = '''
            INSERT INTO `u2_info` (
                `Get_Time`,
                `User_ID`,
                `User_Name`,
                `Join_Date`,
                `Last_Seen`,
                `Gender`,
                `User_Class`,
                `Uploaded`,
                `Downloaded`,
                `Raw_Uploaded`,
                `Raw_Downloaded`,
                `UCoin`,
                `EXP`,
                `Seeding_Time`,
                `Downloading_Time`,
                `Torrent_Comments`,
                `Forum_Posts`,
                `Uploaded_Torrents_Quantity`,
                `Uploaded_Torrents_Size`,
                `Currently_Seeding_Quantity`,
                `Currently_Seeding_Size`,
                `Completed_Torrents_Quantity`,
                `Completed_Torrents_Size`
                )
            VALUES (
                %(Get_Time)s,
                %(User_ID)s,
                %(User_Name)s,
                %(Join_Date)s,
                %(Last_Seen)s,
                %(Gender)s,
                %(User_Class)s,
                %(Uploaded)s,
                %(Downloaded)s,
                %(Raw_Uploaded)s,
                %(Raw_Downloaded)s,
                %(UCoin)s,
                %(EXP)s,
                %(Seeding_Time)s,
                %(Downloading_Time)s,
                %(Torrent_Comments)s,
                %(Forum_Posts)s,
                %(Uploaded_Torrents_Quantity)s,
                %(Uploaded_Torrents_Size)s,
                %(Currently_Seeding_Quantity)s,
                %(Currently_Seeding_Size)s,
                %(Completed_Torrents_Quantity)s,
                %(Completed_Torrents_Size)s
                )'''
            await cursor.execute(sql, info_dict)
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            self.logger.error('[sql][insertUsers]: {}'.format(e))
            return False
        else:
            return None
        finally:
            await cursor.close()
            await self.pool.release(conn)

    async def selectUsersList(self):
        '''获取用户列表'''
        conn, cursor = await self.get_curosr()
        sql = "SELECT `id` FROM `u2_user` ORDER BY `id`"
        await cursor.execute(sql)  # 4、执行sql语句
        results = await cursor.fetchall()
        await conn.commit()
        await cursor.close()
        await self.pool.release(conn)
        return results

    async def selectUsersInfo(self, uid, date='2000-01-01 00:00:00'):
        conn, cursor = await self.get_curosr()
        sql = "SELECT * FROM `u2_info` WHERE `User_ID` = '%s' AND `Get_Time` >= %s ORDER BY `Self`"
        await cursor.execute(sql, (uid, date))
        results = await cursor.fetchall()
        await conn.commit()
        await cursor.close()
        await self.pool.release(conn)
        return results
