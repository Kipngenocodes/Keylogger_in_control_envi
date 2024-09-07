import pandas as pd
import numpy as np
import re
import nltk

from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 1: Data Collection
# Replace 'phishing_email_dataset.csv' with the path to your dataset
# Step 1: Data Collection
# Use the full file path to ensure the dataset is correctly loaded
dataset = pd.read_csv(r'C:\Users\Admin Pc\Desktop\project_60\phishing_email_dataset.csv')
  

# Step 2: Data Preprocessing
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
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
    # Filtering words and Remove stopwords
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(filtered_words)

# Apply preprocessing
dataset['clean_text'] = dataset['email_text'].apply(preprocess_text)

# Step 3: Feature Extraction
# TF-IDF Vectorization for email content
vectorizer = TfidfVectorizer(max_features=5000)
X_text_features = vectorizer.fit_transform(dataset['clean_text'])

# URL and Sender Analysis
def extract_url_features(text):
    return re.findall(r'(https?://[^\s]+)', text)

def analyze_urls(urls):
    features = []
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        is_ip = re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$', domain) is not None
        domain_length = len(domain)
        num_subdomains = len(domain.split('.')) - 2
        features.append([is_ip, domain_length, num_subdomains])
    return np.mean(features, axis=0) if features else [0, 0, 0]

def extract_features(email):
    # Extract features from the email
    urls = extract_url_features(email)
    url_features = analyze_urls(urls)
    return np.array(url_features)  # Ensure it returns a NumPy array

# Combine features
X_additional_features = np.array(dataset['email_text'].apply(extract_features).tolist())
X = np.hstack([X_text_features.toarray(), X_additional_features])

# 'label' should have 0 (ham) and 1 (phishing)
y = dataset['label']

# Step 4: Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Model Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model and vectorizer
joblib.dump(model, 'phishing_model.pkl')  # Correct extension to .pkl
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

# Function to make a prediction without using a web framework
def predict_email(email_text):
    # Load the trained model and vectorizer
    model = joblib.load('phishing_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')

    # Preprocessing and extracting features from the input email
    features = extract_features(email_text)
    vectorized_text = vectorizer.transform([preprocess_text(email_text)])
    # Combine all features
    combined_features = np.hstack([vectorized_text.toarray(), features.reshape(1, -1)])

    # Predicting the email class
    prediction = model.predict(combined_features)
    return 'Phishing' if prediction[0] == 1 else 'Ham'

# Test the prediction function
if __name__ == '__main__':
    # Example email text input
    email_text = input("Enter the email text to classify: ")
    prediction_result = predict_email(email_text)
    print(f"The email is classified as: {prediction_result}")
