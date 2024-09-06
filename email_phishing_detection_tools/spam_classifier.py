import pandas as pd
import numpy as np
import re
import nltk    
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# stp 1: collecting the data to be analysed 
#  the data is stored in from of CSV file
# replacing 'phishing_email_dataset.csv' with the path to dataset
dataset= pd.read_csv('phishing_email_dataset.csv')


# step 2: preprocessing dataset 
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Function to preprocess email text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()    
    # Remove the punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # fltering words  and Remove stopwords
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]  
    return ' '.join(filtered_words)

# applying the  preprocessing
dataset['email_text'] = dataset['email_text'].apply(preprocess_text)


# step 3: Feature Extraction
# TF-IDF Vectorization for email content
vectorizer = TfidfVectorizer(max_features=5000)
X_text_features = vectorizer.fit_transform(dataset['clean_text'])


    
