import pickle
import re
import pandas as pd
import nltk
import numpy as np

from docx_to_text import docx_to_text
from pdf_to_text import convert_to_text

file_name = "home-loan-sample1.pdf"
nltk.download('stopwords')
nltk.download('punkt')


# file_name = "100-Original-Resumes/"+actual_file_name
# try:
#     content_text = convert_to_text(file_name)
# except:
#     try:
#         content_text = docx_to_text(file_name)
#     except:
#         print("unsupported file")

def extract_loan_amt(content_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(content_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    x = re.findall('[0-9].+[/-]', content_text)
    if x:
        return str(x[0][:-2])
    else:
        return 0


def extract_gender(content_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(content_text)
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i] == "Sex":
            if filtered_tokens[i + 1] == 'Male':
                return 1
            else:
                return 0
        if i > 500:
            return 0


def extract_status(content_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(content_text)
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i] == "Status":
            if filtered_tokens[i + 1] == "Married":
                return 1
            else:
                return 0
        if i > 500:
            return 0


def extract_education(content_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(content_text)
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i] == "Graduate":
            if filtered_tokens[i + 1] == "yes":
                return 0
            else:
                return 1
        if i > 500:
            return 0


def extract_dependent(content_text):
    word_tokens = nltk.tokenize.word_tokenize(content_text)
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalnum()]
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i] == "dependents":
            return str(filtered_tokens[i + 3])
        if i > 800:
            return '0'


def extract_employment(content_text):
    word_tokens = nltk.tokenize.word_tokenize(content_text)
    # remove the punctuation
    filtered_tokens = content_text.split()
    for i in range(len(filtered_tokens)):
        if filtered_tokens[i] == "Self-employed":
            if filtered_tokens[i + 1] == "yes":
                return 1
            elif filtered_tokens[i + 1] == "no":
                return 0
        if i > 800:
            return 0


def extract_loan_term(content_text):
    x = content_text.find('Tenure in Months')
    words = content_text[x:].split()
    try:
        return str(words[3])
    except:
        return 0


def extract_app_income(content_text):
    x = content_text.find('Gross income')
    words = content_text[x:].split()
    try:
        return str(words[2])
    except:
        return 0


def extract_coapp_income(content_text):
    content_text = content_text[content_text.find('Co-applicant'):]
    x = content_text.find('Net Annual Income')
    words = content_text[x:].split()
    try:
        return str(words[4])
    except:
        return 0


def predict_approval(file_name):
    print(file_name)
    d = {1: "Accepted :)", 0: "Rejected :("}
    content_text = ""
    try:
        content_text = convert_to_text(file_name)
    except:
        try:
            content_text = docx_to_text(file_name)
        except:
            print("unsupported file")
    model_file_name = 'Final_Loan_Model.sav'
    model = pickle.load(open(model_file_name, 'rb'))

    loan_amt = extract_loan_amt(content_text)
    gender = extract_gender(content_text)
    marital_status = extract_status(content_text)
    graduation = extract_education(content_text)
    dependents = extract_dependent(content_text)
    employment = extract_employment(content_text)
    loan_term = extract_loan_term(content_text)
    app_income = extract_app_income(content_text)
    coapp_income = extract_coapp_income(content_text)
    credit_history = 1
    print(loan_amt)
    print(loan_term)
    print(gender)
    print(marital_status)
    print(graduation)
    print(dependents)
    print(employment)
    print(app_income)
    print(coapp_income)
    row_l = pd.DataFrame({'Gender': [1], "Married": [0], 'Dependents': [0], 'Education': [1], 'Self_Employed': [0],
                          'ApplicantIncome': [4895], 'CoapplicantIncome': [0], "LoanAmount": [102],
                          "Loan_Amount_Term": [360], 'Credit_History': [1]})
    # print(row_l)
    # prediction = model.predict([row_l])
    classID = 0
    # if prediction[0] == 1:
    #     classID = 1
    return d[classID]

# Dependents	ApplicantIncome	CoapplicantIncome	LoanAmount	Loan_Amount_Term	Mal
