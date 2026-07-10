import streamlit as st
import requests

# 1. Qaris Data (Name, ID, Photo)
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

# 2. Styling (CSS) - Appun herif adereg yemetay style
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; font-weight: bold; }
    .stSelectbox, .stSidebar { background-color: #1e1e1e; }
    h1, h2, h3 { color: #81c784; }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Quranify Pro")

# 3. Sidebar - Settings
st.sidebar.header("⚙️ Kenjit-och")
lang_choice = st.sidebar.selectbox("Quanqua (Translation)", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("Qari (Reciter)", list(qari_data.keys()))
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)
show_tafsir = st.sidebar.checkbox("Tafsir Asay (Jalalayn)")

# 4. Surah List Fetching
@st.cache_data
def get_surah_list():
    try:
        resp = requests.get(f"{API_BASE}/surah")
        return resp.json().get('data', [])
    except: return []

surahs = get_surah_list()

# 5. Main Logic
if surahs:
    selected_surah = st.selectbox("Surah Yimeretu", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']} ({x['name']})")

    if st.button("Load / Asey"):
        with st.spinner('Yeyalechnal...'):
            lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"
            
            # API Calls
            text_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}").json()
            audio_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}").json()
            
            text_data = text_resp.get('data', {})
            audio_data = audio_resp.get('data', {})
            
            if text_data:
                st.subheader(f"{text_data.get('englishName')} - {text_data.get('name')}")
                
                # Audio Player
                if audio_data and 'ayahs' in audio_data and len(audio_data['ayahs']) > 0:
                    st.audio(audio_data['ayahs'][0].get('audio'))
                else:
                    st.warning("Le-zih surah audio al-tegenem.")

                # Tafsir Logic
                tafsir_data = None
                if show_tafsir:
                    tafsir_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/ar.jalalayn").json()
                    tafsir_data = tafsir_resp.get('data', {}).get('ayahs', [])

                # Display Surah Text & Tafsir
                for i, ayah in enumerate(text_data.get('ayahs', [])):
                    st.write(f"**{ayah.get('numberInSurah')}.** {ayah.get('text')}")
                    if show_tafsir and tafsir_data:
                        st.caption(f"✨ Tafsir: {tafsir_data[i].get('text')}")
                    st.markdown("---")
            else:
                st.error("Mereja-w mochen al-chalem.")
else:
    st.error("Yesurah-och zirzir mechen al-chalem.")
