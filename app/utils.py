import datetime
import requests
import streamlit as st
from typing import Tuple, List

def analyze_with_deepseek(prompt: str, api_key: str) -> str:
    """Function to call DeepSeek API for analysis"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 300
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erreur DeepSeek API: {str(e)}")
        return None

def calculate_risk_score(kyc_data: dict) -> Tuple[int, List[str]]:
    """Calculate risk score based on KYC data"""
    risk_score = 0
    risk_factors = []
    
    # Analyse de l'âge de l'entreprise
    if kyc_data.get("date_immatriculation"):
        try:
            immat_date = datetime.datetime.strptime(kyc_data["date_immatriculation"], "%d/%m/%Y")
            age = (datetime.datetime.today() - immat_date).days // 365
            
            if age < 1:
                risk_score += 2
                risk_factors.append("entreprise récente (<1 an)")
            elif age < 3:
                risk_score += 1
                risk_factors.append("entreprise jeune (<3 ans)")
        except:
            pass
    
    # Analyse du capital social
    if kyc_data.get("capital_social"):
        try:
            capital = float(kyc_data["capital_social"].split()[0].replace(",", "."))
            if capital < 1000:
                risk_score += 1
                risk_factors.append("capital social faible (<1k€)")
        except:
            pass
    
    return risk_score, risk_factors

def display_risk_assessment(risk_score: int, risk_factors: List[str]):
    """Display risk assessment with proper styling"""
    if risk_score == 0:
        risk_class = "risk-low"
        risk_label = "FAIBLE"
    elif risk_score == 1:
        risk_class = "risk-medium"
        risk_label = "MODÉRÉ"
    else:
        risk_class = "risk-high"
        risk_label = "ÉLEVÉ"
    
    st.markdown(f"""
        <div style='border-radius: 0.5rem; padding: 1rem; margin: 1rem 0;'>
            <h4 style='margin-top: 0;'>Score de risque: <span class='{risk_class}'>{risk_label}</span></h4>
            {f"<p>Facteurs de risque: {', '.join(risk_factors)}</p>" if risk_factors else "<p>Aucun facteur de risque significatif détecté</p>"}
        </div>
    """, unsafe_allow_html=True)

def display_deepseek_analysis(kyc_data: dict, api_key: str):
    """Handle DeepSeek analysis display"""
    st.subheader("Analyse avancée avec DeepSeek")
    with st.spinner("Analyse en cours avec DeepSeek..."):
        try:
            prompt = f"""
            Analyse ce document KYC et donne une évaluation professionnelle:
            - Type: {kyc_data.get('type_personne', 'Inconnu')}
            - Nom: {kyc_data.get('nom_entreprise') or kyc_data.get('nom_prenom', 'Inconnu')}
            - SIREN: {kyc_data.get('siren', 'Non fourni')}
            - Date immatriculation: {kyc_data.get('date_immatriculation', 'Inconnue')}
            - Activité: {kyc_data.get('activite', 'Non spécifiée')}
            
            Fais une analyse concise (3-5 points max) des risques potentiels et des vérifications recommandées.
            Réponds en français sous forme de liste à puces.
            """
            
            analysis = analyze_with_deepseek(prompt, api_key)
            if analysis:
                st.markdown(analysis)
        except Exception as e:
            st.error(f"Erreur lors de l'analyse DeepSeek: {str(e)}")