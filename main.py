import streamlit as st

# 1. PWA Meta Tags (ለስልክ አፕሊኬሽን ስሜት)
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Quranify">
""", unsafe_allow_html=True)

# 2. የቋንቋዎች ትርጉም
translations = {
    "Amharic": {"title": "ቁርአኒፋይ", "now_playing": "አሁን እየተጫወተ ነው", "list": "የሱራዎች ዝርዝር"},
    "English": {"title": "Quranify", "now_playing": "Now playing", "list": "List of Surahs"},
    "Arabic": {"title": "القرآن", "now_playing": "يتم التشغيل الآن", "list": "قائمة السور"}
}

# 3. ቅንብር (Config)
st.set_page_config(page_title="Quranify", layout="centered")

# 4. የቋንቋ መምረጫ በጎን በኩል (Sidebar)
lang = st.sidebar.selectbox("ቋንቋ / Language / اللغة", ["Amharic", "English", "Arabic"])
text = translations[lang]

# 5. ዋናው ገጽ
st.title(f"📖 {text['title']}")
st.markdown("---")

# ሱራዎች እና ሊንኮች
surah_data = {
    "Al-Fatiha": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Al-Baqarah": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
}

# የSession State አጠቃቀም
if 'selected_surah' not in st.session_state:
    st.session_state.selected_surah = "Al-Fatiha"

st.subheader(f"{text['now_playing']}: {st.session_state.selected_surah}")
st.audio(surah_data[st.session_state.selected_surah])

st.markdown("---")

# 6. የሱራ ዝርዝር
st.subheader(text['list'])
for surah_name in surah_data.keys():
    if st.button(f"🎧 {surah_name}"):
        st.session_state.selected_surah = surah_name
        st.rerun()

# 7. ፕሮፌሽናል ስታይል (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    div.stButton > button { border-radius: 20px; border: 1px solid #4CAF50; }
    </style>
""", unsafe_allow_html=True)
