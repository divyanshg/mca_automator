from datetime import datetime

today = datetime.now().strftime('%b %d').replace(' ', ' ')

XLSX_FILE = f"data/Companies Registered {today}.xlsx"
TEMPLATE_FILE = "templates/template.html"
API_URL = "https://www.mca.gov.in/bin/MDSMasterDataServlet"

MONGO_URL="mongodb+srv://divyanshg809:6crURmeUaXju6ki7@iotcluster.l5ehf.gcp.mongodb.net/?appName=iotCluster"
DATABASE_NAME="avyukt-auto-mailer"

SMTP_ENDPOINT="email-smtp.ap-south-1.amazonaws.com"
SMTP_USER = "AKIA47CRXEGATZBVPLO3"
SMTP_PASSWORD = "BM2UtUgfE7Xxqg397Hslo0ec6glZIOCXg1vW/1MkX2mX"

FROM_EMAIL="divyansh@avyuktlabs.in"