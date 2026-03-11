import smtplib
from email.message import EmailMessage
from config.constants.index import mail_id, mail_password
from utils.errors.index import InternalServerError

def send_mail(otp : str, to : str) :
    msg = EmailMessage()
    msg.set_content(f"OTP : {otp}")

    msg['Subject'] = "Testing Email Verification"
    msg['From'] = mail_id
    msg['To'] = to

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(mail_id, mail_password)
            s.send_message(msg)
            print("Success!")

    except Exception as e:
        raise InternalServerError(e.args[0])
