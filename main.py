import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pricing_logic import calculate_price

# Authentifizierung laden
with open('auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# NEUE VERSION: Nur ein Rückgabewert
auth_status = authenticator.login("Login", location="main")

if auth_status:
    username = authenticator.username
    name = config["credentials"]["usernames"][username]["name"]

    st.title("🏨 Hotel Pricing Demo")
    st.success(f"Willkommen zurück, {name}!")

    with st.form("eingabe"):
        zimmer = st.text_input("Zimmername", "Standard")
        basis = st.number_input("Basispreis (€)", value=100.0)
        mitbewerb = st.number_input("Mitbewerberpreis (€)", value=110.0)
        auslastung = st.slider("Auslastung", 0.0, 1.0, 0.6)
        aggressiv = st.select_slider("Strategie", [0.3, 0.5, 0.7, 1.0], value=0.7)
        senden = st.form_submit_button("Preis berechnen")

    if senden:
        neuer_preis = calculate_price(basis, mitbewerb, auslastung, aggressiv)
        st.success(f"💰 Empfohlener KI-Preis: {neuer_preis:.2f} €")
        gewinn = (neuer_preis - basis) * auslastung * 90
        st.info(f"📆 Gewinn über 90 Tage: {gewinn:.2f} €")

elif auth_status is False:
    st.error("❌ Falscher Benutzername oder Passwort")
elif auth_status is None:
    st.warning("🔐 Bitte einloggen.")
