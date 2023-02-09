import smtplib
from email.message import EmailMessage

FROM_EMAIL = "andraszollai.mail@gmail.com" #"zozo.mailtest@yahoo.com"
FROM_PASSW = "eaazhtpytzdjoxju"#"just$for$test"
TO_EMAIL = "andrszollai@gmail.com"

class Email:
    def sendEmail(subject:str,message:str):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        msg = EmailMessage()

        message = f'{message}\n'
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        #server.send_message(msg)
        server.login(FROM_EMAIL,FROM_PASSW)
        server.sendmail(FROM_EMAIL,TO_EMAIL,"Test")
        print("Message sent")


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, message):
    password = FROM_PASSW
    my_email = FROM_EMAIL  # needs to be changed
    smtp_obj = smtplib.SMTP('smtp.mail.yahoo.com', 465)
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login(my_email, password)
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()
    print("Message sent")