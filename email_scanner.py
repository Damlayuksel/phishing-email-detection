"""
PHISHING EMAIL SCANNER — Real-time Detection

SETUP (one-time):
─────────────────
1. Run the notebook and execute the last cell to save the model.

2. Create a .env file in the same folder with this content:
      EMAIL=your_email@gmail.com
      APP_PASSWORD=xxxx xxxx xxxx xxxx

3. Get Gmail App Password:
   → https://myaccount.google.com/apppasswords
   → Select Mail → Generate → Copy the 16-character password

4. Run: python email_scanner.py
"""

import imaplib
import email
import re
import joblib
import os
from email.header import decode_header
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
EMAIL        = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
IMAP_SERVER  = "imap.gmail.com"
SCAN_LIMIT   = 10


def load_model():
    if not os.path.exists("phishing_model.pkl"):
        print("ERROR: phishing_model.pkl not found.")
        print("Please run the notebook first and execute the 'Save Model' cell.")
        exit(1)
    model      = joblib.load("phishing_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    print("Model loaded successfully.\n")
    return model, vectorizer


def preprocess(text):
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    for pkg in ['stopwords', 'punkt', 'punkt_tab']:
        try:
            nltk.data.find(f'tokenizers/{pkg}' if 'punkt' in pkg else f'corpora/{pkg}')
        except LookupError:
            nltk.download(pkg, quiet=True)
    stemmer    = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    text = str(text).lower()
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = word_tokenize(text)
    tokens = [stemmer.stem(t) for t in tokens if t and t not in stop_words]
    return ' '.join(tokens)


def extract_phishing_features(text):
    from scipy.sparse import csr_matrix
    t = str(text).lower()
    return csr_matrix([[
        int(bool(re.search(r'urgent|immediately|expire|limited|act now|asap', t))),
        int(bool(re.search(r'free|win|winner|prize|cash|offer|discount|reward|gift', t))),
        int(bool(re.search(r'verify|password|login|account|confirm|validate', t))),
        int(bool(re.search(r'suspend|block|arrest|penalty|lawsuit|closed|disabled', t))),
        int(bool(re.search(r'dear (customer|user|friend|sir|madam|member|winner)', t))),
        int(bool(re.search(r'http\S+|www\.\S+|click here', text, re.I))),
    ]])


def predict_email(text, model, vectorizer):
    from scipy.sparse import hstack
    combined = hstack([vectorizer.transform([preprocess(text)]),
                       extract_phishing_features(text)])
    return model.predict(combined)[0]


def decode_subject(subject):
    decoded = decode_header(subject)[0]
    if isinstance(decoded[0], bytes):
        return decoded[0].decode(decoded[1] or 'utf-8', errors='ignore')
    return decoded[0]


def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            body = ""
    return body


def scan_emails():
    if not EMAIL or not APP_PASSWORD:
        print("ERROR: EMAIL or APP_PASSWORD not found in .env file.")
        print("Create a .env file with:")
        print("  EMAIL=your_email@gmail.com")
        print("  APP_PASSWORD=xxxx xxxx xxxx xxxx")
        return

    model, vectorizer = load_model()

    print(f"Connecting to Gmail ({EMAIL})...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    mail.select("inbox")
    _, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()[-SCAN_LIMIT:]

    print(f"Scanning last {len(email_ids)} emails...\n")
    print("─" * 65)

    phishing_count = 0
    for eid in reversed(email_ids):
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg     = email.message_from_bytes(msg_data[0][1])
        sender  = msg.get("From", "Unknown")
        subject = decode_subject(msg.get("Subject", "(No Subject)"))
        body    = get_email_body(msg)
        result  = predict_email(f"{subject} {body}", model, vectorizer)

        if "Phishing" in result:
            icon = "PHISHING"
            phishing_count += 1
        else:
            icon = "SAFE    "

        print(f"[{icon}]  From: {sender[:35]:<35}  |  {subject[:30]}")

    print("─" * 65)
    print(f"\nScan complete: {len(email_ids)} emails checked, {phishing_count} phishing detected.")
    mail.logout()


if __name__ == "__main__":
    scan_emails()
