import streamlit as st

# የገጽ መግለጫ
st.set_page_config(page_title="Quranify Clone", layout="centered")

# Custom CSS ለ dark theme
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    </style>
""", unsafe_allow_html=True)

# ርዕስ
st.title("📖 Quranify")
st.subheader("በጣም የተወደዱ ቃሪዎች")

# የቃሪዎች ዝርዝር (ምሳሌ)
reciters = ["Fatih Seferagig", "Abdulrahman Al-Suwayid", "Abdullah Al-Qarafi"]
cols = st.columns(3)

for i, name in enumerate(reciters):
    with cols[i]:
        st.image("https://via.placeholder.com/150", caption=name)
        if st.button(f"አጫውት", key=name):
            st.write(f"አሁን እየተጫወተ ነው: {name}")

# የድምጽ ማቀናበሪያ (Background sound section)
st.divider()
st.subheader("የጀርባ ድምጽ (Background Sounds)")
sound_option = st.selectbox("ድምጽ ይምረጡ:", ["ምንም", "ዝናብ", "ወንዝ", "ነፋስ"])
st.info(f"የተመረጠው የጀርባ ድምጽ: {sound_option}")
