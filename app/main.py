import streamlit as st
import pandas as pd
from PIL import Image
from ocr import extract_text_from_image, extract_kyc_data
from utils import calculate_risk_score, display_deepseek_analysis, display_risk_assessment


def display_results(text, kyc_data, use_llm, api_key):
    """Handle all result display logic"""
    with st.expander("Voir le texte brut OCR"):
        st.text_area("Texte OCR", text, height=200, label_visibility="collapsed")
    
    # Section des données extraites
    st.subheader("Données KYC structurées")
    df = pd.DataFrame.from_dict(kyc_data, orient='index', columns=['Valeur'])
    df = df[df['Valeur'] != ""]
    st.dataframe(df, use_container_width=True, column_config={"index": "Champ", "Valeur": "Valeur détectée"})
    
    # Analyse de risque
    st.subheader("Analyse de risque")
    risk_score, risk_factors = calculate_risk_score(kyc_data)
    display_risk_assessment(risk_score, risk_factors)
    
    # Analyse avancée
    if use_llm and api_key:
        display_deepseek_analysis(kyc_data, api_key)
    

# Configuration de la page
st.set_page_config(
    page_title="KYC Automatisé", 
    layout="centered",
    page_icon=":bar_chart: KYC Automatisé"
)

# Titre avec style amélioré
st.title("Analyse automatique de document KYC")
st.markdown("""
    <style>
        .big-font { font-size:18px !important; }
        .risk-high { color: #ff4b4b; font-weight: bold; }
        .risk-medium { color: #f4b136; font-weight: bold; }
        .risk-low { color: #0f9d58; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Sidebar pour les paramètres
with st.sidebar:
    st.header("Paramètres")
    use_llm = st.checkbox("Utiliser l'analyse avancée (DeepSeek)", value=True)
    if use_llm:
        deepseek_api_key = st.text_input("Clé API DeepSeek", type="password")
        st.info("L'analyse avancée peut prendre quelques secondes.")

# Zone de téléchargement
uploaded_file = st.file_uploader(
    "Téléversez une image de KBIS ou carte d'identité", 
    type=["png", "jpg", "jpeg", "pdf"],
    help="Formats acceptés : PNG, JPG, JPEG, PDF"
)

if uploaded_file:
    try:
        # Affichage du document
        col1, col2 = st.columns(2)
        image = Image.open(uploaded_file) if uploaded_file.type != "application/pdf" else Image.open("pdf_first_page.png")
        
        with col1:
            st.image(image, caption="Document importé", use_column_width=True)
            
        # Extraction OCR
        with st.status("Extraction et analyse des données...", expanded=True) as status:
            st.write("Extraction du texte...")
            text = extract_text_from_image(image)
            
            st.write("Analyse des données KYC...")
            kyc_data = extract_kyc_data(text)
            status.update(label="Analyse terminée!", state="complete", expanded=False)
        
        # Afficher les résultats
        display_results(text, kyc_data, use_llm, deepseek_api_key)
        
    except Exception as e:
        st.error(f"Une erreur est survenue: {str(e)}")
