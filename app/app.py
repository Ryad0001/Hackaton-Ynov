import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from algos.data_processor import process_data, generate_art, validate_file_type

st.set_page_config(
    page_title="ANTKATHON",
    page_icon=None,
    layout="wide"
)

def main():
    st.title("ANTKATHON - Générateur d'Art Abstraît")
    st.markdown("---")
    
    st.markdown("""
    Bienvenue dans l'application de génération d'art abstrait à partir de données.
    Téléversez un fichier CSV ou JSON et découvrez comment vos données peuvent devenir une œuvre d'art unique !
    """)
    
    st.markdown("---")
    
    st.subheader("Téléversement de Fichier")
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV ou JSON",
        type=['csv', 'json'],
        help="Seuls les fichiers CSV et JSON sont acceptés"
    )
    
    if uploaded_file is not None:
        if not validate_file_type(uploaded_file.name):
            st.error("Format de fichier non supporté. Veuillez téléverser un fichier CSV ou JSON.")
        else:
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['filename'] = uploaded_file.name
            
            st.success(f"Fichier téléversé avec succès : {uploaded_file.name}")
            
            st.subheader("Aperçu des Données")
            
            try:
                processed_data = process_data(uploaded_file)
                
                if processed_data.get('type') == 'csv':
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)
                    
                    st.markdown(f"**Shape :** {df.shape[0]} lignes × {df.shape[1]} colonnes")
                    st.dataframe(df.head(5), use_container_width=True)
                    
                    if processed_data.get('summary'):
                        with st.expander("Statistiques descriptives"):
                            st.dataframe(pd.DataFrame(processed_data['summary']), use_container_width=True)
                
                elif processed_data.get('type') == 'json':
                    uploaded_file.seek(0)
                    import json
                    content = uploaded_file.read().decode('utf-8')
                    data = json.loads(content)
                    
                    if isinstance(data, list):
                        if len(data) > 0:
                            df = pd.DataFrame(data)
                            st.markdown(f"**Nombre d'éléments :** {len(data)}")
                            st.dataframe(df.head(5), use_container_width=True)
                    else:
                        st.json(data)
                
                st.session_state['processed_data'] = processed_data
                
                st.markdown("---")
                
                st.subheader("Génération de l'Œuvre d'Art")
                
                if st.button("Générer l'Œuvre d'Art", type="primary", use_container_width=True):
                    with st.spinner("Génération de l'œuvre d'art en cours..."):
                        try:
                            art_path = generate_art(processed_data)
                            
                            if art_path and os.path.exists(art_path):
                                st.success("Génération Réussie !")
                                
                                st.markdown("---")
                                
                                st.subheader("Votre Œuvre d'Art Générée")
                                
                                st.image(
                                    art_path,
                                    caption="Votre œuvre d'art générée à partir de vos données",
                                    use_container_width=True
                                )
                                
                                with open(art_path, "rb") as img_file:
                                    st.download_button(
                                        label="Télécharger l'image",
                                        data=img_file,
                                        file_name="generated_art.png",
                                        mime="image/png",
                                        use_container_width=True
                                    )
                            else:
                                st.error("Erreur : L'image générée n'a pas pu être créée.")
                            
                        except Exception as e:
                            st.error(f"Erreur lors de la génération : {str(e)}")
                
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {str(e)}")
    
    with st.sidebar:
        st.header("À Propos")
        st.markdown("""
        **ANTKATHON - Générateur d'Art Abstraît**
        
        Cette application permet de transformer vos données en œuvres d'art abstrait.
        
        **Formats supportés :**
        - CSV (.csv)
        - JSON (.json)
        
        **Comment utiliser :**
        1. Téléversez votre fichier de données
        2. Consultez l'aperçu de vos données
        3. Cliquez sur "Générer l'Œuvre d'Art"
        4. Admirez le résultat !
        """)
        
        st.markdown("---")
        st.markdown("Développé par Oubay, Adam, Ryad et Azad")
    
    st.markdown("---")
    st.markdown("""<div style='text-align: center; color: #888;'>
    ANTKATHON - Transformez vos données en art abstrait
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()