import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd
import plotly.express as px

# Blynk configuration
BLYNK_SERVER = "https://sgp1.blynk.cloud"
BLYNK_TOKEN = "4rKddVxLgMJBfztxOi8Y1-0IsF5QeE8a"

def send_to_blynk(virtual_pin, value):
    """Send value to Blynk virtual pin"""
    url = f"{BLYNK_SERVER}/external/api/update"
    params = {
        "token": BLYNK_TOKEN,
        f"V{virtual_pin}": value
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error sending data: {str(e)}")
        return False

def get_from_blynk(virtual_pin):
    """Get value from Blynk virtual pin"""
    url = f"{BLYNK_SERVER}/external/api/get"
    params = {
        "token": BLYNK_TOKEN,
        f"V{virtual_pin}": ""
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        st.error(f"API Error: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# Initialize session state
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'v1_value' not in st.session_state:
    st.session_state.v1_value = "N/A"
if 'last_update' not in st.session_state:
    st.session_state.last_update = "Never"
if 'history_data' not in st.session_state:
    st.session_state.history_data = pd.DataFrame(columns=['Timestamp', 'Value'])

# Streamlit app layout
st.title("Blynk IoT Dashboard with Plotting 📈")

# Send data to V0
with st.form("send_form"):
    v0_value = st.number_input("Enter value to send to V0:", step=1)
    if st.form_submit_button("Send to V0 🚀"):
        if send_to_blynk(0, v0_value):
            st.success(f"Successfully sent {v0_value} to V0!")
        else:
            st.error("Failed to send data to V0")

# Receive data section
st.subheader("Received Data from V1")

# Auto-refresh control
auto_refresh = st.checkbox(
    "Enable Auto-Refresh (every 5s)",
    value=st.session_state.auto_refresh,
    key='auto_refresh_checkbox'
)

# Update session state when checkbox changes
if auto_refresh != st.session_state.auto_refresh:
    st.session_state.auto_refresh = auto_refresh
    st.rerun()

# Manual refresh button
if st.button("Refresh Data 🔄") or st.session_state.auto_refresh:
    data = get_from_blynk(1)
    if data is not None:
        try:
            numeric_value = float(data)
            st.session_state.v1_value = numeric_value
            now = datetime.now()
            st.session_state.last_update = now.strftime("%H:%M:%S")
            
            # Add to history
            new_entry = pd.DataFrame({
                'Timestamp': [now],
                'Value': [numeric_value]
            })
            st.session_state.history_data = pd.concat([
                st.session_state.history_data, 
                new_entry
            ]).reset_index(drop=True)
        except ValueError:
            st.error(f"Received non-numeric value: {data}")

# Display current value
col1, col2 = st.columns(2)
with col1:
    st.metric("Current V1 Value", st.session_state.v1_value)
    st.caption(f"Last updated: {st.session_state.last_update}")

with col2:
    if st.button("Clear History"):
        st.session_state.history_data = pd.DataFrame(columns=['Timestamp', 'Value'])
        st.rerun()

# Plotting section
st.subheader("Value History Plot")
if not st.session_state.history_data.empty:
    fig = px.line(
        st.session_state.history_data,
        x='Timestamp',
        y='Value',
        title='V1 Value Over Time',
        markers=True
    )
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Value',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for plotting")

# Auto-refresh logic
if st.session_state.auto_refresh:
    time.sleep(5)
    st.rerun()

# Debug information
with st.expander("Debug Information"):
    st.write("Latest 5 data points:")
    st.dataframe(st.session_state.history_data.tail(5))
    st.write(f"Auto-refresh state: {st.session_state.auto_refresh}")
    st.write(f"Last update: {st.session_state.last_update}")
