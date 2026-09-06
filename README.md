# 📚 Bibliothèque Numérique UCKIS / ISA-UCKIS

Application Streamlit pour consulter, filtrer et enrichir le catalogue de ressources académiques en libre accès.

## 🚀 Mise en ligne gratuite (Streamlit Community Cloud) — accessible depuis votre téléphone

### Étape 1 — Créer un compte GitHub (si vous n'en avez pas)
1. Allez sur **https://github.com**
2. Cliquez sur "Sign up", créez un compte gratuit

### Étape 2 — Créer un dépôt (repository)
1. Une fois connecté, cliquez sur le bouton vert **"New"** (ou allez sur github.com/new)
2. Nom du dépôt : `uckis-bibliotheque` (ou le nom de votre choix)
3. Cochez **"Public"**
4. Cliquez **"Create repository"**

### Étape 3 — Ajouter les 3 fichiers
Sur la page de votre nouveau dépôt vide :
1. Cliquez **"uploading an existing file"**
2. Glissez-déposez les 3 fichiers de ce dossier : `app.py`, `catalogue.csv`, `requirements.txt`
3. Cliquez **"Commit changes"** en bas de page

### Étape 4 — Déployer sur Streamlit Cloud
1. Allez sur **https://share.streamlit.io**
2. Cliquez **"Sign in with GitHub"** et autorisez la connexion
3. Cliquez **"Create app"** (ou "New app")
4. Sélectionnez :
   - Repository : `votre-compte/uckis-bibliotheque`
   - Branch : `main`
   - Main file path : `app.py`
5. Cliquez **"Deploy"**
6. Patientez 1-2 minutes — l'app se construit automatiquement

### Étape 5 — Utiliser l'app sur votre téléphone
1. Vous obtenez une URL du type : `https://uckis-bibliotheque.streamlit.app`
2. Ouvrez cette URL dans le navigateur de votre téléphone
3. Pour un accès rapide type "application" :
   - **iPhone (Safari)** : bouton Partager → "Sur l'écran d'accueil"
   - **Android (Chrome)** : menu ⋮ → "Ajouter à l'écran d'accueil"

L'icône `icon.png` (livre + croix, aux couleurs de l'UCKIS) sert de favicon de l'app et apparaît comme icône lors de l'ajout à l'écran d'accueil.

## 🔄 Mettre à jour le catalogue plus tard
Toute modification faite dans l'app (ajout/suppression d'un ouvrage) est enregistrée sur le serveur Streamlit Cloud, mais **n'est pas automatiquement renvoyée vers GitHub**. Pour une mise à jour durable et versionnée : éditez `catalogue.csv` directement sur GitHub (bouton crayon ✏️ sur le fichier) puis "Commit changes" — l'app se redéploie automatiquement.

## ⚠️ Note sur la persistance des données
Streamlit Community Cloud réinitialise le système de fichiers à chaque redéploiement. Les ajouts faits *via le formulaire de l'app* peuvent donc être perdus lors d'une mise à jour du code. Pour une bibliothèque destinée à durer, il est recommandé à terme de passer à une vraie base de données (Google Sheets, Airtable, ou PostgreSQL) — je peux vous accompagner sur cette évolution quand vous serez prêt.
