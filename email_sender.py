import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
from config import TEMPLATE_FILE, FROM_EMAIL, FROM_PASSWORD

def generateMail(company_name):
    with open(TEMPLATE_FILE, 'r') as file:
        body = file.read()

    return body.replace("{{company_name}}", company_name)

def send_email(to_email, company_name):
    body = generateMail(company_name)
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = f"Professional Website Development for {company_name}"

    # Add tracking pixel
    # encoded_email = urllib.parse.quote(to_email)
    # tracking_pixel = f'<img src="https://pixel-server-377e.onrender.com/pixel?email={encoded_email}" width="1" height="1" style="display:none;">'
    # body = body.replace("{{pixel_tracker}}", tracking_pixel)

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
