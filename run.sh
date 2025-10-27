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

# Installer ou mettre à jour les dépendances
echo "📦 Vérification et installation des dépendances..."
$PIP_CMD install --upgrade -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès !"
    echo ""
else
    echo "❌ Erreur lors de l'installation des dépendances."
    echo "Veuillez vérifier vos configurations Python et pip."
    exit 1
fi
echo ""

# Lancer l'application
echo "🚀 Lancement de l'application..."
streamlit run app/app.py
