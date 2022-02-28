# -*- coding: utf-8 -*-

import os
from loguru import logger
import logging
# import datetime
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from score import get_config
import score.global_var as gol
from score.global_var import set_value
from score.global_var import get_value
from score.websource import WEBSOURCE
from score.sql import SQL
from unit.users import Users

if __name__ == "__main__":
    gol._init()  # 初始化全局变量
    set_value('abs_path', os.path.split(os.path.realpath(__file__))[0])
    config = get_config.config()  # 读取配置文件
    set_value('config', config)  # 将配置文件存入全局变量
    set_value('logger', logger)  # 将LOG函数存入全局变量
    set_value('websource', WEBSOURCE())
    set_value('sql', SQL())

    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }

    job_defaults = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 60
    }

    scheduler = AsyncIOScheduler(
        job_defaults=job_defaults, timezone='Asia/Shanghai')

    # 提高schedule的日志等级
    logging.getLogger('apscheduler.scheduler').setLevel(level=logging.ERROR)

    logger.add(level='DEBUG',
               sink=os.path.join(get_value('abs_path'),
                                 f'{config.log_path_name}/', config.log_file_name),
               rotation='00:00',
               retention='30 days',
               encoding='utf-8')

    users = Users()

    scheduler.add_job(func=users.run, trigger='interval', minutes=15)

    scheduler.start()

    logger.info(
        'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        loop_forever = asyncio.new_event_loop()
        coro = asyncio.get_event_loop().run_forever()
        future = asyncio.run_coroutine_threadsafe(coro, loop_forever)
    except (KeyboardInterrupt, SystemExit):
        pass
