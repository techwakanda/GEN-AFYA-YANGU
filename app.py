import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Language toggle in sidebar
st.sidebar.title("Gen Afya Yangu")
language = st.sidebar.selectbox("Language / Lugha", ["English", "Swahili"])
st.session_state.language = language

# Bilingual text dictionary
text = {
    'English': {
        'title': "Gen Afya Yangu - My Health Dashboard",
        'header': "My Current Health",
        'metrics': "Current Health Metrics",
        'table': "Recent Data",
        'trends': "Health Trends",
        'alerts': "Alerts",
        'heart_rate': "Heart Rate",
        'blood_oxygen': "Blood Oxygen",
        'status': "Status",
        'recommendation': "Recommendation",
        'time': "Time",
        'value': "Value",
        'refresh': "Refresh Data"
    },
    'Swahili': {
        'title': "Gen Afya Yangu - Dashibodi ya Afya Yangu",
        'header': "Afya Yangu ya Sasa",
        'metrics': "Vipimo vya Afya vya Sasa",
        'table': "Data za Hivi Karibuni",
        'trends': "Mwelekeo wa Afya",
        'alerts': "Tahadhari",
        'heart_rate': "Mapigo ya Moyo",
        'blood_oxygen': "Oksijeni ya Damu",
        'status': "Hali",
        'recommendation': "Pendekezo",
        'time': "Wakati",
        'value': "Thamani",
        'refresh': "Sasisha Data"
    }
}

# Simulate health data
@st.cache_data
def generate_health_data():
    data = {
        'timestamp': pd.date_range(start=pd.Timestamp.now(), periods=50, freq='T'),
        'heart_rate': np.random.randint(60, 120, 50),  # Simulate heart rate (bpm)
        'blood_oxygen': np.random.randint(85, 100, 50),  # Simulate blood oxygen (%)
    }
    df = pd.DataFrame(data)
    return df

# Preprocess data
def preprocess_data(df):
    df['heart_rate'] = df['heart_rate'].fillna(df['heart_rate'].mean())
    df['blood_oxygen'] = df['blood_oxygen'].clip(lower=85, upper=100)
    return df

# Detect anomalies using Isolation Forest
def detect_anomalies(df):
    model = IsolationForest(contamination=0.05, random_state=42)
    features = ['heart_rate', 'blood_oxygen']
    df['anomaly'] = model.fit_predict(df[features])
    df['anomaly'] = df['anomaly'].apply(lambda x: 'Anomaly / Shida' if x == -1 else 'Normal / Kawaida')
    return df

# Generate recommendations
def generate_recommendations(df):
    df['recommendation'] = ''
    df.loc[(df['anomaly'] == 'Anomaly / Shida') & (df['heart_rate'] > 100), 'recommendation'] = 'Rest for 10 minutes / Pumzika kwa dakika 10.'
    df.loc[(df['anomaly'] == 'Anomaly / Shida') & (df['blood_oxygen'] < 90), 'recommendation'] = 'Consult a doctor / Onana na daktari.'
    return df

# Main app logic
def main():
    # Set page config for better appearance
    st.set_page_config(page_title="Gen Afya Yangu", page_icon="🩺", layout="wide")

    # Apply custom CSS for styling
    st.markdown("""
        <style>
        .main { background-color: #f5f5f5; }
        .stMetric { background-color: #ffffff; border-radius: 10px; padding: 10px; }
        .stAlert { border-left: 5px solid #ff4d4d; }
        </style>
    """, unsafe_allow_html=True)

    # Display title and header
    st.title(text[st.session_state.language]['title'])
    st.header(text[st.session_state.language]['header'], divider="blue")

    # Refresh button to simulate new data
    if st.button(text[st.session_state.language]['refresh']):
        st.cache_data.clear()  # Clear cache to generate new data
        st.rerun()

    # Generate and process data
    df = generate_health_data()
    df = preprocess_data(df)
    df = detect_anomalies(df)
    df = generate_recommendations(df)

    # Display metrics in columns
    st.subheader(text[st.session_state.language]['metrics'])
    col1, col2 = st.columns(2)
    latest = df.iloc[-1]
    with col1:
        st.metric(text[st.session_state.language]['heart_rate'], f"{latest['heart_rate']} bpm")
    with col2:
        st.metric(text[st.session_state.language]['blood_oxygen'], f"{latest['blood_oxygen']}%")

    # Display data table
    st.subheader(text[st.session_state.language]['table'])
    st.dataframe(df[['timestamp', 'heart_rate', 'blood_oxygen', 'anomaly', 'recommendation']].tail(10),
                 use_container_width=True)

    # Plot health trends
    st.subheader(text[st.session_state.language]['trends'])
    fig = px.line(df, x='timestamp', y=['heart_rate', 'blood_oxygen'],
                  labels={'value': text[st.session_state.language]['value'], 
                          'timestamp': text[st.session_state.language]['time']},
                  title=f"{text[st.session_state.language]['trends']}")
    fig.update_layout(showlegend=True, plot_bgcolor='#ffffff')
    st.plotly_chart(fig, use_container_width=True)

    # Display anomalies
    anomalies = df[df['anomaly'] == 'Anomaly / Shida']
    if not anomalies.empty:
        st.subheader(text[st.session_state.language]['alerts'])
        for _, row in anomalies.iterrows():
            st.warning(f"{row['timestamp']}: {row['anomaly']} - {row['recommendation']}")

if __name__ == "__main__":
    main()