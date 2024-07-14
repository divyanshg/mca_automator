from email_sender import send_email
import pandas as pd
import time
import sys
from datetime import datetime
from tqdm import tqdm
from config import TEMPLATE_FILE

EMAILS_PER_MINUTE = 30
EMAILS_PER_HOUR = 1800
TIME_PER_EMAIL = 1  # Seconds per email

def generateMail(company, state, activity):
    with open(TEMPLATE_FILE, 'r') as file:
        body = file.read()

    return body.replace("{{company_name}}", company).replace("{{state}}", state).replace("{{activity}}", activity)

def mail_data(db, mongoClient):
    contactsCollection = db['contacts']
    mailsCollection = db['mails']
    
    try:
        # Fetch records where email_sent is False
        contacts = list(contactsCollection.find({"mailingStage": 0}))

        with tqdm(total=len(contacts)) as progressBar:
            for index, contact in enumerate(contacts):
                if contact.get('email'):
                    start_time = time.time()
                    
                    # Start a session for the transaction
                    with mongoClient.start_session() as session:
                        # Start a transaction
                        with session.start_transaction():
                            try:
                                #create a mail
                                newMail = mailsCollection.insert_one({
                                    "contactId": contact["_id"],
                                }, session=session)

                                new_mail_id = newMail.inserted_id

                                #send mail
                                subject = f"Grow Your Online Presence in {contact["state"]}"
                                body = generateMail(contact["company_name"], contact["state"], contact["activity"])

                                sent_mail = send_email(contact['email'], body, subject, str(new_mail_id))
                                
                                # Update the mailingStage flag if email is successfully sent
                                contactsCollection.update_one(
                                    {"_id": contact["_id"]},
                                    {"$set": {
                                        "mailingStage": 1
                                    }},
                                    session=session  # Use the session for this operation
                                )

                                #update the mail to include further details
                                mailsCollection.update_one({
                                    "_id": new_mail_id,
                                    "contactId": contact["_id"]
                                    }, {
                                        "$set": {
                                            "body": sent_mail["body"],
                                            "subject": sent_mail["subject"],
                                            "sentAt": datetime.now(),
                                            "mailType": 1
                                        }
                                    },
                                    session=session
                                )

                                # If both operations are successful, commit the transaction
                                session.commit_transaction()

                            except Exception as e:
                                # If an error occurs, abort the transaction
                                session.abort_transaction()

                    progressBar.update(1)

                    # Calculate time elapsed and sleep accordingly
                    time_elapsed = time.time() - start_time
                    if time_elapsed < TIME_PER_EMAIL:
                        time.sleep(TIME_PER_EMAIL - time_elapsed)
                
                    # Check if we've sent 60 emails (1 hour worth)
                    if (index + 1) % EMAILS_PER_HOUR == 0:
                        print(f"\nSent {EMAILS_PER_HOUR} emails. Pausing for the rest of the hour...")
                        time_to_next_hour = 3600 - ((index + 1) * TIME_PER_EMAIL % 3600)
                        time.sleep(time_to_next_hour)

    except KeyboardInterrupt:
        print("\n\nInterrupted...")
        sys.exit(1)