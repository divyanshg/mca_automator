from datetime import datetime

today = datetime.now().strftime('%b %d').replace(' ', ' ')

FROM_EMAIL = "avyukt.labs21@gmail.com"
FROM_PASSWORD = "iyax lowj lumd meix"
XLSX_FILE = f"data/Companies Registered {today}.xlsx"
TEMPLATE_FILE = "templates/template.html"
API_URL = "https://www.mca.gov.in/bin/MDSMasterDataServlet"