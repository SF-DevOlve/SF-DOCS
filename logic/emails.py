import os
import sys

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

import joblib
from collections import Counter
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import np
import re
import string
import dns.resolver


def preprocess_text(text):
  """
  Preprocesses text data for machine learning models.

  Args:
      text (str): The text to preprocess.

  Returns:
      str: The preprocessed text.
  """

  # Lowercase the text
  text = text.lower()

  # Remove punctuation (adjust based on your needs)
  text = re.sub(r'[^\w\s]', '', text)

  # Remove stop words (optional, depends on your task)
  # from nltk.corpus import stopwords
  # stop_words = stopwords.words('english')
  # text = [word for word in text.split() if word not in stop_words]

  # Stemming or lemmatization (optional)
  # from nltk.stem import PorterStemmer
  # stemmer = PorterStemmer()
  # text = ' '.join([stemmer.stem(word) for word in text.split()])

  # Remove extra whitespace
  text = re.sub(r'\s+', ' ', text)

  return text

def is_valid_email(email):
    # Regular expression to check email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

def domain_exists(domain):
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    
# Load the models
models : list = [
    joblib.load('models-ai/emails/ComplementNBClassifier.joblib'),
    joblib.load('models-ai/emails/MultinomialNBClassifier.joblib'),
    joblib.load('models-ai/emails/BernoulliNBClassifier.joblib'),
    # joblib.load('models/emails/AdaBoostClassifier.joblib'),
    # joblib.load('models/emails/BernoulliNBClassifier.joblib'),
    # joblib.load('models/emails/ComplementNBClassifier.joblib'),
    # joblib.load('models/emails/RandomForestClassifier.joblib'),
    # joblib.load('models/emails/SGDClassifier.joblib'),
]

models_n:list = [
    joblib.load('models-ai/emails/AdaBoostClassifier.joblib'),
    joblib.load('models-ai/emails/BernoulliNBClassifier.joblib'),
    joblib.load('models-ai/emails/ComplementNBClassifier.joblib'),
    joblib.load('models-ai/emails/RandomForestClassifier.joblib'),
    joblib.load('models-ai/emails/SGDClassifier.joblib')
]

def predict_email_body_phishing(data, models=models):
  predictions = []
  vectorizer = joblib.load('models-ai/emails/tfidf_vectorizer.joblib')
  for idx,model in enumerate(models):
    if idx <3:
        predictions.append(model.predict(vectorizer.transform(data))[0])
    else:
        pass

  
  # Count occurrences of each prediction (works for classification and regression)
  prediction_counts = Counter(list(predictions))
  # Handle potential ties for the most frequent prediction
  most_common_key = prediction_counts.most_common(1)[0][0]

  # Return the key with the maximum count
  return 0 if int(most_common_key)==1 else 1


def check_email_domain(email):
    try:
        domain=email.split('@')[1]
        if not is_valid_email(email):
            return False
        return domain_exists(domain)
    except:
        return False


if __name__== "__main__":
    vectorizer = joblib.load('models-ai/emails/tfidf_vectorizer.joblib')
    print(predict_email_body_phishing(["re : 6 . 1100 , disc : uniformitarianism , re : 1086 ; sex / lang dick hudson 's observations on us use of 's on ' but not 'd aughter ' as a vocative are very thought-provoking , but i am not sure that it is fair to attribute this to "" sons "" being "" treated like senior relatives "" . for one thing , we do n't normally use ' brother ' in this way any more than we do 'd aughter ' , and it is hard to imagine a natural class comprising senior relatives and 's on ' but excluding ' brother ' . for another , there seem to me to be differences here . if i am not imagining a distinction that is not there , it seems to me that the senior relative terms are used in a wider variety of contexts , e . g . , calling out from a distance to get someone 's attention , and hence at the beginning of an utterance , whereas 's on ' seems more natural in utterances like ' yes , son ' , ' hand me that , son ' than in ones like ' son ! ' or ' son , help me ! ' ( although perhaps these latter ones are not completely impossible ) . alexis mr"], models))
    print(models_n[0].predict(vectorizer.transform([preprocess_text("re : 6 . 1100 , disc : uniformitarianism , re : 108")])))








