import streamlit as st
import requests

# 1. ቃሪዎች
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

# 2. የዲዛይን (CSS) - Dark Mode & Cards
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #ffffff; }
    .ayah-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
    }
    .stSidebar { background-color: #0d0d0d; }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Quranify Pro")

# 3. Sidebar - ቅንጅቶች
st.sidebar.header("⚙️ Settings")
lang_choice = st.sidebar.selectbox("Language / ቋንቋ", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("Select Qari / ቃሪ ይምረጡ", list(qari_data.keys()))
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)
show_tafsir = st.sidebar.checkbox("Show Tafsir / ተፍሲር አሳይ")

# 4. ሱራ ዝርዝር መጫኛ
@st.cache_data
def get_surah_list():
    try: return requests.get(f"{API_BASE}/surah").json().get('data', [])
    except: return []

surahs = get_surah_list()
selected_surah = st.selectbox("Select Surah / ሱራ ይምረጡ", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']}")

# 5. ዋናው ስራ
if st.button("Load Surah / ሱራውን አሳይ"):
    with st.spinner('Loading...'):
        lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"
        
        # API ጥሪዎች (ደህንነቱ በተጠበቀ ሁኔታ)
        try:
            text_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}").json()
            audio_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}").json()
            tafsir_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/en.muyassar").json()
            
            text_data = text_resp.get('data', {})
            audio_data = audio_resp.get('data', {})
            tafsir_data = tafsir_resp.get('data', {})
            
            if text_data:
                st.subheader(f"{text_data.get('englishName')} - {text_data.get('name')}")
                
                # ኦዲዮ መጫወቻ (የተጠበቀ)
                audio_list = audio_data.get('ayahs', [])
                if audio_list and len(audio_list) > 0 and audio_list[0].get('audio'):
                    st.audio(audio_list[0]['audio'])
                else:
                    st.warning("ለዚህ ሱራ ኦዲዮ አልተገኘም።")

                # አያቶችን በሳጥን ማሳያ
                for i, ayah in enumerate(text_data.get('ayahs', [])):
                    st.markdown(f"<div class='ayah-card'><strong>{ayah.get('numberInSurah')}.</strong> {ayah.get('text')}</div>", unsafe_allow_html=True)
                    
                    # ተፍሲር (የተጠበቀ)
                    if show_tafsir:
                        tafsir_ayahs = tafsir_data.get('ayahs', [])
                        if i < len(tafsir_ayahs):
                            with st.expander("📖 Tafsir"):
                                st.write(tafsir_ayahs[i].get('text', 'Tafsir not available.'))
            else:
                st.error("መረጃ ማምጣት አልተቻለም።")
        except Exception as e:
            st.error(f"ስህተት ተፈጥሯል: {e}")
