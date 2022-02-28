# -*- coding: utf-8 -*-

import re
import aiohttp
import asyncio
# from score.global_var import set_value
from score.global_var import get_value


class WEBSOURCE():
    def __init__(self):
        self.logger = get_value('logger')
        self.config = get_value('config')
        self.session = None
        # self.cookie = None
        # self.server_session = None

    def check302(self, url, html):
        main_link = re.search(
            r'''(https?://[\w\.]+?/).*''', url, flags=re.I).group(1)
        _re_t = re.search(
            r'''<script type=["']text/javascript["']>window\.location\.href = ['"](.+?)['"];</script>''', html, flags=re.I)
        if _re_t:
            url_302 = '{}{}'.format(main_link, _re_t.group(1))
            return url_302
        else:
            return None

    async def getHtml(self, url):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        for i in range(1, 21):
            try:
                cookie = self.config.cookie
                headers = {'User-Agent': self.config.useragent}
                timeout = aiohttp.ClientTimeout(
                    total=80, sock_connect=15, sock_read=45)
                proxy = self.config.proxies

                async with self.session.get(url, headers=headers, cookies=cookie, proxy=proxy, timeout=timeout) as resp:
                    if resp.status < 400:
                        text = await resp.text(errors='ignore')
                        _r = self.check302(url, text)
                        return await self.gethtml(_r) if _r is not None else text
                    else:
                        self.logger.error(
                            f'aiohttp 状态码不正确<{resp.status}> | 3秒后重试... | {url}')
                        await asyncio.sleep(1)
            except asyncio.TimeoutError as e:
                self.logger.error(f'aiohttp 超时 | 3秒后重试... | {url} | {e}')
                await asyncio.sleep(3)
                continue
            except Exception as e:
                self.logger.error(f'打开网页发生未知错误！ | 3秒后重试... | {url} | {e}')
                await asyncio.sleep(3)
                continue
        return None
