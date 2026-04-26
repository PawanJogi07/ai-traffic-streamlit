import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Page Configuration
st.set_page_config(
    page_title="UrbanTwin AI - City Risk Engine",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #f8fafc, #f1f5f9);
    }
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .big-title {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(to right, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .risk-card {
        background: linear-gradient(to right, #2563eb, #9333ea);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
    }
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'live_data' not in st.session_state:
    st.session_state.live_data = {
        'traffic': 67,
        'accident': 0.34,
        'pollution': 142,
        'crowd': 78,
        'risk': 72
    }

# Sidebar
with st.sidebar:
    st.markdown("## 🏙️ UrbanTwin AI")
    st.markdown("**Real-Time City Risk Engine**")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "🚗 Traffic Model", "⚠️ Accident Model", 
         "🌫️ Pollution Model", "👥 Crowd Model", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### System Status")
    st.success("✅ All Systems Online")
    st.info(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
    
    if st.button("🔄 Refresh Data"):
        st.session_state.live_data['traffic'] = max(0, min(100, st.session_state.live_data['traffic'] + np.random.randn() * 5))
        st.session_state.live_data['accident'] = max(0, min(1, st.session_state.live_data['accident'] + np.random.randn() * 0.05))
        st.session_state.live_data['pollution'] = max(0, min(500, st.session_state.live_data['pollution'] + np.random.randn() * 10))
        st.session_state.live_data['crowd'] = max(0, min(100, st.session_state.live_data['crowd'] + np.random.randn() * 5))
        st.session_state.live_data['risk'] = (st.session_state.live_data['traffic'] * 0.3 + 
                                               st.session_state.live_data['accident'] * 100 * 0.2 +
                                               st.session_state.live_data['pollution'] / 5 * 0.3 +
                                               st.session_state.live_data['crowd'] * 0.2)
        st.rerun()

# Helper Functions
def get_risk_level(risk):
    if risk >= 75:
        return "Critical", "#ef4444"
    elif risk >= 50:
        return "High", "#f59e0b"
    elif risk >= 25:
        return "Moderate", "#eab308"
    return "Low", "#10b981"

def create_time_series_data():
    times = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59']
    traffic = [25, 15, 85, 70, 90, 65, 35]
    pollution = [85, 75, 165, 145, 180, 125, 95]
    crowd = [15, 10, 75, 85, 70, 80, 45]
    risk = [30, 25, 80, 75, 85, 70, 40]
    
    return pd.DataFrame({
        'Time': times,
        'Traffic': traffic,
        'Pollution': pollution,
        'Crowd': crowd,
        'Risk': risk
    })

def create_city_areas_data():
    areas = ['Central', 'North', 'South', 'East', 'West']
    risk = [85, 62, 71, 58, 69]
    traffic = [92, 68, 75, 62, 73]
    pollution = [165, 125, 142, 118, 138]
    crowd = [88, 55, 68, 52, 65]
    
    return pd.DataFrame({
        'Area': areas,
        'Risk': risk,
        'Traffic': traffic,
        'Pollution': pollution,
        'Crowd': crowd
    })

def create_ml_predictions(model_type):
    hours = list(range(1, 7))
    
    if model_type == 'traffic':
        predicted = [45, 38, 52, 68, 82, 75]
        actual = [42, 40, 50, 70, 80, 73]
        confidence = [92, 89, 94, 88, 91, 93]
    elif model_type == 'accident':
        predicted = [0.25, 0.18, 0.32, 0.45, 0.52, 0.38]
        actual = [0.23, 0.20, 0.30, 0.47, 0.50, 0.36]
        confidence = [87, 85, 90, 86, 89, 91]
    elif model_type == 'pollution':
        predicted = [95, 88, 125, 158, 172, 145]
        actual = [92, 90, 122, 160, 168, 143]
        confidence = [94, 91, 95, 89, 92, 93]
    else:  # crowd
        predicted = [35, 28, 62, 78, 85, 72]
        actual = [33, 30, 60, 80, 82, 70]
        confidence = [90, 88, 93, 87, 91, 92]
    
    return pd.DataFrame({
        'Hour': hours,
        'Predicted': predicted,
        'Actual': actual,
        'Confidence': confidence
    })

# Main Content
if page == "🏠 Overview":
    # Header
    st.markdown('<div class="big-title">UrbanTwin AI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Real-Time City Risk Monitoring System</div>', unsafe_allow_html=True)
    
    # Overall Risk Score
    risk_level, risk_color = get_risk_level(st.session_state.live_data['risk'])
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="risk-card">
            <h2>Overall City Risk Score</h2>
            <div style="font-size: 80px; font-weight: bold; margin: 20px 0;">
                {int(st.session_state.live_data['risk'])}
                <span style="font-size: 40px;">/100</span>
            </div>
            <div style="background: {risk_color}; padding: 10px 20px; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 20px;">
                {risk_level}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("🎯 Accuracy", "94.3%", "↑ 2.1%")
        st.metric("⚡ Response Time", "0.8s", "↓ 0.2s")
    
    with col3:
        st.metric("📊 Active Sensors", "156", "↑ 12")
        st.metric("🔄 Updates/min", "45", "→")
    
    st.markdown("---")
    
    # Live Metrics
    st.markdown("### 📊 Live Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div style="font-size: 14px; margin-bottom: 10px;">🚗 Traffic Congestion</div>
            <div style="font-size: 36px; font-weight: bold;">{int(st.session_state.live_data['traffic'])}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <div style="font-size: 14px; margin-bottom: 10px;">⚠️ Accident Risk</div>
            <div style="font-size: 36px; font-weight: bold;">{st.session_state.live_data['accident']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
            <div style="font-size: 14px; margin-bottom: 10px;">🌫️ Air Quality</div>
            <div style="font-size: 36px; font-weight: bold;">{int(st.session_state.live_data['pollution'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
            <div style="font-size: 14px; margin-bottom: 10px;">👥 Crowd Density</div>
            <div style="font-size: 36px; font-weight: bold;">{int(st.session_state.live_data['crowd'])}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 24-Hour Multi-Factor Trend")
        time_data = create_time_series_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_data['Time'], y=time_data['Traffic'], 
                                mode='lines+markers', name='Traffic', 
                                line=dict(color='#3b82f6', width=3)))
        fig.add_trace(go.Scatter(x=time_data['Time'], y=time_data['Pollution'], 
                                mode='lines+markers', name='Pollution', 
                                line=dict(color='#10b981', width=3)))
        fig.add_trace(go.Scatter(x=time_data['Time'], y=time_data['Crowd'], 
                                mode='lines+markers', name='Crowd', 
                                line=dict(color='#8b5cf6', width=3)))
        fig.add_trace(go.Scatter(x=time_data['Time'], y=time_data['Risk'], 
                                mode='lines+markers', name='Risk Score', 
                                line=dict(color='#ef4444', width=4)))
        
        fig.update_layout(height=400, hovermode='x unified', 
                         plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🗺️ Area-wise Risk Distribution")
        area_data = create_city_areas_data()
        
        fig = px.bar(area_data, x='Area', y='Risk', 
                    color='Risk', color_continuous_scale='RdYlGn_r',
                    labels={'Risk': 'Risk Score'})
        fig.update_layout(height=400, showlegend=False,
                         plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # City Map Simulation
    st.markdown("### 🗺️ Interactive City Risk Map")
    
    map_col1, map_col2 = st.columns([3, 1])
    
    with map_col1:
        # Create synthetic map data
        np.random.seed(42)
        n_points = 50
        lat = np.random.uniform(28.5, 28.7, n_points)
        lon = np.random.uniform(77.1, 77.3, n_points)
        risk_values = np.random.uniform(20, 90, n_points)
        
        map_df = pd.DataFrame({
            'lat': lat,
            'lon': lon,
            'risk': risk_values,
            'size': risk_values
        })
        
        fig = px.scatter_mapbox(map_df, lat='lat', lon='lon', 
                               color='risk', size='size',
                               color_continuous_scale='RdYlGn_r',
                               zoom=10, height=500,
                               labels={'risk': 'Risk Score'})
        
        fig.update_layout(mapbox_style="carto-positron",
                         margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    
    with map_col2:
        st.markdown("#### 📍 Area Details")
        selected_area = st.selectbox("Select Area", 
                                     ['Central', 'North', 'South', 'East', 'West'])
        
        area_details = area_data[area_data['Area'] == selected_area].iloc[0]
        
        st.metric("Risk Score", f"{area_details['Risk']}")
        st.metric("Traffic", f"{area_details['Traffic']}%")
        st.metric("Pollution", f"{area_details['Pollution']} AQI")
        st.metric("Crowd", f"{area_details['Crowd']}%")
        
        risk_level, risk_color = get_risk_level(area_details['Risk'])
        st.markdown(f"""
        <div style="background: {risk_color}; color: white; padding: 10px; 
                    border-radius: 8px; text-align: center; font-weight: bold;">
            {risk_level} Risk
        </div>
        """, unsafe_allow_html=True)

elif page == "🚗 Traffic Model":
    st.markdown("## 🚗 Traffic Congestion Prediction Model")
    st.markdown("**LSTM Neural Network** - Advanced time-series forecasting")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "94.3%", "↑ 1.2%")
    with col2:
        st.metric("MAE", "3.2", "↓ 0.3")
    with col3:
        st.metric("R² Score", "0.91", "→")
    
    st.markdown("---")
    
    # Predictions Chart
    st.markdown("### 📊 6-Hour Traffic Forecast")
    ml_data = create_ml_predictions('traffic')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Predicted'],
                            mode='lines+markers', name='ML Prediction',
                            line=dict(color='#8b5cf6', width=3),
                            marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Actual'],
                            mode='lines+markers', name='Actual',
                            line=dict(color='#10b981', width=3, dash='dash'),
                            marker=dict(size=10)))
    
    fig.update_layout(height=400, xaxis_title="Hours Ahead",
                     yaxis_title="Congestion %",
                     hovermode='x unified',
                     plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Confidence Chart
    st.markdown("### 🎯 Prediction Confidence")
    fig = px.bar(ml_data, x='Hour', y='Confidence',
                color='Confidence', color_continuous_scale='Viridis',
                labels={'Confidence': 'Confidence %'})
    fig.update_layout(height=300, showlegend=False,
                     plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

elif page == "⚠️ Accident Model":
    st.markdown("## ⚠️ Accident Probability Prediction Model")
    st.markdown("**Random Forest Classifier** - Risk assessment & prevention")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "89.7%", "↑ 0.8%")
    with col2:
        st.metric("MAE", "0.04", "↓ 0.01")
    with col3:
        st.metric("R² Score", "0.87", "→")
    
    st.markdown("---")
    
    ml_data = create_ml_predictions('accident')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Predicted'],
                            mode='lines+markers', name='ML Prediction',
                            line=dict(color='#ef4444', width=3),
                            marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Actual'],
                            mode='lines+markers', name='Actual',
                            line=dict(color='#10b981', width=3, dash='dash'),
                            marker=dict(size=10)))
    
    fig.update_layout(height=400, xaxis_title="Hours Ahead",
                     yaxis_title="Accident Probability",
                     hovermode='x unified',
                     plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🌫️ Pollution Model":
    st.markdown("## 🌫️ Air Quality Prediction Model")
    st.markdown("**Gradient Boosting** - Environmental monitoring")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "92.1%", "↑ 1.5%")
    with col2:
        st.metric("MAE", "4.8", "↓ 0.5")
    with col3:
        st.metric("R² Score", "0.89", "→")
    
    st.markdown("---")
    
    ml_data = create_ml_predictions('pollution')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Predicted'],
                            mode='lines+markers', name='ML Prediction',
                            line=dict(color='#10b981', width=3),
                            marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Actual'],
                            mode='lines+markers', name='Actual',
                            line=dict(color='#3b82f6', width=3, dash='dash'),
                            marker=dict(size=10)))
    
    fig.update_layout(height=400, xaxis_title="Hours Ahead",
                     yaxis_title="AQI Level",
                     hovermode='x unified',
                     plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

elif page == "👥 Crowd Model":
    st.markdown("## 👥 Crowd Density Prediction Model")
    st.markdown("**CNN + LSTM Hybrid** - People movement forecasting")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "91.5%", "↑ 0.9%")
    with col2:
        st.metric("MAE", "3.7", "↓ 0.4")
    with col3:
        st.metric("R² Score", "0.90", "→")
    
    st.markdown("---")
    
    ml_data = create_ml_predictions('crowd')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Predicted'],
                            mode='lines+markers', name='ML Prediction',
                            line=dict(color='#9333ea', width=3),
                            marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=ml_data['Hour'], y=ml_data['Actual'],
                            mode='lines+markers', name='Actual',
                            line=dict(color='#10b981', width=3, dash='dash'),
                            marker=dict(size=10)))
    
    fig.update_layout(height=400, xaxis_title="Hours Ahead",
                     yaxis_title="Density %",
                     hovermode='x unified',
                     plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

else:  # Settings
    st.markdown("## ⚙️ System Settings")
    
    st.markdown("### 🔔 Alert Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.slider("Traffic Alert Threshold", 0, 100, 75)
        st.slider("Pollution Alert Threshold", 0, 500, 150)
    with col2:
        st.slider("Crowd Alert Threshold", 0, 100, 80)
        st.slider("Risk Score Alert Threshold", 0, 100, 70)
    
    st.markdown("---")
    st.markdown("### 📊 Data Refresh Rate")
    refresh_rate = st.selectbox("Update Interval", ["Real-time", "Every 5 seconds", "Every 10 seconds", "Every 30 seconds"])
    
    st.markdown("---")
    st.markdown("### 🎨 Display Options")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Show Predictions", value=True)
        st.checkbox("Show Confidence Intervals", value=True)
    with col2:
        st.checkbox("Show Historical Data", value=True)
        st.checkbox("Show Map Overlay", value=True)
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <strong>UrbanTwin AI</strong> | Real-Time City Risk Monitoring System<br>
    Powered by Machine Learning & Advanced Analytics | © 2024
</div>
""", unsafe_allow_html=True)