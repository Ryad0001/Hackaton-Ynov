import pandas as pd
import json
from typing import Union, Dict, Any
import os
import random
import math
import colorsys
from PIL import Image, ImageDraw

def normalise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    colonnes_num = df.select_dtypes(include=["number"]).columns.tolist()
    colonnes_text = df.select_dtypes(exclude=["number"]).columns.tolist()
    
    if len(colonnes_num) < 2:
        raise ValueError("Le fichier doit contenir au moins deux colonnes numériques.")
    
    cat_col = colonnes_text[0] if len(colonnes_text) > 0 else "categorie_inconnue"
    valA_col = colonnes_num[0]
    valB_col = colonnes_num[1]

    new_df = pd.DataFrame()
    new_df["Category"] = df[cat_col] if len(colonnes_text) > 0 else "Inconnue"
    new_df["ValueA"] = df[valA_col]
    new_df["ValueB"] = df[valB_col]
    
    return new_df


def process_data(uploaded_file) -> Dict[str, Any]:
    if uploaded_file is None:
        return {}
    
    filename = uploaded_file.name.lower()
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            return {"error": f"Format de fichier non supporté : {filename}"}
            
        if df.empty:
            return {"error": "Le fichier est vide"}
            
        try:
            df_normalise = normalise_dataframe(df)
        except ValueError as e:
            print(f"Erreur de normalisation : {e}")
            return {"error": f"Erreur de normalisation : {e}"}
        
        return {
            "type": "csv" if filename.endswith('.csv') else "json",
            "shape": df_normalise.shape,
            "columns": df_normalise.columns.tolist(),
            "preview": df_normalise.head(5).to_dict('records'),
            "dataframe": df_normalise
        }
            
    except Exception as e:
        return {"error": f"Erreur lors de la lecture du fichier : {e}"}


def create_gradient_background(width, height, top_color=(20, 20, 30), bottom_color=(80, 40, 100)):
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
    Génère une œuvre d'art "Splash Art" (Pillow) avec couleurs HSV
    et rendu déterministe.
    """
    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "generated_art.png")

    if "dataframe" not in processed_data:
        print("❌ Erreur : DataFrame non trouvé dans processed_data.")
        return "" 

    df = processed_data['dataframe']
    
    WIDTH = 1000
    HEIGHT = 700

    # --- DÉBUT DE L'ALGORITHME "SPLASH ART" ---
    
    # 1. Fond dégradé
    if background_style == 'light':
        background = create_gradient_background(WIDTH, HEIGHT, top_color=(240, 240, 230), bottom_color=(200, 200, 220))
    else:
        background = create_gradient_background(WIDTH, HEIGHT, top_color=(20, 20, 30), bottom_color=(80, 40, 100))

    image = background.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")

    # 2. Normalisation des données pour les axes visuels
    # ValueA (Coordonnees) -> Position X
    min_coord = df["ValueA"].min()
    max_coord = df["ValueA"].max()
    coord_norm = (df["ValueA"] - min_coord) / (max_coord - min_coord + 1e-9)
    
    # ValueB (Couleur) -> Teinte HSV
    min_color = df["ValueB"].min()
    max_color = df["ValueB"].max()
    color_norm = (df["ValueB"] - min_color) / (max_color - min_color + 1e-9)

    # 3. Génération des splashs
    print(f"Génération de {len(df)} éléments 'splash'...")
    for i, row in df.iterrows():

        # --- GESTION DU RENDU DÉTERMINISTE ---
        random.seed(hash(tuple(row)))
        # --- FIN DE LA GESTION ---

        # Mappage des données
        x = int(100 + coord_norm.iloc[i] * (WIDTH - 200)) 
        y = random.randint(100, HEIGHT - 100)
        
        # --- LOGIQUE DE COULEUR (HSV Arc-en-ciel) ---
        teinte = color_norm.iloc[i] # ValueB normalisée
        saturation = 1.0
        valeur = 1.0
        
        rgb_tuple = colorsys.hsv_to_rgb(teinte, saturation, valeur)
        r = int(rgb_tuple[0] * 255)
        g = int(rgb_tuple[1] * 255)
        b = int(rgb_tuple[2] * 255)
        # --- FIN DE LA LOGIQUE DE COULEUR ---

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
    
    # Pas besoin de plt.close(fig), car nous n'utilisons pas Matplotlib
    
    print(f"Image 'Splash Art' générée et sauvegardée sous : {output_path}")
    return output_path


# --- 3. Validation de Fichier (inchangée) ---

def validate_file_type(filename: str) -> bool:
    """Valide si l'extension du fichier est supportée."""
    if filename is None:
        return False
    filename_lower = filename.lower()
    return filename_lower.endswith(('.csv', '.json'))
