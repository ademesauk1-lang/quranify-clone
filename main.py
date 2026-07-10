import streamlit as st
import requests

# የቃሪዎች መረጃ
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

st.title("📖 Quranify Pro")

# Sidebar
st.sidebar.header("ቅንጅቶች / Settings")
lang_choice = st.sidebar.selectbox("ቋንቋ / Language", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("ቃሪ ይምረጡ / Select Qari", list(qari_data.keys()))
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)

@st.cache_data
def get_surah_list():
    response = requests.get(f"{API_BASE}/surah")
    return response.json()['data']

surahs = get_surah_list()
selected_surah = st.selectbox("ሱራ ይምረጡ / Select Surah", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']}")

if st.button("አሳይ / Load"):
    with st.spinner('እየጫነ ነው...'):
        lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"
        
        # 1. ጽሁፍ መጫን
        text_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}")
        text_data = text_resp.json().get('data', {})
        
        # 2. ኦዲዮ መጫን
        audio_resp = requests.get(f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}")
        audio_data = audio_resp.json().get('data', {})

        if text_data:
            st.subheader(f"{text_data.get('englishName', '')} - {text_data.get('name', '')}")
            
            # ኦዲዮ ካለ ለማጫወት
            if audio_data and 'ayahs' in audio_data and len(audio_data['ayahs']) > 0:
                st.audio(audio_data['ayahs'][0]['audio'])
            else:
                st.warning("ይህ ቃሪ ለዚህ ሱራ ኦዲዮ የለውም።")
            
            # ጽሁፎችን ማሳየት
            for ayah in text_data.get('ayahs', []):
                st.write(f"**{ayah.get('numberInSurah')}.** {ayah.get('text')}")
        else:
            st.error("መረጃ ማምጣት አልተቻለም። እባክዎ እንደገና ይሞክሩ።")

# CSS
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)
