from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from flask_login import current_user
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jakehopkins/Documents/Flask_Test/flask_test/img-to-docs-450117-078405c7be8a copy.json"


# Load credentials
SERVICE_ACCOUNT_FILE = "flask_test/img-to-docs-450117-078405c7be8a copy.json"
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialize Google Docs and Drive API services
docs_service = build("docs", "v1", credentials=credentials)
drive_service = build("drive", "v3", credentials=credentials)

# Create a new Google Doc
# document = docs_service.documents().create(body={"title": "New Flask Doc"}).execute()
document_id = "1Nq9OTr-sQrkNvkGD3LjTJzjfrWv6XUmSL8Ycx1Ko4JU"

# print(f"New document created: https://docs.google.com/document/d/{document_id}/edit")

def add_text(text):
    """Adds text to the Google Doc."""
    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": text + "\n"
            }
        }
    ]
    
    docs_service.documents().batchUpdate(
        documentId=document_id,  # Fix: Use the correct document ID
        body={"requests": requests}
    ).execute()

    print(f"Text added to document: {text}")

def share_google_doc():
    """Shares the Google Doc with your email."""
    user_email = current_user.email
    permission = {
        "type": "user",
        "role": "writer",
        "emailAddress": user_email,
        "pendingOwner": "true" #doesn't work, need oAuth 
    }
    
    drive_service.permissions().create(
        fileId=document_id,  # Fix: Use the correct document ID
        body=permission,
        sendNotificationEmail=True,
        # pendingOwner=True
    ).execute()

    print(f"Document shared: https://docs.google.com/document/d/{document_id}/edit")

# Example usage



def update_title(new_title):
    body = {"name": new_title}
    drive_service.files().update(
        fileId=document_id,
        body=body
    ).execute()
    print("Document title updated to:", new_title)
