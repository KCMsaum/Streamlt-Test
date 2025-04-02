import streamlit as st
import time
import requests
import pandas as pd
import plotly.express as px

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.update({
        'count': 0,
        'running': False,
        'fact': "Click button to get a random fact!",
        'history': pd.DataFrame(columns=['Timestamp', 'Count'])
    })

def increment_counter():
    while st.session_state.running:
        st.session_state.count += 1
        st.session_state.history = pd.concat([
            st.session_state.history,
            pd.DataFrame([{'Timestamp': pd.Timestamp.now(), 'Count': st.session_state.count}])
        ])
        time.sleep(1)
        st.rerun()

def get_random_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        st.session_state.fact = response.json()['text']
    except Exception as e:
        st.session_state.fact = f"Error: {str(e)}"

# Main app layout
st.title("Enhanced Counter App 📈")

# Display section
col1, col2 = st.columns(2)
with col1:
    st.header(f"Current Count: {st.session_state.count}")
    st.button("New Fact 🎲", on_click=get_random_fact)
    st.write(st.session_state.fact)

with col2:
    if not st.session_state.history.empty:
        st.subheader("Count History")
        fig = px.line(st.session_state.history, x='Timestamp', y='Count', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# Control buttons
cols = st.columns(4)
with cols[0]:
    if st.button("Start ▶️", disabled=st.session_state.running):
        st.session_state.running = True
with cols[1]:
    if st.button("Stop ⏹️", disabled=not st.session_state.running):
        st.session_state.running = False
with cols[2]:
    if st.button("Reset 🔄"):
        st.session_state.count = 0
        st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Count'])
with cols[3]:
    if st.button("Clear History 🗑️"):
        st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Count'])

# Run counter if active
if st.session_state.running:
    increment_counter()
