# Gen Afya Yangu MVP

## Overview
Gen Afya Yangu is an AI-powered health monitoring system that tracks heart rate and blood oxygen levels, detects anomalies, and provides recommendations. This MVP uses simulated data and is deployed on Streamlit Cloud.

## Access
- URL: [To be updated after deployment, e.g., https://gen-afya-yangu.streamlit.app]
- Features:
  - Real-time health metrics display.
  - Anomaly detection using Isolation Forest.
  - Bilingual (English/Swahili) recommendations.
  - Interactive dashboard with trends and alerts.

## How to Use
1. Visit the app URL.
2. Select language (English or Swahili) in the sidebar.
3. View health metrics, trends, and anomaly alerts.
4. Follow recommendations for flagged anomalies.

## Limitations
- Uses simulated data due to time constraints.
- Limited to heart rate and blood oxygen; no real wearable integration.
- Basic recommendations; no advanced time-series analysis.

## Next Steps
- Integrate with Terra or Human API for real wearable data.
- Add LSTM for time-series anomaly detection.
- Develop a mobile app with Flutter.
- Expand to mental health monitoring using social media data.
- Add a chatbot for conversational queries.

## Setup (for Developers)
```bash
pip install -r requirements.txt
streamlit run app.py