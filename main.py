import streamlit as st
import requests

# 1. የቃሪዎች መረጃ (ፎቶ እና ID)
qari_data = {
    "Mishary Alafasy": {"id": "ar.alafasy", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Mishary_Rashid_Alafasy.jpg/220px-Mishary_Rashid_Alafasy.jpg"},
    "Abdul Basit": {"id": "ar.abdulbasit", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Abdul_Basit_Abd_us-Samad.jpg/220px-Abdul_Basit_Abd_us-Samad.jpg"},
    "Abdullah Matroud": {"id": "ar.abdullahmatroud", "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Abdullah_Matroud.jpg/220px-Abdullah_Matroud.jpg"}
}

API_BASE = "https://api.alquran.cloud/v1"

st.title("📖 Quranify Pro")

# 2. Sidebar: ቋንቋ እና ቃሪ ምርጫ
st.sidebar.header("ቅንጅቶች / Settings")
lang_choice = st.sidebar.selectbox("ቋንቋ / Language", ["English", "Amharic"])
selected_qari_name = st.sidebar.selectbox("ቃሪ ይምረጡ / Select Qari", list(qari_data.keys()))

# ቃሪውን ማሳየት
st.sidebar.image(qari_data[selected_qari_name]["photo"], width=150)

# 3. የሱራ ዝርዝር (ከAPI)
@st.cache_data
def get_surah_list():
    response = requests.get(f"{API_BASE}/surah")
    return response.json()['data']

surahs = get_surah_list()
selected_surah = st.selectbox("ሱራ ይምረጡ / Select Surah", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']}")

# 4. መረጃውን መጫን
if st.button("አሳይ / Load"):
    with st.spinner('እየጫነ ነው...'):
        # ጽሁፉን ለማምጣት
        lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"
        text_url = f"{API_BASE}/surah/{selected_surah['number']}/{lang_key}"
        text_data = requests.get(text_url).json()['data']
        
        # ድምጹን ለማምጣት
        audio_url = f"{API_BASE}/surah/{selected_surah['number']}/{qari_data[selected_qari_name]['id']}"
        audio_data = requests.get(audio_url).json()['data']
        
        st.subheader(f"{text_data['englishName']} - {text_data['name']}")
        
        # ኦዲዮ ማጫወቻ
        st.audio(audio_data['ayahs'][0]['audio']) # የመጀመሪያውን አያህ ኦዲዮ ያጫውታል
        
        # ጽሁፎቹን ማሳየት
        for ayah in text_data['ayahs']:
            st.write(f"**{ayah['numberInSurah']}.** {ayah['text']}")

# CSS ስታይል
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)
