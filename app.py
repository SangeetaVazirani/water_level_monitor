import streamlit as st
import requests

st.set_page_config(
    page_title="Water Level Monitor",
    page_icon="💧",
    layout="wide"
)

# -----------------------------
# ThingSpeak settings
# -----------------------------
CHANNEL_ID = "3492220"

# Paste your ThingSpeak READ API KEY here
READ_API_KEY = "G4GHE1YDS9W41SYP"

# -----------------------------
# Get latest data
# -----------------------------
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json"

params = {
    "api_key": READ_API_KEY
}

try:
    response = requests.get(url, params=params, timeout=5)

    if response.status_code == 200:
        data = response.json()

        level = int(float(data["field1"]))
        led1 = int(float(data["field2"]))
        led2 = int(float(data["field3"]))
        buzzer = int(float(data["field4"]))

        # -----------------------------
        # Dashboard
        # -----------------------------
        st.title("💧 Water Level Monitoring System")
        st.write("ESP32 → ThingSpeak → Streamlit")

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Water Level", f"{level}%")

        with col2:
            st.metric("LED 1", "ON" if led1 == 1 else "OFF")

        with col3:
            st.metric("LED 2", "ON" if led2 == 1 else "OFF")

        with col4:
            st.metric("Buzzer", "ON" if buzzer == 1 else "OFF")

        st.divider()

        if level == 50:
            st.success("🟢 Water Level: 50% — Normal Level")
        elif level == 100:
            st.warning("🟠 Water Level: 100% — HIGH LEVEL / ALARM")
        else:
            st.info(f"Water Level: {level}%")

        st.caption(f"Last update received from ThingSpeak: {data.get('created_at', 'Unknown')}")

    else:
        st.error(f"ThingSpeak error: HTTP {response.status_code}")

except Exception as e:
    st.error(f"Unable to connect to ThingSpeak: {e}")