import pandas as pd
import streamlit as st
import os

CSV_PATH = "catalogue.csv"

st.set_page_config(
    page_title="Bibliothèque Numérique UCKIS", page_icon="📚", layout="wide"
)


def charger_donnees():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame(
            columns=[
                "Titre", "Auteur", "Faculte", "Domaine",
                "Format", "Disponibilite", "Annee", "Notes",
            ]
        )
    return pd.read_csv(CSV_PATH)


def sauvegarder_donnees(df):
    df.to_csv(CSV_PATH, index=False)


# Chargement initial en session_state pour éviter de relire le fichier à chaque interaction
if "df" not in st.session_state:
    st.session_state.df = charger_donnees()

df = st.session_state.df

st.title("📚 Bibliothèque Numérique — UCKIS / ISA-UCKIS")
st.caption(
    f"{len(df)} ouvrage(s) actuellement enregistré(s) dans le catalogue réel."
)

# --- Barre latérale : filtres ---
st.sidebar.header("🔍 Filtres de recherche")

facultes = ["Toutes"] + sorted(df["Faculte"].dropna().unique().tolist()) if len(df) else ["Toutes"]
faculte_choisie = st.sidebar.selectbox("Faculté", facultes)

recherche = st.sidebar.text_input("Mot-clé (titre, auteur, domaine)")

df_filtre = df.copy()
if faculte_choisie != "Toutes":
    df_filtre = df_filtre[df_filtre["Faculte"] == faculte_choisie]

if recherche and len(df_filtre):
    masque = (
        df_filtre["Titre"].astype(str).str.contains(recherche, case=False, na=False)
        | df_filtre["Auteur"].astype(str).str.contains(recherche, case=False, na=False)
        | df_filtre["Domaine"].astype(str).str.contains(recherche, case=False, na=False)
    )
    df_filtre = df_filtre[masque]

# --- Statistiques réelles (pas simulées) ---
col1, col2, col3 = st.columns(3)
col1.metric("Ouvrages au catalogue", len(df))
col2.metric("Résultats affichés", len(df_filtre))
col3.metric("Facultés représentées", df["Faculte"].nunique() if len(df) else 0)

st.markdown("---")
st.subheader("📖 Catalogue")
st.dataframe(df_filtre, use_container_width=True)

# --- Formulaire d'ajout d'un ouvrage ---
st.markdown("---")
st.subheader("➕ Ajouter un ouvrage au catalogue")

with st.form("ajout_ouvrage", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        titre = st.text_input("Titre *")
        auteur = st.text_input("Auteur *")
        faculte = st.text_input("Faculté *")
        domaine = st.text_input("Domaine")
    with c2:
        format_ = st.text_input("Format (PDF, EPUB, papier...)")
        dispo = st.selectbox("Disponibilité", ["En ligne", "Papier - bibliothèque", "Réservé", "Indisponible"])
        annee = st.number_input("Année", min_value=1900, max_value=2100, value=2025, step=1)
        notes = st.text_input("Notes")

    envoye = st.form_submit_button("Ajouter au catalogue")

    if envoye:
        if not titre or not auteur or not faculte:
            st.error("Titre, Auteur et Faculté sont obligatoires.")
        else:
            nouvelle_ligne = pd.DataFrame([{
                "Titre": titre, "Auteur": auteur, "Faculte": faculte,
                "Domaine": domaine, "Format": format_, "Disponibilite": dispo,
                "Annee": annee, "Notes": notes,
            }])
            st.session_state.df = pd.concat([df, nouvelle_ligne], ignore_index=True)
            sauvegarder_donnees(st.session_state.df)
            st.success(f"« {titre} » a été ajouté au catalogue.")
            st.rerun()

# --- Suppression / gestion rapide ---
if len(df):
    st.markdown("---")
    st.subheader("🗑️ Retirer un ouvrage")
    titre_a_supprimer = st.selectbox("Sélectionner l'ouvrage à retirer", df["Titre"])
    if st.button("Retirer cet ouvrage"):
        st.session_state.df = df[df["Titre"] != titre_a_supprimer].reset_index(drop=True)
        sauvegarder_donnees(st.session_state.df)
        st.success(f"« {titre_a_supprimer} » a été retiré.")
        st.rerun()
