import pytesseract
from PIL import Image
import re

def extract_text_from_image(image: Image.Image) -> str:
    text = pytesseract.image_to_string(image, lang='fra')
    return text


def extract_kyc_data(text: str) -> dict:
    # Initialiser tous les champs à vide
    data = {
        "type_personne": "Inconnu",
        "siren": "",
        "date_immatriculation": "",
        "nom_entreprise": "",
        "forme_juridique": "",
        "capital_social": "",
        "adresse_siege": "",
        "nom_prenom": "",
        "date_naissance": "",
        "nationalite": "",
        "adresse_personnelle": "",
        "adresse_etablissement": "",
        "activite": "",
        "date_debut_activite": "",
        "mode_exploitation": "",
    }

    lines = text.splitlines()
    cleaned_text = "\n".join([l.strip() for l in lines if l.strip()])

    # Détection du type
    if "IDENTIFICATION DE LA PERSONNE MORALE" in cleaned_text.upper():
        data["type_personne"] = "Morale"

        data["siren"] = re.search(r"Immatriculation.*?(\d{3} ?\d{3} ?\d{3})", cleaned_text)
        data["date_immatriculation"] = re.search(r"Date d'immatriculation\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", cleaned_text)
        data["nom_entreprise"] = re.search(r"Dénomination ou raison sociale\s*[:\-]?\s*(.+)", cleaned_text)
        data["forme_juridique"] = re.search(r"Forme juridique\s*[:\-]?\s*(.+)", cleaned_text)
        data["capital_social"] = re.search(r"Capital social\s*[:\-]?\s*([\d\s\.,]+ EUROS?)", cleaned_text)
        data["adresse_siege"] = re.search(r"Adresse du siège\s*[:\-]?\s*(.+)", cleaned_text)

    elif "IDENTIFICATION DE LA PERSONNE PHYSIQUE" in cleaned_text.upper():
        data["type_personne"] = "Physique"

        data["siren"] = re.search(r"Immatriculation.*?(\d{3} ?\d{3} ?\d{3})", cleaned_text)
        data["date_immatriculation"] = re.search(r"Date d'immatriculation\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", cleaned_text)
        data["nom_prenom"] = re.search(r"Nom, prénoms\s*[:\-]?\s*(.+)", cleaned_text)
        data["date_naissance"] = re.search(r"Date et lieu de naissance\s*[:\-]?\s*(.+)", cleaned_text)
        data["nationalite"] = re.search(r"Nationalité\s*[:\-]?\s*(.+)", cleaned_text)
        data["adresse_personnelle"] = re.search(r"Domicile personnel\s*[:\-]?\s*(.+)", cleaned_text)

    # Commun à tous
    data["adresse_etablissement"] = re.search(r"Adresse de l’établissement\s*[:\-]?\s*(.+)", cleaned_text)
    data["activite"] = re.search(r"Activité\(s\) exercée\(s\)\s*[:\-]?\s*(.+)", cleaned_text)
    data["date_debut_activite"] = re.search(r"Date de commencement d’activité\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", cleaned_text)
    data["mode_exploitation"] = re.search(r"Mode d’exploitation\s*[:\-]?\s*(.+)", cleaned_text)

    # Nettoyage final
    for k, v in data.items():
        if isinstance(v, re.Match):
            data[k] = v.group(1).strip()
        elif not isinstance(v, str):
            data[k] = ""

    return data
