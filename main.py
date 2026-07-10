import streamlit as st
import requests

# 1. ቃሪዎች
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

# 2. የዲዛይን (CSS) ማሻሻያ - የላክከውን የፎቶ ስታይል ለመምሰል
st.markdown("""
    <style>
    /* የጀርባ ቀለም */
    .stApp { background-color: #121212; color: #ffffff; }
    
    /* የቁርአን ሳጥን ስታይል */
    .ayah-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* ጽሁፍ */
    .ayah-text { font-size: 18px; line-height: 1.6; color: #e0e0e0; }
    .ayah-num { font-weight: bold; color: #4CAF50; margin-right: 10px; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0d0d0d; }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Quranify Pro")

# 3. Sidebar - ቅንጅቶች
st.sidebar.header("⚙️ Settings")
lang_choice = st.sidebar.selectbox("Language / ቋንቋ", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("Select Qari / ቃሪ ይምረጡ", list(qari_data.keys()))
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)
show_tafsir = st.sidebar.checkbox("Show Tafsir / ተፍሲር አሳይ")

# 4. ሱራ ዝርዝር
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
        
        # API ጥሪ
        text_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}").json().get('data', {})
        audio_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}").json().get('data', {})
        tafsir_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/en.muyassar").json().get('data', {})

        if text_resp:
            st.subheader(f"{text_resp.get('englishName')} - {text_resp.get('name')}")
            
            # ኦዲዮ ማጫወቻ
            if audio_resp and 'ayahs' in audio_resp:
                st.audio(audio_resp['ayahs'][0].get('audio'))

            # አያቶችን በሳጥን ማሳያ
            for i, ayah in enumerate(text_resp.get('ayahs', [])):
                # የሳጥን ዲዛይን (Card)
                st.markdown(f"""
                    <div class='ayah-card'>
                        <span class='ayah-num'>{ayah.get('numberInSurah')}.</span>
                        <span class='ayah-text'>{ayah.get('text')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # ተፍሲር
                if show_tafsir:
                    with st.expander("📖 Tafsir"):
                        tafsir_text = tafsir_resp['ayahs'][i].get('text') if tafsir_resp else "Not available."
                        st.write(tafsir_text)
        else:
            st.error("መረጃ ማምጣት አልተቻለም።")

# 6. Footer
st.markdown("<br><hr><center>Quranify Pro © 2026</center>", unsafe_allow_html=True)
