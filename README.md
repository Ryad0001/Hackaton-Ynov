# ANTKATHON - Générateur d'Art Abstraît

## Auteurs

Projet développé par **Oubay MOUDDEN, Adam CHOUAG, Ryad MURAD et Azad KARA** dans le cadre du Hackathon Ynov.

## Description

**ANTKATHON** est une application web interactive qui transforme vos données en œuvres d'art abstrait spectaculaires. Développé dans le cadre d'un hackathon, ce projet utilise des algorithmes de visualisation créative pour convertir des jeux de données en compositions artistiques uniques de style "splash art" (art d'éclaboussure).

### Concept

L'application fonctionne selon un principe simple : **vos données deviennent des formes, couleurs et positions visuelles**. Chaque ligne de votre fichier CSV ou JSON est transformée en un élément artistique composé de :

- **Des éclaboussures de couleur** positionnées selon vos valeurs numériques
- **Des couleurs dynamiques** générées à partir de vos données
- **Des effets de "drip" (gouttes)** qui ajoutent du mouvement et de la profondeur à l'œuvre
- **Un fond dégradé** qui sublime la composition

### Fonctionnement

1. **Normalisation des données** : L'algorithme extrait automatiquement les colonnes pertinentes :

   - Une colonne de catégorie (texte)
   - Deux colonnes numériques (ValueA et ValueB)

2. **Génération artistique** :

   - **ValueA** détermine la position horizontale des éléments
   - **ValueB** détermine la teinte de couleur (transformation HSV en RGB)
   - Chaque point de données génère une "explosion" de couleur avec un effet d'éclaboussure
   - Des gouttes tombent verticalement depuis chaque éclaboussure pour ajouter du dynamisme

3. **Personnalisation** : L'utilisateur peut choisir entre un fond sombre ou clair pour adapter l'ambiance de l'œuvre générée

## Structure du Projet

```
Hackaton-Ynov/
├── algos/                          # Algorithmes de traitement de données
│   ├── __init__.py
│   └── data_processor.py          # Modules de traitement et génération
├── app/                            # Interface Streamlit
│   ├── __init__.py
│   └── app.py                     # Application principale
├── data/                           # Images générées
│   └── generated_art.png          # Dernière œuvre générée
├── Dataset/                        # Jeux de données d'exemple
│   ├── composition_1_toile.csv
│   ├── composition_2_explosion.csv
│   └── composition_3_neon.csv
├── requirements.txt                # Dépendances Python
├── run.sh                          # Script de lancement
└── README.md
```

## Installation

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

### Dépannage

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

## Fonctionnalités

- **Téléversement de fichiers** : Support complet des formats CSV et JSON
- **Aperçu des données** : Visualisation des 5 premières lignes avec statistiques descriptives
- **Génération d'art dynamique** : Création automatique d'œuvres abstraites à partir des données
- **Effet "Splash Art"** : Éclaboussures de couleur avec gouttes tombantes réalistes
- **Algorithme de couleur avancé** : Transformation HSV en RGB pour des couleurs vibrantes
- **Téléchargement d'images** : Export des œuvres générées en format PNG haute qualité
- **Interface moderne** : Design Streamlit intuitif et responsive

## Utilisation

### Étape par étape

1. **Lancer l'application** : Exécutez `streamlit run app/app.py` ou utilisez le script `./run.sh`

2. **Téléverser vos données** :

   - Utilisez vos propres fichiers CSV ou JSON
   - Ou testez avec les exemples fournis dans le dossier `Dataset/`

3. **Consultation des données** :
   - Visualisez les 5 premières lignes de votre fichier
   - Consultez les statistiques descriptives (shape, colonnes)
4. **Génération artistique** :
   - Cliquez sur le bouton "Générer l'Œuvre d'Art"
   - Attendez quelques secondes pendant le traitement
5. **Récupération** :
   - Visualisez votre œuvre générée
   - Téléchargez l'image en haute qualité (PNG)

### Format de données recommandé

Votre fichier CSV ou JSON doit contenir :

- **Au moins une colonne texte** : Pour les catégories (ex: noms de produits, types, etc.)
- **Au moins deux colonnes numériques** : Pour générer la position et la couleur

Exemple de structure :

```csv
produit,température,prix
Ordinateur,25,1200
Livre,20,15
Téléphone,30,800
```

Les valeurs numériques seront automatiquement normalisées pour créer l'art.

## Algorithmes et Techniques

### Traitement des Données (`process_data`)

La fonction `process_data()` effectue plusieurs opérations :

1. **Lecture et validation** : Détection du format de fichier (CSV ou JSON)
2. **Normalisation des colonnes** :
   - Conversion des noms en minuscules et suppression des espaces
   - Identification automatique des colonnes numériques et textuelles
   - Création d'un DataFrame standardisé avec `Category`, `ValueA`, `ValueB`
3. **Vérifications** : Contrôle que le fichier contient au moins 2 colonnes numériques

### Génération Artistique (`generate_art`)

L'algorithme de génération utilise plusieurs techniques avancées :

#### 1. Normalisation des Données

```python
# Normalisation linéaire des coordonnées et couleurs
coord_norm = (ValueA - min) / (max - min)
color_norm = (ValueB - min) / (max - min)
```

#### 2. Génération de Couleurs HSV → RGB

- **ValueB** est transformé en teinte (0-1) dans l'espace de couleurs HSV
- Saturation et luminosité fixées à 1.0 pour des couleurs vibrantes
- Conversion en RGB pour le rendu

#### 3. Effet "Splash" (Éclaboussure)

- Distribution circulaire aléatoire de particules autour d'un point central
- Nombre de particules proportionnel à l'intensité
- Variation de la couleur avec ajout de bruit aléatoire (±30)
- Tailles variables des particules (2-8 pixels)

#### 4. Effet "Drip" (Gouttes)

- 1 à 3 gouttes verticales par éclaboussure
- Position et longueur aléatoires pour un effet naturel
- Transparence appliquée (alpha = 180)

#### 5. Fond Dégradé

- Transition linéaire entre deux couleurs RVB
- Calcul pixel par pixel pour un effet fluide
- Deux styles disponibles : sombre (20,20,30 → 80,40,100) ou clair

### Gestion de la Réproducibilité

Chaque ligne de données utilise un seed basé sur son hash pour assurer que :

- Les données identiques produisent toujours le même pattern
- Les données différentes produisent des patterns distincts

## Développement

### Architecture du Code

- **`algos/data_processor.py`** :

  - `normalise_dataframe()` : Standardisation des colonnes
  - `process_data()` : Traitement principal des fichiers
  - `generate_art()` : Génération de l'image artistique
  - `validate_file_type()` : Validation des formats
  - `create_gradient_background()` : Création du fond dégradé
  - `draw_color_splash()` : Dessin des éclaboussures

- **`app/app.py`** :
  - Interface utilisateur Streamlit
  - Gestion du téléversement de fichiers
  - Affichage des données et statistiques
  - Intégration de la génération artistique
  - Bouton de téléchargement

### Technologies Utilisées

- **Streamlit** : Framework web pour l'interface
- **Pandas** : Manipulation des données
- **Pillow (PIL)** : Génération et traitement d'images
- **NumPy** : Calculs numériques
- **Colorsys** : Conversion d'espaces de couleurs

## Dépendances

Le projet utilise les bibliothèques Python suivantes (définies dans `requirements.txt`) :

- **streamlit** (≥1.28.0) : Framework web pour l'interface utilisateur
- **pandas** (≥2.0.0) : Manipulation et analyse de données
- **matplotlib** (≥3.7.0) : Visualisation graphique (non utilisée actuellement)
- **numpy** (≥1.24.0) : Calculs numériques
- **Pillow** (≥9.0.0) : Traitement et génération d'images

## Cas d'Usage

**ANTKATHON** peut être utilisé dans différents contextes :

- **Visualisation créative de données** : Transformer des rapports en œuvres d'art
- **Communication visuelle** : Présenter des statistiques de manière attractive
- **Projets artistiques** : Créer des compositions abstraites à partir de datasets
- **Éducation** : Enseigner la visualisation de données de manière ludique
- **Exploration de données** : Découvrir des patterns visuels dans vos données

## Exemples de Résultats

Les fichiers dans le dossier `Dataset/` contiennent des exemples de compositions pré-définies :

- `composition_1_toile.csv` : Style toile artistique
- `composition_2_explosion.csv` : Style explosion colorée
- `composition_3_neon.csv` : Style néon moderne

## Licence

Ce projet est développé dans le cadre pédagogique et est libre d'utilisation pour le hackathon.
