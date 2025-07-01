import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password):
    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # 邮件正文
    message.attach(MIMEText(body, 'html'))

    try:
        # 连接到SMTP服务器
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 启用 TLS 加密
            server.login(login, password)  # 登录 SMTP 服务器
            server.sendmail(from_email, to_email, message.as_string())  # 发送邮件
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

# 使用示例
# subject = "这是一封来自 Python 的测试邮件。"
# body = """
# <!DOCTYPE html><html><head><style>*{padding:0;margin:0}img{width:100%}.div{display:grid;grid-template-columns:1fr 1fr 1.5fr;border:1px solid;align-items:center}.div:nth-child(even){background-color:#ccc}.div:nth-child(odd){background-color:#aaa}span{font-size:12px;font-family:微软雅黑;text-align:center}</style></head><body><div class="div"><img src="https://media.robertsspaceindustries.com/iaps0ps9oo83s/product_thumb_medium_and_small.jpg"><span class="name">Prowler</span><span>440$&nbsp;-&nbsp;410$&nbsp;=&nbsp;30$</span></div></body></html>
# """
# to_email = "2117960965@qq.com"
# from_email = "dongfang_qisu@163.com"
# smtp_server = "smtp.163.com"
# smtp_port = 25
# login = "dongfang_qisu@163.com"
# password = "LYbuDxj4kZxicRNe"
#
# send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password)
