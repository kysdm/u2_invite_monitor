# -*- coding: utf-8 -*-


import re
import datetime
import asyncio
# import json
from lxml import etree
from score.global_var import set_value
from score.global_var import get_value
import prettytable as pt


class Users:
    def __init__(self):
        self.sql = get_value('sql')
        self.logger = get_value('logger')
        self.config = get_value('config')

    async def run(self):
        user_list = await self.sql.selectUsersList()
        # user_info = await self.sql.selectUsersInfo()
        await self.getUsers(user_list)
        await self.postUsers(user_list)

    async def getUsers(self, user_list):
        sem = asyncio.Semaphore(2)
        tasks = [asyncio.create_task(self.process(_, sem))
                 for _ in [_['id'] for _ in user_list]]
        await asyncio.gather(*tasks)

    async def process(self, uid, sem):
        websource = get_value('websource')
        # self.logger.info('Get get_html')

        async with sem:
            html = etree.HTML(await websource.getHtml(f'https://u2.dmhy.org/userdetails.php?id={uid}'))

            # 已经去世的人
            if html.xpath('//td[@id="outer"]/table/tr/td/h2/text()'):
                e = html.xpath('//td[@id="outer"]/table/tr/td/table/tr/td/text()')
                self.logger.error(f'#{uid} | {e[0] if e else "None"}')
                return

            # 高隐私账户 新用户除非申请福音组，否则不会有高隐私的
            privacy = html.xpath('//*[@id="outer"]/table/tr/td/table/tr[2]/td/font/text()')
            if privacy:
                self.logger.error(f'#{uid} | {privacy[0] if privacy else "None"}')
                return

            user_name = html.xpath('//*[@id="outer"]/h1/span/b/bdo/text()')[0]
            join_date = html.xpath('//td[text()="加入日期"]/following-sibling::td[1]/time/text()')[0]
            last_seen = html.xpath('//td[text()="最近动向"]/following-sibling::td[1]/time/text()')[0]
            gender = html.xpath('//td[text()="性别"]/following-sibling::td[1]/img/@title')[0]
            user_class = html.xpath('//td[text()="等级"]/following-sibling::td[1]/img/@title')[0]
            exp = int(re.search(r':\s?(\d+)', html.xpath('//td[text()="经验值"]/following-sibling::td[1]/text()')[0]).group(1))
            torrent_comments = html.xpath('//td[text()="种子评论"]/following-sibling::td[1]')[0].xpath('string(.)')
            forum_posts = html.xpath('//td[text()="论坛帖子"]/following-sibling::td[1]')[0].xpath('string(.)')
            ucoin = html.xpath('//td[text()="UCoin"]/following-sibling::td[1]/span/@title')[0].replace(",", "")
            uploaded = toGib(html.xpath('//td[@class="embedded"]/strong[text()="上传量"]/parent::td/text()')[-1])
            downloaded = toGib(html.xpath('//td[@class="embedded"]/strong[text()="下载量"]/parent::td/text()')[-1])
            raw_uploaded = toGib(html.xpath('//td[@class="embedded"]/strong[text()="实际上传"]/parent::td/text()')[-1])
            raw_downloaded = toGib(html.xpath('//td[@class="embedded"]/strong[text()="实际下载"]/parent::td/text()')[-1])
            seeding_time = toMin(html.xpath('//td[@class="embedded"]/strong[text()="做种时间"]/parent::td/text()')[-1])
            downloading_time = toMin(html.xpath('//td[@class="embedded"]/strong[text()="下载时间"]/parent::td/text()')[-1])

            # 获取上传种子的数量
            html = etree.HTML(await websource.getHtml(f'https://u2.dmhy.org/getusertorrentlistajax.php?userid={uid}&type=uploaded'))
            xp = ''.join(html.xpath('//text()')[:3]).replace('\xad', '').replace('\xa0', '')
            if xp == "没有记录":
                uploaded_torrents_quantity = 0
                uploaded_torrents_size = 0
            else:
                _r = re.search(r'实际上传(\d+)个种子，([^。]+)。', xp)
                uploaded_torrents_quantity = int(_r.group(1))
                uploaded_torrents_size = toGib(_r.group(2))

            # 做种数量
            html = etree.HTML(await websource.getHtml(f'https://u2.dmhy.org/getusertorrentlistajax.php?userid={uid}&type=seeding'))
            xp = ''.join(html.xpath('//text()')[:2]).replace('\xad', '').replace('\xa0', '')
            if xp == "没有记录":
                currently_seeding_quantity = 0
                currently_seeding_size = 0
            else:
                _r = re.search(r'(\d+)条记录大小(.+)', xp)
                currently_seeding_quantity = int(_r.group(1))
                currently_seeding_size = toGib(_r.group(2))

            # 完成数量
            html = etree.HTML(await websource.getHtml(f'https://u2.dmhy.org/getusertorrentlistajax.php?userid={uid}&type=completed'))
            xp = ''.join(html.xpath('//text()')[:2]).replace('\xad', '').replace('\xa0', '')
            if xp == "没有记录":
                completed_torrents_quantity = 0
                completed_torrents_size = 0
            else:
                _r = re.search(r'(\d+)条记录收藏量\s(.+)', xp)
                completed_torrents_quantity = int(_r.group(1))
                completed_torrents_size = toGib(_r.group(2))

            await self.sql.insertUsers({
                "Get_Time": nowTime(),
                "User_ID": uid,
                "User_Name": user_name,
                "Join_Date": join_date,
                "Last_Seen": last_seen,
                "Gender": gender,
                "User_Class": user_class,
                "Uploaded": uploaded,
                "Downloaded": downloaded,
                "Raw_Uploaded": raw_uploaded,
                "Raw_Downloaded": raw_downloaded,
                "UCoin": ucoin,
                "EXP": exp,
                "Seeding_Time": seeding_time,
                "Downloading_Time": downloading_time,
                "Torrent_Comments": torrent_comments,
                "Forum_Posts": forum_posts,
                "Uploaded_Torrents_Quantity": uploaded_torrents_quantity,
                "Uploaded_Torrents_Size": uploaded_torrents_size,
                "Currently_Seeding_Quantity": currently_seeding_quantity,
                "Currently_Seeding_Size": currently_seeding_size,
                "Completed_Torrents_Quantity": completed_torrents_quantity,
                "Completed_Torrents_Size": completed_torrents_size
            })

    async def postUsers(self, user_list):
        tb = pt.PrettyTable()
        tb.field_names = ["ID", "用户名", "时长", "平均做种数量", "平均做种体积", "获取时间"]
        for i, j in enumerate(user_list):

            # 自统计以来
            _s = await self.sql.selectUsersInfo(j['id'])
            if len(_s) == 0:
                self.logger.warning('#{} | 还没有产生数据'.format(j['id']))
                continue

            user_name = _s[-1]['User_Name']
            tnum = []  # 种子的数量
            tsize = []  # 种子的体积
            tnum_7day = []
            tsize_7day = []
            tnum_30day = []
            tsize_30day = []

            for s in _s:
                # 自统计以来
                tnum.append(s['Currently_Seeding_Quantity'])
                tsize.append(s['Currently_Seeding_Size'])

                if s['Get_Time'] >= otherDay(7):  # 7天内
                    tnum_7day.append(s['Currently_Seeding_Quantity'])
                    tsize_7day.append(s['Currently_Seeding_Size'])
                if s['Get_Time'] >= otherDay(30):  # 30天内
                    tnum_30day.append(s['Currently_Seeding_Quantity'])
                    tsize_30day.append(s['Currently_Seeding_Size'])

            tb.add_rows(
                [
                    [
                        j['id'], user_name, '自统计以来',
                        f'{round(average(tnum))} 个',
                        f'{round(average(tsize), 2)} GiB',
                        nowTime()
                    ],
                    [
                        j['id'], user_name, '30天内',
                        f'{round(average(tnum_30day))} 个',
                        f'{round(average(tsize_30day))} GiB',
                        nowTime()
                    ],
                    [
                        j['id'], user_name, '7天内',
                        f'{round(average(tnum_7day))} 个',
                        f'{round(average(tsize_7day))} GiB',
                        nowTime()
                    ],
                    [
                        j['id'], user_name, '当前',
                        f'{tnum[-1]} 个',
                        f'{round(tsize[-1])} GiB',
                        _s[-1]['Get_Time']
                    ]
                ]
            )

            if i + 1 != len(user_list):
                tb.add_row(['--------', '------------', '----------',
                           '------------', '------------', '--------------------'])
        print(tb)
        print('\n', end="")


def toGib(var) -> int:
    """ 统一单位为GiB """
    numeral = float(var.split(' ')[-2])
    unit = var.split(' ')[-1]

    if unit == 'PiB':
        return numeral * 1024 * 1024
    elif unit == 'TiB':
        return numeral * 1024
    elif unit == 'GiB':
        return numeral
    elif unit == 'MiB':
        return numeral / 1024
    else:
        return 0


def toMin(var) -> int:
    """ 统一单位为分 """
    var = var.replace(':  ', '').replace('\xad', '').replace('\xa0', '')
    minute = 0

    if '天' in var:
        day = int(var.split('天')[0])
        clock = var.split('天')[1]
        minute += day * 24 * 60
    else:
        clock = var

    minute += int(clock.split(':')[0]) * 60 + int(clock.split(':')[1])
    return minute


def average(data) -> float:
    """ 去除最小值和最大值，返回平均值 """
    if len(data) == 0:
        return 0
    if len(data) > 2:
        # 其实去了也白去
        data.remove(min(data))
        data.remove(max(data))
        average_data = float(sum(data))/len(data)
        return average_data
    elif len(data) <= 2:
        average_data = float(sum(data))/len(data)
        return average_data


def nowTime() -> str:
    """ 返回当前的时间 """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def otherDay(day):
    """ 传入天数，返回前几天的时间"""
    return datetime.datetime.now() - datetime.timedelta(days=day)
