"""
Module de traitement des données et de génération d'art pour ANTKATHON
Refactorisé pour une utilisation avec Streamlit.
Utilise l'algorithme "Splash Art" basé sur Pillow (PIL) de manière déterministe.
"""

import pandas as pd
import json
from typing import Union, Dict, Any
import os
import random
import math

# --- Imports pour la génération d'art (Pillow) ---
# Matplotlib et Numpy ne sont plus requis pour CET algorithme
from PIL import Image, ImageDraw


# --- 1. Traitement des Données ---

def normalise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise automatiquement un DataFrame avec des choix intelligents des colonnes,
    basé sur l'algorithme "Splash".
    
    Args:
        df: DataFrame à normaliser
        
    Returns:
        DataFrame normalisé avec les colonnes : Category, ValueA, ValueB
        
    Raises:
        ValueError: Si les conditions (colonnes) ne sont pas remplies.
    """
    # Nettoyer les noms de colonnes (minuscules + suppression des espaces)
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # Détecter colonnes numériques et textuelles
    colonnes_num = df.select_dtypes(include=["number"]).columns.tolist()
    colonnes_text = df.select_dtypes(exclude=["number"]).columns.tolist()
    
    # Vérifications (Amélioration de la gestion d'erreur)
    if len(colonnes_num) < 2:
        raise ValueError("Le fichier doit contenir au moins deux colonnes numériques (pour 'Coordonnees' et 'Couleur').")
    
    # Création du DataFrame normalisé
    new_df = pd.DataFrame()
    
    # - La première colonne texte (si elle existe) devient "Category"
    new_df["Category"] = df[colonnes_text[0]] if len(colonnes_text) > 0 else "Inconnue"
    # - La première colonne numérique devient "ValueA" (Coordonnees)
    new_df["ValueA"] = df[colonnes_num[0]]
    # - La deuxième colonne numérique devient "ValueB" (Couleur)
    new_df["ValueB"] = df[colonnes_num[1]]
    
    print(f"✅ Normalisation : '{colonnes_text[0] if len(colonnes_text) > 0 else 'N/A'}' → Category, '{colonnes_num[0]}' → ValueA, '{colonnes_num[1]}' → ValueB")
    
    return new_df


def process_data(uploaded_file) -> Dict[str, Any]:
    """
    Traite les données du fichier uploadé.
    Tente une normalisation intelligente des colonnes.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        Dict contenant les données traitées ET le DataFrame
    """
    if uploaded_file is None:
        return {}
    
    filename = uploaded_file.name.lower()
    df = None
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            return {"error": f"Format de fichier non supporté : {filename}"}
            
        if df.empty:
            return {"error": "Le fichier est vide"}
            
        # --- GESTION D'ERREUR AMÉLIORÉE ---
        # Tenter la normalisation intelligente
        try:
            df_normalise = normalise_dataframe(df)
        except ValueError as e:
            # Capturer les erreurs de normalisation (ex: "pas assez de colonnes")
            print(f"Erreur de normalisation : {e}")
            return {"error": f"Erreur de normalisation : {e}"}
        
        # Si la normalisation réussit :
        return {
            "type": "csv" if filename.endswith('.csv') else "json",
            "shape": df_normalise.shape,
            "columns": df_normalise.columns.tolist(),
            "preview": df_normalise.head(5).to_dict('records'),
            "dataframe": df_normalise  # <-- Le DF normalisé est prêt
        }
            
    except Exception as e:
        # Erreur générale de lecture de fichier
        return {"error": f"Erreur lors de la lecture du fichier : {e}"}


# --- 2. Génération de l'Art (Algorithme "Splash Art") ---

def create_gradient_background(width, height, top_color=(20, 20, 30), bottom_color=(80, 40, 100)):
    """Crée une image de fond en dégradé vertical (utilisé par generate_art)."""
    img = Image.new("RGB", (width, height), color=0)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def draw_color_splash(draw: ImageDraw.Draw, x, y, base_color, intensity=1.0, radius=50):
    """Dessine une 'éclaboussure' de plusieurs gouttes (utilisé par generate_art)."""
    num_drops = int(100 * intensity)
    for _ in range(num_drops):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, radius)
        px = x + math.cos(angle) * dist
        py = y + math.sin(angle) * dist

        r = min(255, max(0, base_color[0] + random.randint(-30, 30)))
        g = min(255, max(0, base_color[1] + random.randint(-30, 30)))
        b = min(255, max(0, base_color[2] + random.randint(-30, 30)))

        size = random.randint(2, 8)
        draw.ellipse((px - size, py - size, px + size, py + size), fill=(r, g, b))


def generate_art(processed_data: Dict[str, Any], background_style: str = 'dark') -> str:
    """
    Génère une œuvre d'art "Splash Art" à partir des données traitées.
    (Utilise Pillow, non Matplotlib)
    """
    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "generated_art.png")

    if "dataframe" not in processed_data:
        print("❌ Erreur : DataFrame non trouvé dans processed_data.")
        return "" 

    df = processed_data['dataframe']
    
    # Dimensions de l'image
    WIDTH = 1000
    HEIGHT = 700

    # --- DÉBUT DE L'ALGORITHME "SPLASH ART" ---
    
    # 1. Fond dégradé (le style 'dark'/'light' est ignoré ici, on utilise le dégradé par défaut)
    if background_style == 'light':
        # Option pour un fond clair si vous le souhaitez
        background = create_gradient_background(WIDTH, HEIGHT, top_color=(240, 240, 230), bottom_color=(200, 200, 220))
    else:
        # Fond sombre par défaut de l'algorithme
        background = create_gradient_background(WIDTH, HEIGHT, top_color=(20, 20, 30), bottom_color=(80, 40, 100))

    image = background.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")

    # 2. Normalisation des coordonnées
    min_coord = df["ValueA"].min()
    max_coord = df["ValueA"].max()
    coord_norm = (df["ValueA"] - min_coord) / (max_coord - min_coord + 1e-9) # 1e-9 évite division par zéro

    # 3. Génération des splashs
    print(f"Génération de {len(df)} éléments 'splash'...")
    for i, row in df.iterrows():

        # --- GESTION DU RENDU DÉTERMINISTE ---
        # Initialise le générateur aléatoire en se basant sur le contenu de la ligne
        random.seed(hash(tuple(row)))
        # --- FIN DE LA GESTION ---

        # Mappage des données
        # ValueA (Coordonnees) -> Position X
        x = int(100 + coord_norm.iloc[i] * (WIDTH - 200)) 
        # Position Y (aléatoire mais déterministe grâce au seed)
        y = random.randint(100, HEIGHT - 100)
        
        # ValueB (Couleur) -> R, G, B
        base = int(row["ValueB"])
        r = int(base % 256)
        g = int((base * 2) % 256)
        b = int((255 - base) % 256)

        # Splash principal
        radius = random.randint(50, 120)
        intensity = random.uniform(0.8, 1.4)
        draw_color_splash(draw, x, y, (r, g, b), intensity=intensity, radius=radius)

        # Coulures verticales
        for _ in range(random.randint(1, 3)):
            drip_x = x + random.randint(-20, 20)
            drip_y_end = min(HEIGHT - 10, y + random.randint(50, 150))
            draw.line((drip_x, y, drip_x, drip_y_end), fill=(r, g, b, 180), width=random.randint(3, 6))

    # 4. Effet lumière douce
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 20))
    image = Image.alpha_composite(image, overlay)

    # 5. Sauvegarde
    try:
        final_image = image.convert("RGB")
        final_image.save(output_path, quality=95)
    except Exception as e:
        print(f"Erreur critique lors de la sauvegarde de l'image : {e}")
        return ""
    
    print(f"Image 'Splash Art' générée et sauvegardée sous : {output_path}")
    return output_path


# --- 3. Validation de Fichier (inchangée) ---

def validate_file_type(filename: str) -> bool:
    """Valide si l'extension du fichier est supportée."""
    if filename is None:
        return False
    filename_lower = filename.lower()
    return filename_lower.endswith(('.csv', '.json'))
