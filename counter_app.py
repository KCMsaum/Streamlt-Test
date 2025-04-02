import streamlit as st
import time

# Initialize session state variables
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'running' not in st.session_state:
    st.session_state.running = False

# Function to increment the counter
def increment_counter():
    while st.session_state.running:
        st.session_state.count += 1
        time.sleep(1)  # Wait 1 second between increments
        st.rerun()  # Rerun the app to update the display

# App layout
st.title("Simple Counter App")

# Display the current count
st.header(f"Count: {st.session_state.count}")

# Create columns for buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start", disabled=st.session_state.running):
        st.session_state.running = True
        st.rerun()  # Rerun to start the counter

with col2:
    if st.button("Stop", disabled=not st.session_state.running):
        st.session_state.running = False
        st.rerun()  # Rerun to stop the counter

with col3:
    if st.button("Reset"):
        st.session_state.count = 0
        st.session_state.running = False
        st.rerun()  # Rerun to update the display

# Start the counter if running
if st.session_state.running:
    increment_counter()