import streamlit as st

st.markdown("<h1 style='text-align: center;'>Quranify</h1>", unsafe_allow_html=True)

# 1. ምስል
st.image("https://images.unsplash.com/photo-1590595971752-167812258836?q=80&w=200", width=200)

# 2. የቁርአን ኦዲዮ (የሙከራ ሊንክ)
st.write("ሱራ አል-ፋቲሃ")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

# 3. ቁልፎች
col1, col2, col3 = st.columns(3)
with col1: st.button("⏪")
with col2: st.button("▶️")
with col3: st.button("⏩")
