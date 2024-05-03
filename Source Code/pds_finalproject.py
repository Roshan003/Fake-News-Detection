# -*- coding: utf-8 -*-
"""PDS_FinalProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UarrK7XdlYbeWSyzK6zVR3cgTM0LH5As

# **Download and load the dataset**
"""

# Importing required packages

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import nltk
import re
import string
nltk.download('stopwords')

from collections import Counter
from wordcloud import WordCloud

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn.metrics import confusion_matrix

import gdown

# Define the file ID
file_id = '1x3o0pYEoJwqH2ThZItdfVHgc-DAiWtaD'

# Define the URL to download the file
url = f'https://drive.google.com/uc?id={file_id}'

# Define the output file name
output_file = 'news.csv'

# Download the file
gdown.download(url, output_file, quiet=False)

import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('news.csv')

# Display the first few rows of the DataFrame
print(data.head())

"""# **Exploratory data analysis**"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('news.csv')

# Define colors for real and fake bars
colors = ["blue", "orange"]

# Plot the distribution with specified colors
sns.countplot(data=data, x='label', palette=colors, hue='label', legend=False)
plt.xlabel('Data')
plt.ylabel('Count')
plt.title('Distribution of Real and Fake Data')

# Show the plot
plt.show()

data.columns

"""# **Preprocessing datasets**"""

#verifying if there are any null values in the dataset
data.isnull().sum()

import re
from nltk.corpus import stopwords
import string

# Initialize stopwords set and special characters to remove
stop_words = set(stopwords.words('english'))
special_characters = set(string.punctuation + string.digits)
to_remove = special_characters.union(stop_words)

def preprocess_text(text):
    if isinstance(text, str):  # Check if text is a string
        # Convert text to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+', '', text)

        # Remove special characters, digits, and stopwords
        text = " ".join([word for word in text.split() if word not in to_remove])

    return text


# Test the preprocessing function
example_text = "This is an  example text with some stopwords and special characters ! It also contains a URL : https://example.com"
print("Original Text:")
print(example_text)
print("\nPreprocessed Text:")
print(preprocess_text(example_text))

data['text'] = data['text'].apply(preprocess_text)
data['title'] = data['title'].apply(preprocess_text)

# Save the preprocessed dataset to a new CSV file
data.to_csv('preprocessed_news.csv', index=False)

# Display the preprocessed dataset
print(data.head())

"""# **Wordcloud**"""

# Load the preprocessed dataset
data = pd.read_csv('preprocessed_news.csv')

# Combine all text from real data
real_text = " ".join(data[data['label'] == 'REAL']['text'])

# Create a WordCloud object
wc = WordCloud(max_words=1500, width=1000, height=500, stopwords=set(stopwords.words('english')))

# Generate the word cloud
wc.generate(real_text)

# Plot the word cloud
plt.figure(figsize=(20, 20))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

# Convert all values in the 'text' column to strings
data['text'] = data['text'].astype(str)

# Combine all text from fake data
fake_text = " ".join(data[data['label'] == 'FAKE']['text'])

# Create a WordCloud object
wc = WordCloud(max_words=1500, width=1000, height=500, stopwords=set(stopwords.words('english')))

# Generate the word cloud
wc.generate(fake_text)

# Plot the word cloud
plt.figure(figsize=(20, 20))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

# Combine all text from real data
real_text = " ".join(data[data['label'] == 'REAL']['text'])

# Count the most common words in real news articles
real_words_count = Counter(real_text.split())
real_common_words = real_words_count.most_common(100)

# Extract the words and their counts
real_words = [word for word, count in real_common_words]
real_words_count = [count for word, count in real_common_words]

# Plot the top 100 most common words in real news articles
plt.figure(figsize=(20, 10))
plt.bar(real_words, real_words_count)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Words", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.title("Top 100 Most Common Words in Real News Articles", fontsize=16)
plt.show()

# Combine all text from fake data
fake_text = " ".join(data[data['label'] == 'FAKE']['text'])

# Count the most common words in fake news articles
fake_words_count = Counter(fake_text.split())
fake_common_words = fake_words_count.most_common(100)

# Extract the words and their counts
fake_words = [word for word, count in fake_common_words]
fake_words_count = [count for word, count in fake_common_words]

# Plot the top 100 most common words in fake news articles
plt.figure(figsize=(20, 10))
plt.bar(fake_words, fake_words_count)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Words", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.title("Top 100 Most Common Words in Fake News Articles", fontsize=16)
plt.show()

"""# **Feature Engineering**"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed dataset
data = pd.read_csv('preprocessed_news.csv')

# Drop rows with missing values in the 'text' column
data.dropna(subset=['text'], inplace=True)

# Split the dataset into features (X) and target variable (y)
X = data['text']
y = data['label']

# Convert text data into numerical features using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf_vectorizer.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Define the classifiers
classifiers = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "KNN": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": MultinomialNB()
}

# Train and evaluate each classifier
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    print(f"Classifier: {name}")
    print(f"Accuracy: {acc}")
    print(f"Confusion Matrix:\n{cm}\n")

    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', xticklabels=['Fake', 'Real'], yticklabels=['Fake', 'Real'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix - {name}')
    plt.show()

"""# **Predicting statements**"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load the preprocessed dataset
data = pd.read_csv('preprocessed_news.csv')

# Drop rows with missing values in the 'text' column
data.dropna(subset=['text'], inplace=True)

# Split the dataset into features (X) and target variable (y)
X = data['text']
y = data['label']

# Convert text data into numerical features using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf_vectorizer.fit_transform(X)

# Train the Logistic Regression classifier
classifier = LogisticRegression()
classifier.fit(X_tfidf, y)

# Save the trained classifier
with open('logistic_regression_model.pkl', 'wb') as file:
    pickle.dump(classifier, file)

# Take input from the user
statement = input("Enter a statement to predict: ")

# Preprocess the statement
statement_tfidf = tfidf_vectorizer.transform([statement])

# Predict using the trained classifier
prediction = classifier.predict(statement_tfidf)
print("Predicted label:", prediction[0])