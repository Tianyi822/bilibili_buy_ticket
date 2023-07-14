import json
import multiprocessing
import time
import typing
from datetime import datetime

import schedule
from playwright._impl._api_structures import SetCookieParam
from playwright.sync_api import sync_playwright

from config_component.class_define import Config

# 设置初始信号值
signal_value = 0


def buy_ticket(cookies: typing.List[SetCookieParam], robot_config, ticket_config):
    with sync_playwright() as playwright:
        # 启动一个 webkit
        browser = playwright.webkit.launch(headless=False)
        context = browser.new_context()
        # 添加 cookie
        context.add_cookies(cookies)
        # 开启一个新页面并跳转到指定网站
        page = context.new_page()
        page.goto(ticket_config['url'])
        # 设置日期
        page.get_by_text(ticket_config['date'], exact=True).click()
        # 设置票价
        page.get_by_text(ticket_config['value'], exact=True).click()
        # 点击购买
        page.get_by_text("立即购票", exact=True).click()
        # 点击付款按钮
        page.locator("div.confirm-paybtn").click()

        time.sleep(robot_config["sleep_time"])


def build_cookies_list(json_file_path: str):
    """
    构建 cookie 对象
    :param json_file_path:
    :return:
    """
    with open(json_file_path) as json_file:
        json_objs = json.loads(json_file.read())

    cookies = []
    for obj in json_objs:
        cookies.append(
            SetCookieParam(
                name=obj['name'],
                value=obj['value'],
                domain=obj['domain'],
                path=obj['path'],
            )
        )

    return cookies


def run(cookies, robot_config, ticket_config):
    # 进程个数根据 robot 配置进行设置
    processes = []
    for _ in range(robot_config["process_num"]):
        p = multiprocessing.Process(target=buy_ticket, args=(cookies, robot_config, ticket_config))
        processes.append(p)
        p.start()

    # 等待所有进程完成
    for p in processes:
        p.join()

    global signal_value
    signal_value = 5


if __name__ == '__main__':
    # 加载 cookies.json 文件
    cookies = build_cookies_list('comic_con/cookies.json')

    # 加载票务配置文件
    ticket_config = Config("comic_con/ticket_config.ini").get_content("beijing_comic_con")

    # 加载脚本配置文件
    robot_config = Config("comic_con/robot.ini").get_content("base_config")

    # 计算延迟时间，并在指定时间执行函数
    now = datetime.now()
    # 获取开票时间
    start_time = datetime.strptime(robot_config["start_time"], "%Y-%m-%d %H:%M:%S")
    delay_time = start_time - now
    schedule.every().day.at((now + delay_time).strftime("%H:%M:%S")).do(run, cookies, robot_config, ticket_config)

    while True:
        schedule.run_pending()
        time.sleep(1)
        if signal_value == 5:
            break

    time.sleep(robot_config["process_num"] * robot_config["sleep_time"])
