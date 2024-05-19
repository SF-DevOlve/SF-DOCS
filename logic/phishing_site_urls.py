
import os
import sys

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from urllib.parse import urlparse
import re
import joblib
import numpy as np
import random
from collections import Counter
from keras.models import load_model

from urllib.parse import urlparse
import re

def abnormal_url(URL):
    """
    Checks if the URL is abnormal or not.

    Args:
        URL (str): The URL to be checked.

    Returns:
        int: Returns 1 if the URL is abnormal, 0 otherwise.
    """
    hostname = urlparse(URL).hostname
    hostname = str(hostname)
    match = re.search(hostname, URL)
    if match:
        return 1
    else:
        return 0



#Use of IP or not in domain
def having_ip_address(URL: str) -> int:
    """
    Checks if the URL contains an IP address.

    Args:
        URL (str): The URL to check.
        
    Returns:
        int: Returns 1 if the URL contains an IP address, 0 otherwise.
    """
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', URL)  # Ipv6
    if match:
        # print match.group()
        return 1
    else:
        # print 'No matching pattern found'
        return 0
    

def sum_count_special_characters(URL: str) -> int:
    """
    Counts the number of special characters in a URL.

    Args:
        URL (str): The URL to count the special characters from.
        
    Returns:
        int: The number of special characters in the URL.
    """
    special_chars = ['@','?','-','=','.','#','%','+','$','!','*',',','//']

    num_special_chars = sum(char in special_chars for char in URL)
    return num_special_chars


def httpSecured(URL: str) -> int:
    htp = urlparse(URL).scheme
    match = str(htp)
    if match == 'https':
        # print match.group()
        return 1
    else:
        # print 'No matching pattern found'
        return 0

def letter_count(URL: str) -> int:
    letters = 0
    for i in URL:
        if i.isalpha():
            letters = letters + 1
    return letters

def digit_count(URL: str) -> int:
    digits = 0
    for i in URL:
        if i.isnumeric():
            digits = digits + 1
    return digits



def Shortining_Service(URL):
    match = re.search(
                      'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      URL)
    if match:
        return 1
    else:
        return 0

def get_url(url):
    url = url.replace('www.', '')
    url_len = len(url)
    letters_count = letter_count(url)
    digits_count  = digit_count(url)
    special_chars_count = sum_count_special_characters(url)
    shortened = Shortining_Service(url)
    abnormal = abnormal_url(url)
    secure_https = httpSecured(url)
    have_ip = having_ip_address(url)
    parsed_url  = urlparse(url)
    
    return {
        'url_len': url_len,
        'letters_count': letters_count,
        'digits_count': digits_count,
        'special_chars_count': special_chars_count,
        'shortened': shortened,
        'abnormal': abnormal,
        'secure_http': secure_https,
        'have_ip': have_ip
    }






def predict_url_phishing(url):
    rf_model = joblib.load('models-ai/urlss/Classifier_RandomForest.joblib')
    decision_tree_model = joblib.load('models-ai/urlss/DecisionTreeClassifier.joblib')
    knn_model = joblib.load('models-ai/urlss/KNeighborsClassifier.joblib')
    ann_model = load_model('models-ai/urlss/ANNClassifier.h5')

    numerical_values = get_url(url)
    predictions:list = [
        rf_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0],
        decision_tree_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0],
        knn_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0],
        int(ann_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0][0])
    ]
    prediction_counts = Counter(list(predictions))
    # Handle potential ties for the most frequent prediction
    # Get the most common key (the key with the maximum count)
    most_common_key = prediction_counts.most_common(1)[0][0]

    # Return the key with the maximum count
    return 0 if int(most_common_key)==1 else 1


def predict_url_phishing_from_models(url):
    numerical_values = get_url(url)
    rf_model = joblib.load('models-ai/urlss/Classifier_RandomForest.joblib')
    decision_tree_model = joblib.load('models-ai/urlss/DecisionTreeClassifier.joblib')
    knn_model = joblib.load('models-ai/urlss/KNeighborsClassifier.joblib')
    ann_model = load_model('models-ai/urlss/ANNClassifier.h5')
    predictions:list = [
        int(rf_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0]),
        int(decision_tree_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0]),
        int(knn_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0]),
        int(ann_model.predict(np.array(list(numerical_values.values())).reshape(1, -1))[0][0])
    ]
    prediction_counts = Counter(list(predictions))
    # Handle potential ties for the most frequent prediction
    # Get the most common key (the key with the maximum count)
    most_common_key = prediction_counts.most_common(1)[0][0]


    return {
        "phishing": 0 if int(most_common_key)==1 else 1,
        "Random Forest": 0 if predictions[0]==1 else 1,
        "Decision Tree": 0 if predictions[1]==1 else 1,
        "K Nearest Neighbors": 0 if predictions[2]==1 else 1,
        "Artificial Neural Network": 0 if predictions[3]==1 else 1
    }


if __name__ == "__main__":
    print(predict_url_phishing("super1000.info/docs"))












