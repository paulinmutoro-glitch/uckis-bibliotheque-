# 📚 Bibliothèque Numérique UCKIS / ISA-UCKIS

Application Streamlit pour consulter, filtrer et enrichir le catalogue de ressources académiques en libre accès.

## 🚀 Mise en ligne gratuite (Streamlit Community Cloud) — accessible depuis votre téléphone

Le code est déjà sur GitHub dans ce dépôt : il ne reste que le déploiement.

### Étape 1 — Déployer sur Streamlit Cloud
1. Allez sur **https://share.streamlit.io**
2. Cliquez **"Sign in with GitHub"** et autorisez la connexion
3. Cliquez **"Create app"** (ou "New app")
4. Sélectionnez :
   - Repository : `paulinmutoro-glitch/uckis-bibliotheque-`
   - Branch : `main` (une fois la Pull Request fusionnée)
   - Main file path : `app.py`
5. Cliquez **"Deploy"**
6. Patientez 1-2 minutes — l'app se construit automatiquement

### Étape 2 — Utiliser l'app sur votre téléphone
1. Vous obtenez une URL du type : `https://uckis-bibliotheque.streamlit.app`
2. Ouvrez cette URL dans le navigateur de votre téléphone
3. Pour un accès rapide type "application" :
   - **iPhone (Safari)** : bouton Partager → "Sur l'écran d'accueil"
   - **Android (Chrome)** : menu ⋮ → "Ajouter à l'écran d'accueil"

L'icône `icon.png` (livre + croix, aux couleurs de l'UCKIS) sert de favicon de l'app et apparaît comme icône lors de l'ajout à l'écran d'accueil.

## 💻 Créer un exécutable Windows (.exe) — usage hors-ligne sur PC

Un `.exe` ne fonctionne que sur un ordinateur Windows (pas sur téléphone). Il permet
d'utiliser la bibliothèque sans connexion Internet, comme un logiciel installé.

### Prérequis
- Un PC Windows avec [Python 3.10+](https://python.org) installé (cocher "Add to PATH" à l'installation)

### Construction
1. Téléchargez/clonez ce dépôt sur le PC Windows
2. Ouvrez une invite de commande dans le dossier du projet
3. Double-cliquez sur `build_exe.bat` (ou lancez-le depuis l'invite de commande)
4. Patientez quelques minutes — le script installe les dépendances puis construit l'exécutable
5. Récupérez `dist\Bibliotheque_UCKIS.exe`

### Utilisation
Double-cliquez sur `Bibliotheque_UCKIS.exe` : l'application démarre un serveur local
et s'ouvre automatiquement dans le navigateur par défaut. Les ajouts/suppressions
d'ouvrages sont enregistrés dans `catalogue.csv`, créé à côté de l'exécutable au
premier lancement, et sont conservés d'une utilisation à l'autre.

> Cette construction doit être faite sur Windows : un `.exe` ne peut pas être
> généré depuis Linux/macOS ni depuis cette session (environnement cloud Linux).

## 🔄 Mettre à jour le catalogue plus tard
Toute modification faite dans l'app (ajout/suppression d'un ouvrage) est enregistrée sur le serveur Streamlit Cloud, mais **n'est pas automatiquement renvoyée vers GitHub**. Pour une mise à jour durable et versionnée : éditez `catalogue.csv` directement sur GitHub (bouton crayon ✏️ sur le fichier) puis "Commit changes" — l'app se redéploie automatiquement.

## ⚠️ Note sur la persistance des données
Streamlit Community Cloud réinitialise le système de fichiers à chaque redéploiement. Les ajouts faits *via le formulaire de l'app* peuvent donc être perdus lors d'une mise à jour du code. Pour une bibliothèque destinée à durer, il est recommandé à terme de passer à une vraie base de données (Google Sheets, Airtable, ou PostgreSQL) — je peux vous accompagner sur cette évolution quand vous serez prêt.
