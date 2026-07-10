import streamlit as st
import requests

# 1. መረጃውን ከኢንተርኔት ለመጎተት የሚያስችል የ API ሊንክ
API_BASE = "https://api.alquran.cloud/v1"

# 2. የሱራ ዝርዝርን አንድ ጊዜ ብቻ ለመጫን (Cache)
@st.cache_data
def get_surah_list():
    response = requests.get(f"{API_BASE}/surah")
    return response.json()['data']

# 3. ሱራውን በቋንቋ እና በትርጉም ለማምጣት
def get_surah_content(number, lang_key):
    # lang_key: 'en.asad' (English), 'am.sadiq' (Amharic)
    url = f"{API_BASE}/surah/{number}/{lang_key}"
    response = requests.get(url)
    return response.json()['data']

st.title("📖 Quranify Pro")

# 4. ቋንቋ መምረጫ
lang_choice = st.selectbox("ትርጉም ይምረጡ / Select Translation", ["English", "Amharic"])
lang_key = "en.asad" if lang_choice == "English" else "am.sadiq"

# 5. ሱራ መምረጫ
surahs = get_surah_list()
selected_surah = st.selectbox("ሱራ ይምረጡ / Select Surah", surahs, format_func=lambda x: f"{x['number']}. {x['englishName']} ({x['name']})")

if st.button("አሳይ / Load"):
    with st.spinner('እየጫነ ነው...'):
        data = get_surah_content(selected_surah['number'], lang_key)
        
        st.subheader(f"{data['englishName']} - {data['name']}")
        
        # ሱራውን በየአያቱ ማሳየት
        for ayah in data['ayahs']:
            st.write(f"**{ayah['numberInSurah']}.** {ayah['text']}")
            st.markdown("---")

# CSS ለዲዛይን
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)
