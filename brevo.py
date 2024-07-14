from xlsx_handler import filter_xlsx
from api_handler import fetch_company_data
from email_sender import send_email
from config import XLSX_FILE
import pandas as pd
from tqdm import tqdm
import time
import sys
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(2)).strftime('%d-%b-%Y').upper()
updated_xlsx_file = f"updated_companies {yesterday}.csv"

EMAILS_PER_MINUTE = 2
EMAILS_PER_HOUR = 120
TIME_PER_EMAIL = 30  # Seconds per email

def main():
    filtered_data = filter_xlsx(XLSX_FILE)
    
    try:
        with tqdm(total=len(filtered_data)) as pbar:
            for index, row in filtered_data.iterrows():
                start_time = time.time()
                
                company_data = fetch_company_data(row['CIN'])

                if company_data and 'emailAddress' in company_data:
                    email_address = company_data['emailAddress']
                    # email_address = "manyabhati21@gmail.com"
                    send_email(email_address, company_data["company"])
                    filtered_data.at[index, 'email'] = email_address

                pbar.update(1)

                # Calculate time elapsed and sleep accordingly
                time_elapsed = time.time() - start_time
                if time_elapsed < TIME_PER_EMAIL:
                    time.sleep(TIME_PER_EMAIL - time_elapsed)
                
                # Check if we've sent 60 emails (1 hour worth)
                if (index + 1) % EMAILS_PER_HOUR == 0:
                    print(f"\nSent {EMAILS_PER_HOUR} emails. Pausing for the rest of the hour...")
                    time_to_next_hour = 3600 - ((index + 1) * TIME_PER_EMAIL % 3600)
                    time.sleep(time_to_next_hour)

        filtered_data.to_excel(updated_xlsx_file, index=False)

    except KeyboardInterrupt:
        print("\n\nInterrupted...")
        filtered_data.to_csv(updated_xlsx_file, index=False)
        sys.exit(1)

if __name__ == "__main__":
    main()