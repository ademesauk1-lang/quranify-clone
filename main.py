import streamlit as st
import requests

# 1. ቃሪዎች
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

# 2. የዲዛይን (CSS) ማሻሻያ - ታችኛውን ክፍል ለማሳመር
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .footer { text-align: center; color: #888; font-size: 12px; margin-top: 50px; padding: 10px; border-top: 1px solid #333; }
    .ayah-box { background-color: #1a1a1a; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Quranify Pro")

# 3. Sidebar
st.sidebar.header("⚙️ Settings")
lang_choice = st.sidebar.selectbox("Language / ቋንቋ", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("Select Qari / ቃሪ ይምረጡ", list(qari_data.keys()))
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)

# 4. ሱራ ዝርዝር
@st.cache_data
def get_surah_list():
    try: return requests.get(f"{API_BASE}/surah").json().get('data', [])
    except: return []

surahs = get_surah_list()
selected_surah = st.selectbox("Select Surah / ሱራ ይምረጡ", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']}")

if st.button("Load Surah / ሱራውን አሳይ"):
    with st.spinner('Loading...'):
        lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"
        
        # ጽሁፍ እና ኦዲዮ እና ተፍሲር
        text_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}").json().get('data', {})
        audio_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}").json().get('data', {})
        tafsir_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/en.muyassar").json().get('data', {}) # English Tafsir

        st.subheader(f"{text_resp.get('englishName')} - {text_resp.get('name')}")
        
        # ኦዲዮ
        if audio_resp and 'ayahs' in audio_resp:
            st.audio(audio_resp['ayahs'][0].get('audio'))

        # ጽሁፍ እና ተፍሲር
        for i, ayah in enumerate(text_resp.get('ayahs', [])):
            with st.container():
                st.markdown(f"<div class='ayah-box'><strong>{ayah.get('numberInSurah')}.</strong> {ayah.get('text')}</div>", unsafe_allow_html=True)
                
                # ተፍሲር (Expander)
                with st.expander("Show Tafsir / ተፍሲር አሳይ"):
                    tafsir_text = tafsir_resp['ayahs'][i].get('text') if tafsir_resp else "Tafsir not available."
                    st.write(f"**Tafsir:** {tafsir_text}")

# 5. Bottom/Footer Design
st.markdown("<div class='footer'>Quranify Pro © 2026 | Built for Learning & Faith</div>", unsafe_allow_html=True)
