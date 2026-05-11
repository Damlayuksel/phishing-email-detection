# Phishing Email Detection Using NLP

> Detecting phishing emails with Natural Language Processing and Machine Learning

---

## Overview

This project builds an automated phishing email detection system using classical NLP techniques and machine learning algorithms. The model classifies emails as **Phishing** or **Safe** by analyzing both the text content and cybersecurity-specific linguistic patterns used by attackers.

---

## Dataset

- **Source:** [Kaggle — Spam Email Dataset](https://www.kaggle.com/datasets/jackksoncsie/spam-email-dataset)
- **Size:** 18,634 real emails
- **Classes:** Safe Email / Phishing Email

---

## Methodology

### 1. Text Preprocessing
| Step | Description |
|------|-------------|
| Lowercasing | Convert all text to lowercase |
| URL Removal | Strip http/www links |
| Punctuation Removal | Keep alphabetic characters only |
| Tokenization | Split text into individual words |
| Stop-word Removal | Remove low-information words (the, is, your…) |
| Porter Stemming | Reduce words to root form |

### 2. Feature Extraction
- **TF-IDF Vectorization** — Term Frequency x Inverse Document Frequency, captures phishing-specific word importance
- **6 Phishing-Specific Features:**

| Feature | Keywords |
|---------|----------|
| Urgency | urgent, immediately, expire, asap |
| Money Words | free, win, prize, cash, offer, reward |
| Credential | verify, password, login, account, confirm |
| Threat | suspend, block, arrest, penalty |
| Spam Greeting | Dear Customer, Dear Winner |
| Has Link | URL or "click here" present |

### 3. Classification Models
- Multinomial Naive Bayes
- Logistic Regression
- Linear SVM *(best model)*

---

## Results

| Model | Accuracy | F1-Score | Precision | Recall |
|-------|----------|----------|-----------|--------|
| Naive Bayes | 96.1% | 92.1% | 94.5% | 89.8% |
| Logistic Regression | 97.0% | 94.2% | 95.8% | 92.7% |
| **Linear SVM** | **99.2%** | **98.3%** | **99.1%** | **97.5%** |

### Comparison with Previous Work

| Study | Method | Accuracy |
|-------|--------|----------|
| Chandrasekaran (2006) | Rule-based SVM | ~95% |
| Abu-Nimeh (2007) | Multiple ML classifiers | ~94-95% |
| Prakash (2010) | URL + Content analysis | ~95% |
| Fette et al. (2007) | Random Forest (PILFER) | 99.5% |
| **This Work** | **Linear SVM + TF-IDF** | **99.2%** |

> Note: Direct comparison is difficult as different studies used different datasets.

---

## How to Run

**1. Install dependencies:**
```bash
pip install pandas numpy scikit-learn nltk matplotlib seaborn scipy
```

**2. Download the dataset from Kaggle:**
```
https://www.kaggle.com/datasets/jackksoncsie/spam-email-dataset
```
Place `emails.csv` in the same folder as the notebook.

**3. Open the notebook:**
```bash
jupyter notebook spam_classification.ipynb
```

**4. Run all cells:**
```
Cell -> Run All
```

---

## Project Structure

```
phishing-email-detection/
│
├── spam_classification.ipynb   # Main notebook
├── email_scanner.py            # Optional: scan your real Gmail inbox
└── README.md
```

---

## Live Demo

At the end of the notebook, you can test the model with your own email:

```python
predict("URGENT: Your account will be suspended. Verify at http://bit.ly/secure")
# Result: PHISHING

predict("Hi team, the meeting is rescheduled to Friday at 2pm.")
# Result: SAFE
```

---

## Email Scanner (Optional)

To scan your real Gmail inbox, use `email_scanner.py`:

**1. Install extra dependency:**
```bash
pip install python-dotenv
```

**2. Create a `.env` file:**
```
EMAIL=your_email@gmail.com
APP_PASSWORD=xxxx xxxx xxxx xxxx
```

**3. Get Gmail App Password:**
- Go to: https://myaccount.google.com/apppasswords
- Select Mail -> Generate -> Copy the 16-character password

**4. Run:**
```bash
python email_scanner.py
```

> The `.env` file is never uploaded to GitHub — your credentials stay local.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-orange)
![NLTK](https://img.shields.io/badge/NLTK-3.9-green)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)

---

## Author

**Damla Yuksel**
2025–2026
