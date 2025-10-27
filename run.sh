#!/bin/bash

# Script de lancement pour l'application Streamlit ANTKATHON

echo "🎨 Lancement de ANTKATHON - Générateur d'Art Abstraît"
echo "=================================================="
echo ""

# Détecter la commande pip disponible
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ pip n'est pas installé."
    echo ""
    echo "Veuillez installer pip avec :"
    echo "  python3 -m ensurepip --upgrade"
    echo ""
    echo "Ou utiliser Homebrew :"
    echo "  brew install python3"
    echo ""
    exit 1
fi

# Détecter la commande streamlit
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit n'est pas installé."
    echo "📦 Installation des dépendances..."
    $PIP_CMD install -r requirements.txt
    echo ""
fi

# Lancer l'application
echo "🚀 Lancement de l'application..."
streamlit run app/app.py
