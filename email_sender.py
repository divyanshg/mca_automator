import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import TEMPLATE_FILE, SMTP_USER, SMTP_PASSWORD, SMTP_ENDPOINT, FROM_EMAIL

# def generateMail(company_name):
#     with open(TEMPLATE_FILE, 'r') as file:
#         body = file.read()

#     return body.replace("{{company_name}}", company_name)

def send_email(to_email, body, subject, uid):
    # body = generateMail(company_name)
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add tracking pixel
    tracking_pixel = f'<img src="http://localhost:3000/assets/{uid}" height="60" width="200" style="margin-left: -12px; margin-bottom: 16px; margin-top:24px;">'
    body_with_tracker = body.replace("{{av_logo}}", tracking_pixel)

    msg.attach(MIMEText(body_with_tracker, 'html'))

    try:
        server = smtplib.SMTP(SMTP_ENDPOINT, 587)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()

        return {
            "body": body.replace("{{av_logo}}", ""),
            "subject": subject
        }
    except Exception as e:
        raise e
