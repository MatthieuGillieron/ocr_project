import streamlit as st
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
import re
import mysql.connector
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

def filter_results_by_confidence(results, confidence_threshold=0.5):
    return [res for res in results if res[1][1] > confidence_threshold]

def extract_info_with_conditions(results, index, pattern=None, suffix=None):
    for res in results[index:]:
        text = res[1][0]
        if pattern and not pattern.match(text):
            continue
        if suffix and not text.endswith(suffix):
            continue

        # Supprimer les caractères spéciaux (* par exemple) du résultat
        text = text.replace('*', '')

        return text
    return None

def id_exists_in_database(id_text):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='2007IFAGE',
        database='swiss_id_db'
    )

    cursor = connection.cursor()

    select_query = "SELECT * FROM swiss_table WHERE id = %s"
    cursor.execute(select_query, (id_text,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None

def extract_info_from_image(img_path):
    # Initialisation du modèle OCR
    ocr_model = PaddleOCR(lang='fr', use_gpu=False)

    result = ocr_model.ocr(img_path)

    filtered_result = filter_results_by_confidence(result[0])

    id_index = 0
    nom_index = 0
    prenom_index = 0
    date_naissance_index = 0

    # ID
    while True:
        id_text = extract_info_with_conditions(filtered_result, id_index, pattern=re.compile(r'^[ABCDEF]\d+$'))
        if id_text:
            break
        id_index += 1

    id_index += 1

    if id_exists_in_database(id_text):
        return None, None, None, None, True  # Signal pour indiquer une ID dupliquée

    # Nom
    while True:
        nom_text = extract_info_with_conditions(filtered_result, nom_index, suffix='*')
        if nom_text:
            break
        nom_index += 1

    nom_index += 1

    # Prénom
    while True:
        prenom_text = extract_info_with_conditions(filtered_result, prenom_index, suffix='*')
        if prenom_text and prenom_text != nom_text:
            break
        prenom_index += 1

    prenom_index += 1

    # Date de naissance
    while True:
        date_naissance_text = extract_info_with_conditions(filtered_result, date_naissance_index, pattern=re.compile(r'^\d+$'))
        if date_naissance_text:
            break
        date_naissance_index += 1

    date_naissance_index += 1

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='put ur password :))',
        database='swiss_id_db'
    )

    cursor = connection.cursor()

    insert_query = "INSERT INTO swiss_table (id, nom, prenom, date_naissance) VALUES (%s, %s, %s, %s)"
    data = (id_text, nom_text, prenom_text, date_naissance_text)

    cursor.execute(insert_query, data)

    connection.commit()

    cursor.close()
    connection.close()

    return id_text, nom_text, prenom_text, date_naissance_text, False

def main():
    st.title("Swiss ID")

    uploaded_file = st.sidebar.file_uploader("Choisissez une ID...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        with st.spinner('Traitement de l\'image...'):
            try:
                image = Image.open(uploaded_file)
                image_np = np.array(image)

                with ThreadPoolExecutor() as executor:
                    future = executor.submit(extract_info_from_image, image_np)
                    id_text, nom_text, prenom_text, date_naissance_text, duplicate_id = future.result()

                if id_text is not None:
                    st.write("Résultats OCR:")
                    st.write(f"ID: {id_text}")
                    st.write(f"Nom: {nom_text}")
                    st.write(f"Prénom: {prenom_text}")
                    formatted_date_naissance = datetime.strptime(date_naissance_text, "%d%m%y").strftime("%d.%m.%y")
                    st.write(f"Date de naissance: {formatted_date_naissance}")

                    st.image(image_np, caption='ID sélectionnée', use_column_width=True)

                if duplicate_id:
                    st.warning('ID déjà existante dans la base de données', icon="⚠️")
                elif id_text is None:
                    st.error('Une meilleure image est nécessaire', icon="🚨")
                else:
                    st.success('Traitement terminé!')
            except Exception as e:
                st.error(f"Erreur : {str(e)}", icon="🚨")

if __name__ == "__main__":
    main()
