import json
import os

import pandas as pd
import streamlit as st
from PIL import Image

CSV_PATH = "catalogue.csv"
PLAN_PATH = "plan_acquisition.json"
ICON_PATH = "icon.png"

icone_page = Image.open(ICON_PATH) if os.path.exists(ICON_PATH) else "📚"

st.set_page_config(
    page_title="Bibliothèque Numérique UCKIS", page_icon=icone_page, layout="wide"
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


def charger_plan():
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_plan(plan):
    with open(PLAN_PATH, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)


if "df" not in st.session_state:
    st.session_state.df = charger_donnees()

if "plan" not in st.session_state:
    st.session_state.plan = charger_plan()

st.title("📚 Bibliothèque Numérique — UCKIS / ISA-UCKIS")

onglet_catalogue, onglet_projet = st.tabs(
    ["📖 Catalogue", "🎯 Projet d'acquisition (100 000 ressources)"]
)

# ============================================================
# Onglet 1 — Catalogue
# ============================================================
with onglet_catalogue:
    df = st.session_state.df

    st.caption(
        f"{len(df)} ouvrage(s) actuellement enregistré(s) dans le catalogue réel."
    )

    st.sidebar.header("🔍 Filtres de recherche")

    facultes = (
        ["Toutes"] + sorted(df["Faculte"].dropna().unique().tolist())
        if len(df)
        else ["Toutes"]
    )
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

    col1, col2, col3 = st.columns(3)
    col1.metric("Ouvrages au catalogue", len(df))
    col2.metric("Résultats affichés", len(df_filtre))
    col3.metric("Facultés représentées", df["Faculte"].nunique() if len(df) else 0)

    st.markdown("---")
    st.subheader("📖 Catalogue")
    st.dataframe(df_filtre, use_container_width=True)

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
            dispo = st.selectbox(
                "Disponibilité",
                ["En ligne", "Papier - bibliothèque", "Réservé", "Indisponible"],
            )
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

    if len(df):
        st.markdown("---")
        st.subheader("🗑️ Retirer un ouvrage")
        titre_a_supprimer = st.selectbox("Sélectionner l'ouvrage à retirer", df["Titre"])
        if st.button("Retirer cet ouvrage"):
            st.session_state.df = df[df["Titre"] != titre_a_supprimer].reset_index(drop=True)
            sauvegarder_donnees(st.session_state.df)
            st.success(f"« {titre_a_supprimer} » a été retiré.")
            st.rerun()

# ============================================================
# Onglet 2 — Suivi du projet d'acquisition
# ============================================================
with onglet_projet:
    plan = st.session_state.plan

    st.caption(
        "Suivi opérationnel du plan d'acquisition de 100 000 ressources documentaires "
        "(stratégie numérique, dons/partenariats, achats ciblés)."
    )

    total_cible = sum(o["cible"] for o in plan["objectifs"].values())
    total_actuel = sum(o["actuel"] for o in plan["objectifs"].values())

    st.markdown("### 🎯 Progression globale")
    st.progress(min(total_actuel / total_cible, 1.0) if total_cible else 0)
    st.metric(
        "Ressources acquises / cible totale",
        f"{total_actuel:,} / {total_cible:,}".replace(",", " "),
    )

    st.markdown("---")
    st.markdown("### 📊 Objectifs par stratégie")

    cols = st.columns(3)
    cles = list(plan["objectifs"].keys())
    nouvelles_valeurs = {}

    for col, cle in zip(cols, cles):
        obj = plan["objectifs"][cle]
        with col:
            st.markdown(f"**{obj['label']}**")
            st.progress(min(obj["actuel"] / obj["cible"], 1.0) if obj["cible"] else 0)
            nouvelles_valeurs[cle] = st.number_input(
                f"Quantité acquise ({cle})",
                min_value=0,
                max_value=obj["cible"],
                value=obj["actuel"],
                step=100,
                key=f"input_{cle}",
            )
            st.caption(f"Cible : {obj['cible']:,}".replace(",", " "))

    if st.button("💾 Enregistrer la progression"):
        for cle, valeur in nouvelles_valeurs.items():
            plan["objectifs"][cle]["actuel"] = int(valeur)
        sauvegarder_plan(plan)
        st.success("Progression enregistrée.")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🗓️ Chronogramme d'exécution (Mois 1 à 3)")

    for i, tache in enumerate(plan["chronogramme"]):
        c1, c2 = st.columns([1, 8])
        with c1:
            fait = st.checkbox(
                "Fait", value=tache["fait"], key=f"tache_{i}", label_visibility="collapsed"
            )
        with c2:
            statut = "✅" if fait else "⬜"
            st.markdown(
                f"{statut} **{tache['periode']}** — {tache['action']} "
                f"*(Responsable : {tache['responsable']})*"
            )
        plan["chronogramme"][i]["fait"] = fait

    if st.button("💾 Enregistrer le chronogramme"):
        sauvegarder_plan(plan)
        st.success("Chronogramme mis à jour.")
        st.rerun()
