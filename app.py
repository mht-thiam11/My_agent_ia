import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from duckduckgo_search import DDGS

# ==========================================
# 1. INITIALISATION & BRANDING (VOTRE CV VISUEL)
# ==========================================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration de la page
st.set_page_config(page_title="Agent IA | Mohamet THIAM", page_icon="🚀", layout="wide")

# --- La barre latérale (Sidebar) pour votre profil ---
with st.sidebar:
    # Injection de CSS pour sublimer la photo et gérer l'interface
    st.markdown("""
    <style>
        /* 1. Rendre l'image ronde, centrée et garder la netteté */
        [data-testid="stSidebar"] [data-testid="stImage"] { 
            display: flex;
            justify-content: center;
        }
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            border-radius: 50%;
            width: 150px !important;
            height: 150px !important;
            object-fit: cover !important; /* Maintient les proportions sans flou */
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* 2. Cacher UNIQUEMENT le bouton Deploy et le menu (pour garder la flèche de la sidebar) */
        .stAppDeployButton {display: none !important;}
        [data-testid="stAppDeployButton"] {display: none !important;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # On charge l'image en pleine largeur pour garder la qualité, le CSS fera le cercle de 150px
    st.image("profile.png", use_container_width=True)
    st.title("👨‍💻 Mohamet THIAM")
    st.write("Passionné par le développement full-stack, la data et l'Intelligence Artificielle.")
    st.write("🎓 *Master 1 MIAGE ISI - Paris Nanterre*")
    
    # Mise en avant de votre recherche d'alternance
    st.success("🎯 **Recherche Alternance (24 mois)**\n\nÀ partir de Septembre 2026\n\n*Rythme : 3j/2j ou 3 sem/3 sem.*")
    
    st.divider() # Ligne de séparation
    
    # Vos liens professionnels
    st.write("🔗 **[Mon Portfolio Web](https://enchanting-kitsune-93e7ad.netlify.app/)**")
    st.write("💼 **[Mon LinkedIn](https://www.linkedin.com/in/mohamet-thiam/)**")
    st.write("🐙 **[Mon GitHub](https://github.com/mht-thiam11/)**")
    st.write("✉️ **moustaphat275@gmail.com**")
    st.write("📞 **07 58 41 23 91**")
    st.divider()
    st.caption("Ce projet démontre mes compétences en IA (API Gemini, Tool Calling) et en architecture Python (Streamlit).")

st.title("🚀 Assistant IA de Mohamet Thiam")
st.caption("Posez des questions sur le web ou demandez-moi de vous parler des compétences et projets de Mohamet !")

# ==========================================
# 2. OUTILS DE L'AGENT
# ==========================================
def recherche_web(requete: str) -> str:
    """Recherche des informations récentes sur internet."""
    st.toast(f"🔍 Recherche web en cours : {requete}") 
    try:
        resultats = DDGS().text(requete, max_results=3)
        return str(resultats) if resultats else "Aucun résultat trouvé."
    except Exception as e:
        return f"Erreur de recherche : {e}"

# ==========================================
# 3. MÉMOIRE ET CERVEAU DE L'APPLICATION
# ==========================================
if "chat" not in st.session_state:
    # --- Le Prompt Engineering sur mesure (Votre CV pour l'IA) ---
    instructions = """
    Tu es l'assistant personnel virtuel et le porte-parole de Mohamet THIAM.
    Mohamet est un développeur Full-Stack & Data talentueux, passionné par l'Intelligence Artificielle.
    Il est admis en Master MIAGE ISI (Ingénierie des Systèmes Intelligents) à l’Université Paris Nanterre.
    
    SON OBJECTIF PRINCIPAL : Il recherche activement une alternance de 24 mois à partir de septembre 2026 (rythme 3j entreprise / 2j école ou 3 sem / 3 sem).

    SES COMPÉTENCES :
    - Data & IA : Power BI, Streamlit, Pandas, NumPy, scikit-learn, algorithmes d'embeddings (pgvector).
    - Langages : Python, SQL/PLSQL, Java, JavaScript, PHP.
    - Web & Back-end : FastAPI, Django, API REST, SQLAlchemy.
    - Outils : PostgreSQL, Docker, Git/GitHub, Environnement Linux/Windows.

    SES PROJETS PHARES (Donne ces détails précis s'il pose des questions dessus) :
    1. Recherche sémantique locale (Python, FastAPI, PostgreSQL, pgvector, SQLAlchemy, Docker) : Conception d’une application de recherche avec embeddings multilingues de 384 dimensions, stockage vectoriel et classement des 10 résultats les plus pertinents ; documentation Swagger/OpenAPI.
    2. Make Graphe Great Again (Python, NLP, SQL, Pandas, NetworkX, Gephi) : Analyse et structuration de 65 918 publications textuelles ; génération d’un graphe de 500 nœuds et 81 036 relations pour identifier mots-clés, tendances et communautés.
    3. RisingTown : Smart City (Python, Django, JavaScript, SQLite, API REST, Git) : Développement agile d’une plateforme web avec 4 rôles utilisateurs, modèle de données persistant, interfaces AJAX/Fetch et déploiement sur PythonAnywhere.
    4. LogiFête (PHP, JavaScript, MariaDB, SQL, Apache) : Modélisation et développement d’un PGI (Progiciel de Gestion Intégré) répondant à 3 enjeux métier : optimisation logistique, performance commerciale et gestion du patrimoine.
    5. Donjon Mystère (Unity, C#, JavaScript, HTML, CSS) : Conception d’un jeu intégrant une IA pour les ennemis, capables de patrouiller, poursuivre et attaquer selon le comportement du joueur.

    🚨 RÈGLE STRICTE CONCERNANT LES PROJETS :
    Après avoir présenté ou résumé un ou plusieurs de ces projets avec ces détails, tu DOIS TOUJOURS proposer à l'utilisateur de consulter le portfolio en ligne pour voir beaucoup plus de détails visuels et techniques.
    Tu incluras SYSTÉMATIQUEMENT ce lien cliquable à la fin de ta réponse : [Cliquez ici pour découvrir mon Portfolio en détails](https://enchanting-kitsune-93e7ad.netlify.app/#top).

    Ton but est de mettre en valeur Mohamet avec professionnalisme et courtoisie.
    """
    
    config_agent = types.GenerateContentConfig(
        tools=[recherche_web],
        temperature=0.7,
        system_instruction=instructions
    )
    
    # NOUVEAU : 10 modèles en cascade pour une haute disponibilité (anti-crash)
    st.session_state.modeles_fallback = [
        "gemini-flash-lite-latest",
        "gemini-1.5-flash-8b",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-flash-latest",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]
    
    st.session_state.current_model = st.session_state.modeles_fallback[0]
    st.session_state.chat = client.chats.create(
        model=st.session_state.current_model,
        config=config_agent
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis l'assistant IA de Mohamet THIAM. Je peux chercher des informations sur Internet pour vous, ou vous présenter le profil de Mohamet (compétences, projets, recherche d'alternance). Que souhaitez-vous savoir ?"}
    ]

# Affichage de l'historique
# Affichage de l'historique
for msg in st.session_state.messages:
    # On attribue une belle icône selon qui parle
    icone = "🧑‍💻" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=icone):
        st.markdown(msg["content"])


# ==========================================
# 4. ZONE DE TEXTE (CHAT) AVEC FALLBACK
# ==========================================
if prompt := st.chat_input("Posez votre question..."):
    
    # 1. Icône du visiteur
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Icône de l'agent IA avec Fallback
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Je réfléchis..."):
            reponse = None
            erreur = None
            
            # BOUCLE DE SÉCURITÉ : On essaie les modèles un par un
            for modele in st.session_state.modeles_fallback:
                try:
                    # S'il y a eu un crash et qu'on doit passer au modèle suivant
                    if st.session_state.current_model != modele:
                        st.session_state.current_model = modele
                        # On recrée une connexion avec le nouveau modèle
                        st.session_state.chat = client.chats.create(
                            model=modele,
                            config=config_agent
                        )
                        st.toast(f"🔄 Serveur occupé : basculement sur {modele}")
                    
                    # On tente d'envoyer la question
                    reponse = st.session_state.chat.send_message(prompt)
                    break # SUCCÈS ! On sort de la boucle
                    
                except Exception as e:
                    erreur = e
                    continue # ÉCHEC : On passe au modèle suivant
            
            # AFFICHAGE DU RÉSULTAT FINAL
            if reponse:
                st.markdown(reponse.text)
                st.session_state.messages.append({"role": "assistant", "content": reponse.text})
            else:
                st.error(f"Désolé, tous mes serveurs de secours sont actuellement saturés. Réessayez dans 2 minutes. (Erreur : {erreur})")