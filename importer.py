from xlsx_handler import filter_xlsx
from api_handler import fetch_company_data
from tqdm import tqdm
import sys
from config import XLSX_FILE
import time

#MAILING STAGE:
# 0 - Email Not Sent
# 1 - First Reach Done
# 2 - First Follow up Done
# 3 - Second Follow up Done
# 4 - Breakup Done

def remove_duplicates(arr, key):
    seen = set()
    result = []
    for obj in arr:
        value = obj.get(key)
        if value not in seen:
            seen.add(value)
            result.append(obj)
    return result


def import_data(db):
    collection = db['contacts']
    
    filtered_data = filter_xlsx(XLSX_FILE)
    batch = []
    
    try:
        with tqdm(total=len(filtered_data)) as pbar:
            for index, row in filtered_data.iterrows():
                start_time = time.time()
                
                company_data = fetch_company_data(row['CIN'])
                
                data_entry = {
                    "cin": row['CIN'],
                    "company_name": row['COMPANY NAME'],
                    "state": row['STATE'],
                    "activity": row['ACTIVITY DESCRIPTION'],
                    "doi": row["DATE OF INCORPORATION"],
                    "email": company_data.get('emailAddress', None),
                    "mailingStage": 0,
                    "inCommunication": False
                }
                
                batch.append(data_entry)

                if len(batch) == 50:
                    cleaned_batch = remove_duplicates(batch, "cin")
                    collection.insert_many(cleaned_batch)
                    batch.clear()
                
                pbar.update(1)

                time.sleep(2)

        # Insert any remaining data in the batch
        if batch:
            cleaned_batch = remove_duplicates(batch, "cin")
            collection.insert_many(cleaned_batch)
        print("Contacts imported and saved to MongoDB")

    except KeyboardInterrupt:
        print("\n\nInterrupted...")
        sys.exit(1)