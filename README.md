# ANTKATHON - Générateur d'Art Abstraît

## 🎨 Description

Application web Streamlit pour la génération d'art abstrait à partir de données. Ce projet a été développé dans le cadre d'un hackathon et permet de transformer des fichiers CSV ou JSON en œuvres d'art abstrait.

## 📁 Structure du Projet

```
Hackaton-Ynov/
├── algos/                  # Algorithmes de traitement de données
│   ├── __init__.py
│   └── data_processor.py  # Modules de traitement et génération
├── app/                    # Interface Streamlit
│   ├── __init__.py
│   └── app.py             # Application principale
├── data/                   # Données et images générées (à créer)
├── requirements.txt        # Dépendances Python
├── .gitignore
└── README.md
```

## 🚀 Installation

1. **Cloner le repository :**

```bash
git clone <url-du-repo>
cd Hackaton-Ynov
```

2. **Créer un environnement virtuel (recommandé) :**

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. **Installer les dépendances :**

```bash
# Avec pip3
pip3 install -r requirements.txt

# OU avec pip
pip install -r requirements.txt
```

4. **Lancer l'application :**

```bash
streamlit run app/app.py
# OU utiliser le script de lancement :
./run.sh
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### 🔧 Dépannage

Si vous rencontrez l'erreur `pip: command not found` :

**Sur macOS/Linux :**

```bash
# Vérifier si python3 est installé
python3 --version

# Installer pip si nécessaire
python3 -m ensurepip --upgrade

# OU avec Homebrew
brew install python3
```

**Ou utilisez directement python3 et pip3 :**

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
streamlit run app/app.py
```

## 🎯 Fonctionnalités

- ✅ Téléversement de fichiers CSV ou JSON
- ✅ Aperçu des données (5 premières lignes)
- ✅ Statistiques descriptives pour les données numériques
- ✅ Interface de génération d'art (placeholder)
- ✅ Design moderne et intuitif

## 📝 Utilisation

1. Ouvrir l'application dans votre navigateur
2. Téléverser un fichier CSV ou JSON via l'interface (ou utiliser les fichiers d'exemple fournis : `example_data.csv` et `example_data.json`)
3. Consulter l'aperçu de vos données
4. Cliquer sur "Générer l'Œuvre d'Art"
5. Visualiser le résultat (simulé pour l'instant)

## 🔧 Développement

### Structure des Modules

- **`algos/data_processor.py`** : Contient les fonctions `process_data()` et `generate_art()` qui doivent être implémentées avec les vrais algorithmes
- **`app/app.py`** : Contient l'interface Streamlit principale

### Prochaines Étapes

- [ ] Implémenter l'algorithme de génération d'art abstrait dans `generate_art()`
- [ ] Ajouter des paramètres de personnalisation de la génération
- [ ] Implémenter l'export des images générées
- [ ] Ajouter plus de formats de fichiers supportés

## 📦 Dépendances

- `streamlit` : Interface web
- `pandas` : Traitement des données

## 👥 Auteurs

Développé pour le Hackathon Ynov

## 📄 Licence

Ce projet est libre d'utilisation pour le hackathon.
