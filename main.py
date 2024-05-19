import streamlit as st
from logic.emails import predict_email_body_phishing, check_email_domain, is_valid_email,predict_email_body_phishing_from_models
from logic.phishing_site_urls import predict_url_phishing,predict_url_phishing_from_models
from logic.dns_ import check_phishing_dns
from voice.main import base64_to_audio_segment, Data
from llm.main import get_translation_from_language_to_english
from documents.main import get_emails_urls_from_pages_contents_from, extract_emails_and_urls
import speech_recognition as sr
import pyttsx3
import io
from pydub import AudioSegment
import base64
import uuid
import shutil
from pathlib import Path
import os
import sqlite3

import io

# Helper functions
def handle_email_body_phishing(email_body: str):
    # email_body = get_translation_from_language_to_english(email_body)
    prediction = predict_email_body_phishing_from_models([email_body])
    return prediction

# Helper function to handle email structure phishing prediction
def handle_email_structure_phishing(email: str):
    return {"phishing": 0 if check_email_domain(email) else 1}

# Helper function to handle URL phishing prediction
def handle_url_phishing(url: str, local_dns_resolution: str):
    prediction = predict_url_phishing(url)
    dns_phishing = 0 if check_phishing_dns(url, local_dns_resolution) else 1
    return {"phishing": prediction, "dns_phishing": dns_phishing}

# Helper function to handle PDF phishing detection
def handle_pdf_phishing(pdf_file):
    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)
    pdf_id = str(uuid.uuid4())
    pdf_path = temp_dir / f"{pdf_id}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.read())
    urls, emails = get_emails_urls_from_pages_contents_from(str(pdf_path))
    emails_with_phishing = [email for email in emails if not is_valid_email(email) or not check_email_domain(email)]
    urls_with_phishing = [url for url in urls if predict_url_phishing(url)]
    pdf_path.unlink()
    return {"phishing": 1 if emails_with_phishing or urls_with_phishing else 0,"emails": emails_with_phishing, "urls": urls_with_phishing}

# Function to create SQLite database and run SQL file
def create_database():
    # Check if the database already exists
    if os.path.exists("vishing.db"):
        return
    
    # Create a new SQLite database
    conn = sqlite3.connect("vishing.db")
    cursor = conn.cursor()

    # Run an existing SQL file to create tables and populate data
    with open("vishing.sql", "r") as f:
        sql_script = f.read()
        cursor.executescript(sql_script)

    # Commit changes and close connection
    conn.commit()
    conn.close()
create_database()

# Function to fetch data from SQLite database
def fetch_data(langue):
    conn = sqlite3.connect("vishing.db")
    cursor = conn.cursor()

    if langue == "fr":
        cursor.execute("SELECT * FROM orders")
    elif langue == "ar":
        cursor.execute("SELECT * FROM orders_ar")

    rows = cursor.fetchall()
    hotwords = [row[1].split(",") for row in rows]
    category_names = [row[2] for row in rows]
    orders = [row[3] for row in rows]

    conn.close()
    return hotwords, category_names, orders

# Function to detect voice phishing
def detect_voice_phishing(audio_data, langue):
    recognizer = sr.Recognizer()
    text_speech = pyttsx3.init()

    if langue.lower() == "francais":
        langue = "fr"
    elif langue.lower() == "anglais":
        langue = "en"
    elif langue.lower() == "arabe":
        langue = "ar"
    else:
        raise ValueError("Langue non prise en charge")

    try:
        text = recognizer.recognize_google(audio_data, language=langue)
    except sr.UnknownValueError:
        raise ValueError(f"Désolé, je n'ai pas compris le son en {langue}")
    except sr.RequestError:
        raise ValueError(f"Désolé, le service est actuellement indisponible en {langue}")

    hotwords, category_names, _ = fetch_data(langue)

    matched_categories = []
    matched_category_names = set()

    for i, hotword_list in enumerate(hotwords):
        for hotword in hotword_list:
            if hotword in text.lower():
                category_name = category_names[i]
                if category_name not in matched_category_names:
                    matched_categories.append({"category_name": category_name})
                    matched_category_names.add(category_name)
                    break

    if matched_categories:
        return {
            "langue": langue,
            "text": text.lower(),
            "matched_categories": matched_categories,
        }
    else:
        return {
            "matched_categories": [],
            "langue": langue,
            "text": text.lower(),
            "provider": "google",
        }



# Main app structure
st.title("Phishing Detection App")

# Sidebar navigation
pages = ["Challenge details","Email Body Phishing Check", "Email Structure Phishing Check","URL Pharming Check", "URL Phishing Check", "PDF Phishing Check", "Voice Phishing Check"]
page = st.sidebar.selectbox("Choose a page", pages)

if page == "Challenge details":
    # Title and subtitle
    st.title("HACKATHON-ENSET-2024")
    st.subheader("Thème : L'IA au Service de la Cybersécurité")
    st.write('**Sujet :** "Intelligence Artificielle contre les Cyber-Menaces : Vers une Détection Parfaite du Phishing"')

    # Challenge description
    st.header("Description")
    st.write("""
    Ce challenge propose de développer un système automatisé utilisant l'intelligence artificielle
    pour détecter les e-mails et sites de phishing, tout en alertant les utilisateurs en temps réel.
    Les participants devront créer une solution capable d'analyser les e-mails entrants et les URL
    afin d'identifier les signes de phishing, tels que les liens suspects, les pièces jointes
    malveillantes et le texte trompeur, en utilisant des techniques de machine learning.
    """)

    # Problem statement
    st.header("I. Problématique")
    st.write("""
    La montée en puissance des cyber-attaques, en particulier le phishing, menace la sécurité
    des informations personnelles et des actifs organisationnels. Comment l'intelligence
    artificielle peut-elle être exploitée pour identifier et neutraliser ces menaces de manière
    proactive et efficace ?
    """)

    # Objectives
    st.header("II. Objectifs")
    st.write("""
    1. **Développement d'un modèle d'IA :** Créer un modèle d'intelligence artificielle capable de
    détecter les tentatives de phishing avec une précision élevée.
    2. **Interface utilisateur :** Concevoir une interface intuitive pour visualiser et interagir avec les
    données de détection.
    3. **Rapidité et efficacité :** Garantir que la solution est rapide et fonctionne en temps réel pour
    contrer les attaques.
    """)

    # Solution functionalities
    st.header("III. Fonctionnalités de la solution")
    st.write("""
    1. **Détection en temps réel :** Analyse continuelle des e-mails et des sites web pour identifier
    les signaux de phishing.
    2. **Apprentissage automatique :** Adaptation du système en fonction des nouvelles techniques
    de phishing identifiées.
    3. **Tableau de bord interactif :** Visualisation des alertes de sécurité, des statistiques de
    détection, et gestion des fausses alertes.
    4. **Rapports détaillés :** Génération automatique de rapports décrivant les tentatives de
    phishing détectées et les actions prises.
    """)


    # Deliverables
    st.header("IV. Les livrables")
    st.write("""
    Les livrables doivent être déposés dans la Classroom avec les liens vers les dépôts GitHub.
    [Lien vers Classroom](https://classroom.google.com/c/NjgzODc5NDAzOTEy?cjc=t2frsvg)
    1. **Code source :** Ensemble complet du code développé pendant le hackathon.
    2. **Documentation :** Explication des choix technologiques, architecture du système, et guide
    utilisateur.
    3. **Démo du produit :** Prototype fonctionnel de la solution avec une démonstration de la
    détection de phishing.
    4. **Présentation finale :** Support de présentation résumant le travail réalisé, les résultats
    obtenus, et les perspectives d'amélioration.
    """)

    # Presentation details
    st.header("V. Présentation")
    st.write("""
    Chaque équipe disposera de 8 minutes pour présenter leur solution devant un jury. La
    présentation devra inclure :
    1. **Introduction :** Brève description du problème et de la solution proposée.
    2. **Démonstration :** Montrez comment votre solution fonctionne avec des exemples concrets.
    3. **Résultats :** Mettez en avant les performances de votre modèle et les bénéfices de votre
    interface utilisateur.
    4. **Conclusion :** Récapitulez les points forts de votre projet et discutez des améliorations
    futures possibles.
    """)

    # Notes for participants
    st.header("Notes pour les participants")
    st.write("""
    **Technologies recommandées :** Python, TensorFlow, Keras, scikit-learn, Flask/Django pour
    l'interface web.
    **Sources de données :** Utilisation de bases de données publiques de phishing (par exemple,
    OpenPhish, PhishTank, kaggle) pour l'entraînement des modèles.
    **Critères d'évaluation :** Précision du modèle, convivialité de l'interface utilisateur, innovation
    dans l'approche, qualité de la présentation finale.
    """)

    st.write("Bonne chance à toutes les équipes et que le meilleur projet gagne !")


elif page == "Email Body Phishing Check":
    st.header("Email Body Phishing Check")

    # Simple Definition
    st.subheader("Definition")
    st.write("Email body phishing detection involves analyzing the content of an email to determine if it contains phishing attempts, which are fraudulent attempts to obtain sensitive information by disguising as a trustworthy entity.")

    # Link to Dataset
    st.subheader("Dataset")
    st.markdown("[Link to the Kaggle dataset used for training](https://www.kaggle.com/datasets/subhajournal/phishingemails)")  # Replace with actual URL

    # Architecture and Model
    st.subheader("Model Architecture and Performance")
    st.image("docs/images/email-phishing.jpeg", caption="Phishing Email Architecture", use_column_width=True)
    st.write("The following models were used in training and their performance is summarized in the table below:")
    
    model_data = {
        "Model": ["Gaussian Naive Bayes", "Multinomial Naive Bayes", "Bernoulli Naive Bayes","Random Forest","Decision Tree","AdaBoost","SGD","Logistic Regression"],
        "Accuracy": [88.2, 83.5, 96.7,93.61,89.19,92.45,98.08,97.19]
    }
    
    st.table(model_data)

    st.subheader("Test")
    email_body = st.text_area("Enter email body")
    if st.button("Check Email Body Phishing"):
        result=handle_email_body_phishing(email_body)
        st.json(result)


elif page == "URL Phishing Check":
    st.header("URL Phishing Check")

    # Simple Definition
    st.subheader("Definition")
    st.write("URL phishing detection involves analyzing a URL to determine if it is a phishing attempt, where attackers disguise malicious websites as legitimate ones to trick users into providing sensitive information.")

    # Link to Dataset (if applicable)
    st.subheader("Dataset")
    st.markdown("[Link to the Kaggle dataset used for training](https://www.kaggle.com/datasets/mohamedouledhamed/phishing-site-urls)")  # Replace with actual URL

    # Architecture and Model (if applicable)
    st.subheader("Model Architecture and Performance")

    st.image("docs/images/url-phishing.jpeg", caption="Phishing Url Architecture", use_column_width=True)
    st.image("docs/images/ANN.jpeg", caption="Phishing Url ANN Architecture", use_column_width=True)
    st.write("The following models were used in training and their performance is summarized in the table below:")
    
    model_data = {
        "Model": ["Logistic Regression", "K-Nearest Neighbors", "Gaussian NB","Decision Tree","Random Forest","Artificial Neural Network"],
        "Accuracy": [75.7, 80.45, 74.71,82.01,82.60,81.3]
    }
    
    st.table(model_data)
    # Test
    st.subheader("Test")
    url = st.text_input("Enter URL")
    if st.button("Check URL Phishing"):
        result = predict_url_phishing_from_models(url)
        st.json(result)



elif page == "Email Structure Phishing Check":
    st.header("Email Structure Phishing Check")
    
    # Definition and how it works
    st.subheader("What is Email Structure Phishing Check?")
    st.write("""
    Email structure phishing check involves analyzing the structure of an email address to determine if it is likely to be used for phishing. This check includes:
    1. **Email Structure Validation**: Ensuring the email format is correct.
    2. **Domain Existence Check**: Verifying if the domain name of the email address actually exists.
    """)
    
    # Email structure phishing check
    st.subheader("Test")
    email = st.text_input("Enter email address")
    if st.button("Check Email Structure Phishing"):
        result = handle_email_structure_phishing(email)
        st.json(result)



# URL Pharming Check Page
elif page == "URL Pharming Check":
    st.header("URL Pharming Check")
    
    # Definition and how it works
    st.subheader("What is URL Pharming?")
    st.write("""
    URL pharming is a type of cyber attack where an attacker redirects a website's traffic to a fraudulent website by compromising the DNS (Domain Name System) server or by modifying the hosts file on a victim's computer. The attacker's goal is to steal sensitive information such as login credentials, financial details, or personal information.
    
    In a URL pharming attack, the attacker typically replaces the IP address associated with a legitimate website domain with the IP address of a malicious website. This can be done by exploiting vulnerabilities in the DNS infrastructure or by tricking users into visiting a malicious website through phishing emails or fraudulent links.
    """)
    
    # URL pharming check
    st.subheader("Test")
    url = st.text_input("Enter URL")
    local_dns_resolution = st.text_input("Enter Local DNS Resolution (IP address)")
    if st.button("Check URL Pharming"):
        result = handle_url_phishing(url, local_dns_resolution)
        st.json(result)

elif page == "PDF Phishing Check":
    st.header("PDF Phishing Check")

    # Simple Definition
    st.subheader("Definition")
    st.write("PDF phishing detection involves analyzing the content of a PDF document to extract emails and URLs, and then checking each one for potential phishing attempts.")

    # How it works
    st.subheader("How it Works")
    st.write("""
    1. **Upload PDF**: Upload the PDF document that you want to check for phishing.
    2. **Check PDF Phishing**: Click the button to start the phishing check process.
    3. **Result**: The result will show if any malicious or phishing emails or URLs were found in the PDF document.
    """)

    # Test
    st.subheader("Test")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file and st.button("Check PDF Phishing"):
        result = handle_pdf_phishing(pdf_file)
        st.json(result)


elif page == "Voice Phishing Check":
    st.header("Voice Phishing Check")
    
    # Definition and how it works
    st.subheader("What is Voice Phishing (Vishing)?")
    st.write("""
    Voice phishing, also known as vishing, is a type of social engineering attack where attackers use voice communication (such as phone calls or VoIP) to trick individuals into providing sensitive information or performing actions that compromise security.
    
    In a vishing attack, attackers often impersonate legitimate entities (such as banks, government agencies, or tech support) to gain the trust of their targets and persuade them to reveal personal information, login credentials, or financial details.
    """)
    st.subheader("Architectue")
    st.image("docs/images/voice-phishing.jpeg", caption="Voice Phishing Architecture", use_column_width=True)
    
    # Voice phishing check
    st.subheader("Test")
    st.write("Record an audio clip of a suspected vishing attempt and upload it here:")
    audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
    
    if audio_file and st.button("Check Voice Phishing"):
        audio_data = audio_file.read()
        result = detect_voice_phishing(audio_data, "francais")
        st.json(result)














