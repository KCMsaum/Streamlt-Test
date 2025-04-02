import streamlit as st
import time
import requests

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'running' not in st.session_state:
    st.session_state.running = False
if 'fact' not in st.session_state:
    st.session_state.fact = "Click button to get a random fact!"

def increment_counter():
    while st.session_state.running:
        st.session_state.count += 1
        time.sleep(1)
        st.rerun()

def get_random_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        st.session_state.fact = response.json()['text']
    except:
        st.session_state.fact = "Failed to fetch fact 😞"

st.title("Enhanced Counter App 🚀")

# Display section
st.header(f"Count: {st.session_state.count}")
st.subheader("Random Fact:")
st.write(st.session_state.fact)

# Control buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Start ▶️", disabled=st.session_state.running):
        st.session_state.running = True
with col2:
    if st.button("Stop ⏹️", disabled=not st.session_state.running):
        st.session_state.running = False
with col3:
    if st.button("Reset 🔄"):
        st.session_state.count = 0
        st.session_state.running = False
with col4:
    if st.button("New Fact 🎲"):
        get_random_fact()

# Run counter if active
if st.session_state.running:
    increment_counter()
