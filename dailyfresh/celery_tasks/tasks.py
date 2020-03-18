from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import os
import django

# 任务处理者一端的django初始化
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 我们这里案例使用redis作为broker
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8 ')


# 创建任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送邮件信息"""
    # 发送邮件
    subject = '天天生鲜欢迎信息'
    message = ''
    html_message = '<h1>%s,欢迎您成为天天呢生鲜的注册会员</h1>请点击下方链接激活账户<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    sender = settings.EMAIL_FROM
    receiver = [to_email]

    send_mail(subject, message, sender, receiver, html_message=html_message)