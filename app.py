import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Water Level Monitor",
    page_icon="💧",
    layout="wide"
)

# -----------------------------
# ThingSpeak settings
# -----------------------------
CHANNEL_ID = "3492220"

# ThingSpeak READ API KEY
READ_API_KEY = "G4GHE1YDS9W41SYP"

# -----------------------------
# Dashboard title
# -----------------------------
st.title("💧 Water Level Monitoring System")
st.write("ESP32 → ThingSpeak → Streamlit")

st.divider()


# -----------------------------
# Automatically refresh dashboard
# -----------------------------
@st.fragment(run_every=3)
def water_level_dashboard():

    # -----------------------------
    # Get latest ThingSpeak data
    # -----------------------------
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json"

    params = {
        "api_key": READ_API_KEY
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            # Check that data exists
            if data.get("field1") is None:
                st.error("No water level data received from ThingSpeak.")
                return

            # -----------------------------
            # Read fields
            # -----------------------------
            level = int(float(data["field1"]))
            led1 = int(float(data["field2"]))
            led2 = int(float(data["field3"]))
            buzzer = int(float(data["field4"]))

            # -----------------------------
            # Display values
            # -----------------------------
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "💧 Water Level",
                    f"{level}%"
                )

            with col2:
                st.metric(
                    "🔴 LED 1",
                    "ON" if led1 == 1 else "OFF"
                )

            with col3:
                st.metric(
                    "🔴 LED 2",
                    "ON" if led2 == 1 else "OFF"
                )

            with col4:
                st.metric(
                    "🔊 Buzzer",
                    "ON" if buzzer == 1 else "OFF"
                )

            st.divider()

            # -----------------------------
            # Water level message
            # -----------------------------
            if level == 0:

                st.info(
                    "⚪ Water Level: 0% — System Idle"
                )

            elif level == 50:

                st.success(
                    "🟢 Water Level: 50% — Normal Level"
                )

            elif level == 100:

                st.warning(
                    "🟠 Water Level: 100% — HIGH LEVEL / ALARM"
                )

            else:

                st.info(
                    f"Water Level: {level}%"
                )

            # -----------------------------
            # ThingSpeak update time
            # -----------------------------
            st.caption(
                f"Last ThingSpeak update: "
                f"{data.get('created_at', 'Unknown')}"
            )

            # -----------------------------
            # Dashboard refresh information
            # -----------------------------
            st.caption(
                "🔄 Dashboard automatically checks ThingSpeak every 3 seconds."
            )

        else:

            st.error(
                f"ThingSpeak error: HTTP {response.status_code}"
            )

    except Exception as e:

        st.error(
            f"Unable to connect to ThingSpeak: {e}"
        )


# Run dashboard
water_level_dashboard()
