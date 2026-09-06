"""Lanceur pour l'exécutable Windows : démarre Streamlit dans le même
processus et ouvre l'application dans le navigateur, comme un vrai logiciel.

Utilise l'API interne de Streamlit (au lieu d'un sous-processus) car un
exécutable PyInstaller ne peut pas relancer un interpréteur Python externe."""

import os
import sys

from streamlit.web import cli as stcli


def dossier_de_base():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # dossier temporaire créé par PyInstaller (--onefile)
    return os.path.dirname(os.path.abspath(__file__))


def desactiver_prompt_premier_lancement():
    """Évite que Streamlit ne demande un email au tout premier lancement."""
    dossier = os.path.join(os.path.expanduser("~"), ".streamlit")
    fichier = os.path.join(dossier, "credentials.toml")
    if not os.path.exists(fichier):
        os.makedirs(dossier, exist_ok=True)
        with open(fichier, "w", encoding="utf-8") as f:
            f.write('[general]\nemail = ""\n')


def main():
    desactiver_prompt_premier_lancement()
    base_dir = dossier_de_base()
    app_path = os.path.join(base_dir, "app.py")
    os.chdir(base_dir)

    sys.argv = [
        "streamlit", "run", app_path,
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
