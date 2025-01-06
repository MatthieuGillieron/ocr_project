# OCR POUR EXTRACTION DE DONNÉES DES ID SUISSES

Spécialement conçu pour extraire des données à partir de cartes d'identité suisses. Optimisé pour gérer diverses qualités de photos et conditions d'éclairage, en se concentrant sur l'extraction précise des informations telles que :

- Nom
- Prénom
- Date de naissance
- Numéro d'identification de la carte

Les données extraites sont automatiquement stockées dans une base de données MySQL pour faciliter leur gestion et leur accès.


## 🖼️ Aperçu Visuel

Les résultats obtenus sont volontairement flouttés :

### 📋 Image avec Extraction Réussie
![Exemple d'ID Valide](images/idOk.png)



### ⚠️ Image avec doublons
![Exemple d'ID Non Valide](images/idNok.png)



## 🛠️ Fonctionnalités Principales

- **Gestion des Qualités de Photo** : Traitement des images de qualité variable pour améliorer la reconnaissance sous différents éclairages.
- **Extraction de Données Personnelles** : Identification précise et fiable des informations critiques.
- **Précision Optimisée** : Entraînement sur un ensemble de données étendu pour des résultats plus précis.
- **Stockage Structuré** : Sauvegarde des données extraites dans une base MySQL pour un accès et une gestion simplifiés.
- **Adaptabilité** : Compatible avec les cartes d'identité suisses. 

##  💻 Technologies

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)  
Le langage principal utilisé

[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white&style=for-the-badge)](https://opencv.org/)  
 Pour le traitement et la manipulation des images

[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-0073CF?style=for-the-badge)](https://github.com/PaddlePaddle/PaddleOCR)  
Un framework avancé et rapide pour l’OCR

[![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white&style=for-the-badge)](https://www.mysql.com/)  
Utilisé pour stocker toutes les données extraites

<br>
( PS : Quand j’ai créé ce projet, j’étais encore en plein apprentissage et je n’avais pas encore pensé à faire un fichier requirements.txt pour installer les dépendances automatiquement. Du coup, si vous voulez tester le projet, il faudra installer les packages à la main) :(  

