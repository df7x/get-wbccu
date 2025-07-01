import datetime
from typing import Callable

import httpx
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

import config
import demo


class DailyGreeter:
    """
    每日定时问候服务
    功能：
    1. 基于网络时间每天00:00:20准时触发
    2. 自动处理时区转换
    3. 提供自定义回调功能
    """

    def __init__(self, timezone: str = 'Asia/Shanghai'):
        """
        初始化服务
        :param timezone: 时区字符串，默认上海时区
        """
        self.timezone = pytz.timezone(timezone)
        self.scheduler = BlockingScheduler(timezone=timezone)
        self.client = httpx.Client()  # 复用HTTP客户端

    def _get_network_time(self) -> datetime.datetime:
        """
        获取网络时间（内部方法）
        :return: 带时区的datetime对象
        """
        try:
            resp = self.client.head("http://www.tencent.com", follow_redirects=True)
            if 'date' in resp.headers:
                return datetime.datetime.strptime(
                    resp.headers['date'],
                    '%a, %d %b %Y %H:%M:%S GMT'
                ).replace(tzinfo=pytz.UTC).astimezone(self.timezone)
        except Exception as e:
            print(f"[警告] 网络时间获取失败: {e}")
        return datetime.datetime.now(self.timezone)

    def set_daily_task(self,
                       task: Callable[[datetime.datetime], None],
                       hour: int = config.default_time[0],
                       minute: int = config.default_time[1],
                       second: int = config.default_time[2]):
        """
        设置每日定时任务
        :param task: 接收当前时间作为参数的回调函数
        :param hour: 定时小时（默认0）
        :param minute: 定时分钟（默认0）
        :param second: 定时秒数（默认20）
        """

        def wrapped_task():
            current_time = self._get_network_time()
            task(current_time)

        self.scheduler.add_job(
            wrapped_task,
            'cron',
            hour=hour,
            minute=minute,
            second=second,
            misfire_grace_time=60
        )

    def run(self):
        """启动服务（阻塞式运行）"""
        print(f"启动每日定时服务，时区: {self.timezone.zone}")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.shutdown()

    def shutdown(self):
        """停止服务"""
        self.client.close()
        self.scheduler.shutdown()
        print("服务已停止")


# 预置快捷函数
def simple_hello():
    """默认的hello输出函数"""

    def _greeter(current_time: datetime.datetime):
        print(f"本次任务执行时间：[{current_time.strftime('%Y-%m-%d %H:%M:%S')}]")
        demo.start_get_wbccu()

    service = DailyGreeter()
    service.set_daily_task(_greeter)
    service.run()


simple_hello()
