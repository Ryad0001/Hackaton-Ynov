"""
Module de traitement des données pour ANTKATHON
"""

import pandas as pd
import json
from typing import Union, Dict, Any


def process_data(uploaded_file) -> Dict[str, Any]:
    """
    Traite les données du fichier uploadé.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        Dict contenant les données traitées
    
    Raises:
        ValueError: Si le format de fichier n'est pas supporté
    """
    if uploaded_file is None:
        return {}
    
    # Vérifier l'extension du fichier
    filename = uploaded_file.name.lower()
    
    if filename.endswith('.csv'):
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file)
        
        # Vérifier si le DataFrame est vide
        if df.empty:
            return {"error": "Le fichier CSV est vide"}
        
        # Retourner un aperçu des données traitées
        return {
            "type": "csv",
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict('records'),
            "summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        }
    
    elif filename.endswith('.json'):
        # Lire le fichier JSON
        content = uploaded_file.read().decode('utf-8')
        data = json.loads(content)
        
        # Convertir en DataFrame pour faciliter le traitement si c'est une liste
        if isinstance(data, list):
            df = pd.DataFrame(data)
            return {
                "type": "json",
                "shape": df.shape,
                "columns": df.columns.tolist() if hasattr(df, 'columns') else [],
                "preview": df.head(5).to_dict('records') if hasattr(df, 'head') else data[:5] if isinstance(data, list) else data,
                "summary": df.describe().to_dict() if hasattr(df, 'describe') and len(df.select_dtypes(include=['number']).columns) > 0 else {}
            }
        else:
            return {
                "type": "json",
                "data": data
            }
    
    else:
        raise ValueError(f"Format de fichier non supporté : {filename}")


def generate_art(processed_data: Dict[str, Any]) -> str:
    """
    Génère une œuvre d'art à partir des données traitées.
    
    Args:
        processed_data: Données traitées par process_data
        
    Returns:
        Chemin vers l'image générée (simulé pour l'instant)
    
    Note:
        Cette fonction sera implémentée plus tard avec un vrai algorithme de génération
    """
    # Pour l'instant, on simule juste la génération
    # TODO: Implémenter l'algorithme de génération d'art abstrait
    return "data/generated_art.png"


def validate_file_type(filename: str) -> bool:
    if filename is None:
        return False
    filename_lower = filename.lower()
    return filename_lower.endswith(('.csv', '.json'))
