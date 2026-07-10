import streamlit as st

st.set_page_config(page_title="Quranify", layout="centered")

# 1. የሱራዎች መረጃ (እዚህ ላይ እውነተኛውን የድምጽ ሊንክ ማድረግ ትችላለህ)
surah_data = {
    "ሱራ አል-ፋቲሃ": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "ሱራ አል-በቀራ": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "ሱራ አን-ኒሳእ": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}

st.title("📖 Quranify")

# 2. የትኛው ሱራ እንደተመረጠ የሚያስታውስ ቦታ (Session State)
if 'selected_surah' not in st.session_state:
    st.session_state.selected_surah = "ሱራ አል-ፋቲሃ"

# 3. የድምጽ ማጫወቻ
st.subheader(f"አሁን እየተጫወተ ነው: {st.session_state.selected_surah}")
st.audio(surah_data[st.session_state.selected_surah])

st.markdown("---")

# 4. የሱራዎች ዝርዝር (ሲጫን አፕሊኬሽኑን ያዘምናል)
st.subheader("የሱራዎች ዝርዝር")
for surah_name in surah_data.keys():
    if st.button(f"🎧 {surah_name}"):
        st.session_state.selected_surah = surah_name
        st.rerun() # አፕሊኬሽኑን አዲስ ምርጫ እንዲያሳይ እንደገና ያስጀምረዋል
