import streamlit as st

# 1. ርዕስ እና ዲዛይን
st.title("📖 Quranify")
st.markdown("---")

# 2. የኦዲዮ ማጫወቻ (የሙከራ ሊንክ)
st.subheader("አሁን እየተጫወተ ነው:")
st.write("ሱራ አል-ፋቲሃ")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

# 3. አግድም ቁልፎች (Horizontal Controls)
col1, col2, col3 = st.columns(3)
with col1: 
    st.button("⏪", use_container_width=True)
with col2: 
    st.button("▶️", use_container_width=True)
with col3: 
    st.button("⏩", use_container_width=True)

st.markdown("---")

# 4. የቃሪዎች ወይም የሱራዎች ዝርዝር (መጀመር ያለብን ክፍል)
st.subheader("የሱራዎች ዝርዝር")
surahs = ["ሱራ አል-ፋቲሃ", "ሱራ አል-በቀራ", "ሱራ አል-ኢምራን", "ሱራ አን-ኒሳእ"]

for surah in surahs:
    if st.button(f"🎧 {surah}"):
        st.write(f"የተመረጠው: {surah}")
