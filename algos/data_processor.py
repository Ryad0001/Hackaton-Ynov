"""
Module de traitement des données et de génération d'art pour ANTKATHON
Refactorisé pour une utilisation avec Streamlit.
"""

import pandas as pd
import json
from typing import Union, Dict, Any
import matplotlib.pyplot as plt  # Ajout pour la génération
import numpy as np               # Ajout pour la génération
import random                    # Ajout pour la génération
import os                        # Ajout pour la gestion des fichiers

# --- 1. Traitement des Données ---

def normalise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise automatiquement un DataFrame avec des choix intelligents des colonnes.
    Reprend la logique de normaliser_csv du notebook.
    
    Args:
        df: DataFrame à normaliser
        
    Returns:
        DataFrame normalisé avec les colonnes : Category, ValueA, ValueB
    """
    # Nettoyer les noms de colonnes (minuscules + suppression des espaces)
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Détecter colonnes numériques et textuelles
    colonnes_num = df.select_dtypes(include=["number"]).columns.tolist()
    colonnes_text = df.select_dtypes(exclude=["number"]).columns.tolist()
    
    # Vérifications
    if len(colonnes_text) < 1:
        raise ValueError("Le fichier doit contenir au moins une colonne texte.")
    
    if len(colonnes_num) < 2:
        raise ValueError("Le fichier doit contenir au moins deux colonnes numériques.")
    
    # Choix intelligent :
    # - La première colonne texte devient "Category"
    # - La première colonne numérique devient "ValueA"
    # - La deuxième colonne numérique devient "ValueB"
    cat_col = colonnes_text[0]
    valuea_col = colonnes_num[0]
    valueb_col = colonnes_num[1] if len(colonnes_num) > 1 else colonnes_num[0]
    
    # Création du DataFrame normalisé
    df_normalise = pd.DataFrame({
        "Category": df[cat_col],
        "ValueA": df[valuea_col],
        "ValueB": df[valueb_col]
    })
    
    print(f"✅ Normalisation : '{cat_col}' → Category, '{valuea_col}' → ValueA, '{valueb_col}' → ValueB")
    
    return df_normalise


def process_data(uploaded_file) -> Dict[str, Any]:
    """
    Traite les données du fichier uploadé.
    (Refactorisé pour inclure le DataFrame complet dans la sortie)
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        Dict contenant les données traitées ET le DataFrame
    """
    if uploaded_file is None:
        return {}
    
    filename = uploaded_file.name.lower()
    
    if filename.endswith('.csv'):
        try:
            df = pd.read_csv(uploaded_file)
            
            if df.empty:
                return {"error": "Le fichier CSV est vide"}
            
            # Valider les colonnes nécessaires - Essayer d'abord la normalisation intelligente
            required_cols = ['Category', 'ValueA', 'ValueB']
            if not all(col in df.columns for col in required_cols):
                print("🔄 Colonnes non standardisées détectées. Application de la normalisation intelligente...")
                try:
                    df = normalise_dataframe(df)
                except Exception as normalise_error:
                    return {"error": f"Impossible de normaliser les colonnes : {normalise_error}"}

            # Valider et normaliser les catégories
            valid_categories = ['Stroke', 'Gesture', 'Drip', 'Wave']
            
            # Vérifier si toutes les catégories sont valides
            unique_categories = df['Category'].unique()
            invalid_categories = [cat for cat in unique_categories if cat not in valid_categories]
            
            if invalid_categories:
                print(f"⚠️  Catégories non valides détectées : {invalid_categories}")
                print("🔄 Attribution aléatoire des catégories valides...")
                
                # Remplacer les catégories invalides par des catégories valides aléatoires
                for cat in invalid_categories:
                    df.loc[df['Category'] == cat, 'Category'] = random.choice(valid_categories)
                
                print(f"✅ Catégories normalisées : {df['Category'].unique()}")
            
            # Gestion d'erreur : si après normalisation il n'y a toujours pas de catégories valides
            if len(df['Category'].unique()) == 0 or not any(cat in df['Category'].values for cat in valid_categories):
                print("⚠️  Aucune catégorie valide après normalisation.")
                print("🔄 Attribution de catégories aléatoires à toutes les lignes...")
                df['Category'] = [random.choice(valid_categories) for _ in range(len(df))]
                print(f"✅ Toutes les lignes ont maintenant une catégorie valide.")
            
            return {
                "type": "csv",
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "preview": df.head(5).to_dict('records'),
                "dataframe": df  # <-- MODIFICATION CLÉ: Ajout du DF complet
            }
        except Exception as e:
            return {"error": f"Erreur lors de la lecture du CSV : {e}"}
    
    elif filename.endswith('.json'):
        try:
            df = pd.read_json(uploaded_file)
            
            if df.empty:
                return {"error": "Le fichier JSON est vide ou mal formaté"}
                
            # Valider les colonnes - Essayer d'abord la normalisation intelligente
            required_cols = ['Category', 'ValueA', 'ValueB']
            if not all(col in df.columns for col in required_cols):
                print("🔄 Colonnes non standardisées détectées. Application de la normalisation intelligente...")
                try:
                    df = normalise_dataframe(df)
                except Exception as normalise_error:
                    return {"error": f"Impossible de normaliser les colonnes : {normalise_error}"}
                
            # Valider et normaliser les catégories
            valid_categories = ['Stroke', 'Gesture', 'Drip', 'Wave']
            
            # Vérifier si toutes les catégories sont valides
            unique_categories = df['Category'].unique()
            invalid_categories = [cat for cat in unique_categories if cat not in valid_categories]
            
            if invalid_categories:
                print(f"⚠️  Catégories non valides détectées : {invalid_categories}")
                print("🔄 Attribution aléatoire des catégories valides...")
                
                # Remplacer les catégories invalides par des catégories valides aléatoires
                for cat in invalid_categories:
                    df.loc[df['Category'] == cat, 'Category'] = random.choice(valid_categories)
                
                print(f"✅ Catégories normalisées : {df['Category'].unique()}")
            
            # Gestion d'erreur : si après normalisation il n'y a toujours pas de catégories valides
            if len(df['Category'].unique()) == 0 or not any(cat in df['Category'].values for cat in valid_categories):
                print("⚠️  Aucune catégorie valide après normalisation.")
                print("🔄 Attribution de catégories aléatoires à toutes les lignes...")
                df['Category'] = [random.choice(valid_categories) for _ in range(len(df))]
                print(f"✅ Toutes les lignes ont maintenant une catégorie valide.")
                
            return {
                "type": "json",
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "preview": df.head(5).to_dict('records'),
                "dataframe": df  # <-- MODIFICATION CLÉ: Ajout du DF complet
            }
        except Exception as e:
            return {"error": f"Erreur lors de la lecture du JSON : {e}"}
    
    else:
        # Erreur gérée par validate_file_type, mais on double la sécurité
        return {"error": f"Format de fichier non supporté : {filename}"}


# --- 2. Génération de l'Art ---

def generate_art(processed_data: Dict[str, Any], background_style: str = 'light') -> str:
    """
    Génère une œuvre d'art à partir des données traitées en utilisant
    l'algorithme "Artiste Abstrait" (multi-mode).
    
    Args:
        processed_data: Dictionnaire sortant de process_data
        background_style: 'light' ou 'dark' pour le fond de la toile
        
    Returns:
        Chemin vers l'image générée
    """
    
    # S'assurer que le dossier de sortie existe
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "generated_art.png")

    # Vérifier si les données sont valides
    if "dataframe" not in processed_data:
        print("❌ Erreur : DataFrame non trouvé dans processed_data.")
        return "" 

    df = processed_data['dataframe']
    
    # Vérifier qu'il y a au moins une catégorie valide
    valid_categories = ['Stroke', 'Gesture', 'Drip', 'Wave']
    if not any(cat in df['Category'].values for cat in valid_categories):
        print("❌ Erreur : Aucune catégorie valide trouvée dans les données.")
        print("Les catégories doivent être : Stroke, Gesture, Drip ou Wave")
        return ""
    
    # Compter les catégories valides présentes
    present_categories = df[df['Category'].isin(valid_categories)]['Category'].unique()
    print(f"✅ Catégories détectées : {present_categories}")

    # --- DÉBUT DE L'ALGORITHME DE GÉNÉRATION "ARTISTE ABSTRAIT" ---
    WIDTH = 10
    HEIGHT = 10
    DPI = 300 
    
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT), dpi=DPI)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Style de fond (toile)
    if background_style == 'dark':
        ax.set_facecolor('#0a0a1a') # Fond sombre (style "Tech")
    else:
        ax.set_facecolor('#f4f0e8') # Fond clair (style "Toile")

    print(f"Génération de l'art... Fond : {background_style}")

    # --- BOUCLE DE DESSIN PAR CATÉGORIE ---
    
    for category, group in df.groupby('Category'):
        
        print(f"Dessin du calque : {category} ({len(group)} éléments)")
        
        try:
            # --- MODE 1: ONDE (WAVE) ---
            if category == 'Wave':
                x_wave = np.linspace(0, 100, 500)
                for index, row in group.iterrows():
                    amp = 5 + (row['ValueA'] / 100) * 15
                    freq = 0.5 + (row['ValueB'] / 100) * 3
                    y_center = 50 + (row['ValueA'] - 50) / 5
                    y_wave = amp * np.sin(x_wave / 100 * freq * 2 * np.pi) + y_center
                    
                    ax.plot(x_wave, y_wave, color='cyan', linewidth=2.5, alpha=1.0)
                    ax.plot(x_wave, y_wave, color='white', linewidth=4.5, alpha=0.3)

            # --- MODE 2: TOUCHE (STROKE) ---
            elif category == 'Stroke':
                for index, row in group.iterrows():
                    x_pos = row['ValueA']
                    y_height = row['ValueB']
                    color = plt.cm.Set3(random.random())
                    
                    ax.plot([x_pos, x_pos + random.uniform(-1, 1)], [0, y_height], 
                            color=color, 
                            linewidth=15 + (row['ValueA']/100)*20, 
                            alpha=0.6,
                            solid_capstyle='butt')

            # --- MODE 3: COULURE (DRIP) ---
            elif category == 'Drip':
                for index, row in group.iterrows():
                    x_pos = row['ValueA']
                    y_length = row['ValueB']
                    color = plt.cm.hot(random.uniform(0.3, 0.7)) 
                    
                    ax.plot([x_pos, x_pos + random.uniform(-0.5, 0.5)], [100, 100 - y_length], 
                            color=color, 
                            linewidth=2 + (row['ValueB']/100)*4, 
                            alpha=0.8)
                    
                    ax.scatter(x_pos, 100 - y_length, 
                               s=50 + (row['ValueB']/100)*200, 
                               color=color,
                               alpha=0.7,
                               edgecolors='none')

            # --- MODE 4: GESTE (GESTURE) ---
            elif category == 'Gesture':
                for index, row in group.iterrows():
                    start_x = row['ValueA']
                    start_y = row['ValueB']
                    
                    x_gesture = np.linspace(start_x, start_x + random.uniform(-10, 10), 10)
                    y_gesture = start_y + np.sin(x_gesture) * random.uniform(5, 15)
                    
                    ax.plot(x_gesture, y_gesture, 
                            color='black', 
                            linewidth=1.5, 
                            alpha=0.7)
            
            else:
                print(f"Avertissement : Catégorie '{category}' non reconnue. Elle sera ignorée.")
                
        except Exception as e:
            print(f"Erreur lors du dessin de la catégorie '{category}': {e}")
            # Continue à la catégorie suivante
            pass

    # --- FIN DE L'ALGORITHME ---
    
    try:
        # Sauvegarde de l'image
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    except Exception as e:
        print(f"Erreur critique lors de la sauvegarde de l'image : {e}")
        return "" # Retourne un chemin vide en cas d'échec
    finally:
        # **TRÈS IMPORTANT pour Streamlit**
        # Ferme la figure pour libérer la mémoire et éviter les crashs
        plt.close(fig) 
    
    print(f"Image générée et sauvegardée sous : {output_path}")
    
    # Retourne le chemin où l'image a été sauvegardée
    return output_path


# --- 3. Validation de Fichier (inchangée) ---

def validate_file_type(filename: str) -> bool:
    """Valide si l'extension du fichier est supportée."""
    if filename is None:
        return False
    filename_lower = filename.lower()
    return filename_lower.endswith(('.csv', '.json'))
