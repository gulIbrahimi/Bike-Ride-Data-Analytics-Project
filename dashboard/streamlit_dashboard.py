import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration with custom styling
st.set_page_config(
    page_title="London Bike Analytics | Data Portfolio",
    page_icon="🚴‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Custom CSS for premium look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Advanced Header with Gradient */
    .portfolio-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .portfolio-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'%3E%3Cpath d='m0 40l40-40h-40v40zm0 0h40v-40l-40 40z'/%3E%3C/g%3E%3C/svg%3E");
    }
    
    .portfolio-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .portfolio-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: 1rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Advanced Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 20px 40px rgba(31, 38, 135, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-icon {
        font-size: 2rem;
        opacity: 0.7;
        margin-bottom: 0.5rem;
    }
    
    /* Advanced Filter Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Chart Container Styling */
    .chart-container {
        background: rgba(255, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        .chart-container {
        padding: 0;
        margin: 0.25rem 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.15);
        transform: translateY(-2px);
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Advanced Insight Cards */
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .insight-card {
        background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .insight-card.peak-hours {
        border-left-color: #3b82f6;
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    .insight-card.weather-impact {
        border-left-color: #10b981;
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .insight-card.temperature {
        border-left-color: #f59e0b;
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
    }
    
    .insight-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .insight-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-text {
        color: #475569;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Filter Section Styling */
    .filter-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .filter-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Data Info Panel */
    .data-info-panel {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .data-info-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .data-info-item {
        margin: 0.5rem 0;
        opacity: 0.9;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Correlation Matrix Styling */
    .correlation-section {
        background: linear-gradient(145deg, #fefefe 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid rgba(226, 232, 240, 0.6);
    }
    
    /* Download Section */
    .download-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(14, 165, 233, 0.2);
        text-align: center;
    }
    
    /* Portfolio Footer */
    .portfolio-footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .portfolio-header h1 {
            font-size: 2.5rem;
        }
        
        .metric-container {
            grid-template-columns: 1fr;
        }
        
        .insights-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the processed bike sharing data from Excel file"""
    import os
    
    # List of possible file locations to try
    possible_paths = [
        'data/processed/london_bikes_final.xlsx',     # From root folder
        '../data/processed/london_bikes_final.xlsx',  # From dashboard folder
        'london_bikes_final.xlsx',                    # Same directory
        './london_bikes_final.xlsx',                  # Same directory explicit
        '../london_bikes_final.xlsx',                 # One level up
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_excel(path, sheet_name='bike_data')
                break
        except Exception as e:
            continue
    else:
        st.error("❌ Could not find the data file in any expected location.")
        st.stop()
    
    # Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Extract additional time features for analysis
    df['hour'] = df['time'].dt.hour
    df['day_of_week'] = df['time'].dt.day_name()
    df['month'] = df['time'].dt.month
    df['date'] = df['time'].dt.date
    
    return df

def create_advanced_hourly_chart(df):
    """Create advanced hourly usage pattern chart"""
    hourly_avg = df.groupby('hour')['count'].mean().reset_index()
    hourly_std = df.groupby('hour')['count'].std().reset_index()
    
    fig = go.Figure()
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=hourly_avg['hour'],
        y=hourly_avg['count'] + hourly_std['count'],
        fill=None,
        mode='lines',
        line_color='rgba(102, 126, 234, 0)',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=hourly_avg['hour'],
        y=hourly_avg['count'] - hourly_std['count'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(102, 126, 234, 0)',
        name='Confidence Interval',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    # Main line
    fig.add_trace(go.Scatter(
        x=hourly_avg['hour'],
        y=hourly_avg['count'],
        mode='lines+markers',
        name='Average Usage',
        line=dict(color='#667eea', width=4),
        marker=dict(size=8, color='#667eea', symbol='circle')
    ))
    
    fig.update_layout(
        title=dict(text="Hourly Usage Pattern with Confidence Intervals", font=dict(size=20)),
        xaxis_title="Hour of Day",
        yaxis_title="Average Bike Count",
        template='plotly_white',
        height=400,
        hovermode='x unified',
        font=dict(family='Inter')
    )
    
    return fig

def create_advanced_weather_chart(df):
    """Create advanced weather impact chart with animations"""
    weather_stats = df.groupby('weather').agg({
        'count': ['mean', 'std', 'count']
    }).round(1)
    weather_stats.columns = ['avg_count', 'std_count', 'total_records']
    weather_stats = weather_stats.reset_index().sort_values('avg_count', ascending=True)
    
    # Create color scale based on usage
    colors = px.colors.sequential.Viridis_r
    color_scale = [colors[i] for i in range(0, len(colors), len(colors)//len(weather_stats))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=weather_stats['weather'],
        x=weather_stats['avg_count'],
        orientation='h',
        marker=dict(
            color=weather_stats['avg_count'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Avg Usage")
        ),
        text=weather_stats['avg_count'],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Average Usage: %{x}<br>Records: %{customdata}<extra></extra>',
        customdata=weather_stats['total_records']
    ))
    
    fig.update_layout(
        title=dict(text="Weather Impact Analysis", font=dict(size=20, family='Inter')),
        xaxis_title="Average Bike Count",
        yaxis_title="Weather Condition",
        template='plotly_white',
        height=400,
        font=dict(family='Inter')
    )
    
    return fig

def create_advanced_seasonal_chart(df):
    """Create advanced seasonal distribution with 3D effect"""
    seasonal_stats = df.groupby('season').agg({
        'count': ['sum', 'mean', 'count']
    }).round(1)
    seasonal_stats.columns = ['total_rides', 'avg_rides', 'records']
    seasonal_stats = seasonal_stats.reset_index()
    
    colors = {'spring': '#90EE90', 'summer': '#FFD700', 'fall': '#FFA500', 'winter': '#87CEEB'}
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=seasonal_stats['season'],
        values=seasonal_stats['total_rides'],
        hole=0.4,
        marker=dict(
            colors=[colors[season] for season in seasonal_stats['season']],
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, family='Inter', color='white'),
        hovertemplate='<b>%{label}</b><br>Total Rides: %{value:,}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text="Seasonal Distribution Analysis", font=dict(size=20, family='Inter')),
        template='plotly_white',
        height=400,
        font=dict(family='Inter'),
        annotations=[dict(text='Total<br>Usage', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    return fig

def create_advanced_temperature_scatter(df):
    """Create advanced temperature scatter with regression line"""
    sample_df = df.sample(min(2000, len(df))) if len(df) > 2000 else df
    
    fig = px.scatter(
        sample_df, 
        x='temp_real_C', 
        y='count', 
        color='weather',
        size='humidity_percent',
        hover_data=['wind_speed_kph', 'season'],
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Add regression line
    z = np.polyfit(sample_df['temp_real_C'], sample_df['count'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=sample_df['temp_real_C'].sort_values(),
        y=p(sample_df['temp_real_C'].sort_values()),
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=dict(text="Temperature vs Usage Correlation Analysis", font=dict(size=20, family='Inter')),
        xaxis_title="Temperature (°C)",
        yaxis_title="Bike Count",
        height=400,
        font=dict(family='Inter')
    )
    
    return fig

def create_advanced_daily_trend(df):
    """Create advanced daily trend with moving average"""
    daily_counts = df.groupby('date')['count'].sum().reset_index()
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])
    daily_counts = daily_counts.sort_values('date')
    
    # Calculate moving average
    daily_counts['ma_7'] = daily_counts['count'].rolling(window=7).mean()
    daily_counts['ma_30'] = daily_counts['count'].rolling(window=30).mean()
    
    fig = go.Figure()
    
    # Raw data
    fig.add_trace(go.Scatter(
        x=daily_counts['date'],
        y=daily_counts['count'],
        mode='lines',
        name='Daily Usage',
        line=dict(color='lightblue', width=1),
        opacity=0.6
    ))
    
    # 7-day moving average
    fig.add_trace(go.Scatter(
        x=daily_counts['date'],
        y=daily_counts['ma_7'],
        mode='lines',
        name='7-Day Average',
        line=dict(color='#667eea', width=3)
    ))
    
    # 30-day moving average
    fig.add_trace(go.Scatter(
        x=daily_counts['date'],
        y=daily_counts['ma_30'],
        mode='lines',
        name='30-Day Average',
        line=dict(color='#764ba2', width=3)
    ))
    
    fig.update_layout(
        title=dict(text="Daily Usage Trend with Moving Averages", font=dict(size=20, family='Inter')),
        xaxis_title="Date",
        yaxis_title="Total Daily Rides",
        template='plotly_white',
        height=400,
        font=dict(family='Inter'),
        hovermode='x unified'
    )
    
    return fig

def create_advanced_weekday_chart(df):
    """Create advanced weekday pattern with comparison"""
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_stats = df.groupby('day_of_week').agg({
        'count': ['mean', 'std'],
        'is_weekend': 'first'
    }).round(1)
    weekday_stats.columns = ['avg_count', 'std_count', 'is_weekend']
    weekday_stats = weekday_stats.reindex(day_order).reset_index()
    
    # Color by weekend vs weekday
    colors = ['#667eea' if not weekend else '#764ba2' for weekend in weekday_stats['is_weekend']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekday_stats['day_of_week'],
        y=weekday_stats['avg_count'],
        error_y=dict(type='data', array=weekday_stats['std_count'], visible=True),
        marker=dict(color=colors),
        text=weekday_stats['avg_count'].round(0),
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Average Usage: %{y}<br>Std Dev: %{error_y.array}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text="Weekly Usage Pattern (Weekdays vs Weekends)", font=dict(size=20)),
        xaxis_title="Day of Week",
        yaxis_title="Average Bike Count",
        template='plotly_white',
        height=400,
        font=dict(family='Inter')
    )
    
    return fig

def main():
    # Advanced Portfolio Header
    st.markdown("""
    <div class="portfolio-header">
        <h1>🚴‍♂️ London Bike Sharing Analytics</h1>
        <div class="portfolio-subtitle">
            Advanced Data Analytics Dashboard | Built with Python & Streamlit<br>
            <em>Interactive exploration of London's bike sharing patterns and trends</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data with loading spinner
    with st.spinner("🔄 Loading and processing data..."):
        df = load_data()
    
    # Advanced Sidebar with better styling
    with st.sidebar:
        st.markdown("""
        <div class="filter-title">
            🎛️ Interactive Filters
        </div>
        """, unsafe_allow_html=True)
        
        # Season filter with icons
        seasons = ['All'] + sorted(df['season'].unique().tolist())
        selected_season = st.selectbox("🌸 Season:", seasons, help="Filter data by seasonal patterns")
        
        # Weather filter with icons
        weather_conditions = ['All'] + sorted(df['weather'].unique().tolist())
        selected_weather = st.selectbox("🌤️ Weather Condition:", weather_conditions, help="Analyze weather impact on usage")
        
        # Date range filter
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        date_range = st.date_input(
            "📅 Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Select custom date range for analysis"
        )
        
        # Temperature filter
        temp_range = st.slider(
            "🌡️ Temperature Range (°C):",
            float(df['temp_real_C'].min()),
            float(df['temp_real_C'].max()),
            (float(df['temp_real_C'].min()), float(df['temp_real_C'].max())),
            help="Filter by temperature range"
        )
        
        # Advanced data info panel
        st.markdown("""
        <div class="data-info-panel">
            <div class="data-info-title">📊 Dataset Information</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['season'] == selected_season]
    
    if selected_weather != 'All':
        filtered_df = filtered_df[filtered_df['weather'] == selected_weather]
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'] >= date_range[0]) & 
            (filtered_df['date'] <= date_range[1])
        ]
    
    filtered_df = filtered_df[
        (filtered_df['temp_real_C'] >= temp_range[0]) & 
        (filtered_df['temp_real_C'] <= temp_range[1])
    ]
    
    # Update sidebar info
    with st.sidebar:
        st.markdown(f"""
        <div class="data-info-item"><strong>Records:</strong> {len(filtered_df):,}</div>
        <div class="data-info-item"><strong>Date Range:</strong> {filtered_df['date'].min()} to {filtered_df['date'].max()}</div>
        <div class="data-info-item"><strong>Weather Types:</strong> {filtered_df['weather'].nunique()}</div>
        <div class="data-info-item"><strong>Temperature Range:</strong> {filtered_df['temp_real_C'].min():.1f}°C to {filtered_df['temp_real_C'].max():.1f}°C</div>
        """, unsafe_allow_html=True)
    
    # Check if filtered data is empty
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
        return
    
    # Advanced Key Metrics with custom styling
    st.markdown("## 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("🚴‍♂️", "Total Rides", f"{filtered_df['count'].sum():,}", "#667eea"),
        ("⏱️", "Avg Rides/Hour", f"{filtered_df['count'].mean():.0f}", "#10b981"),
        ("🎯", "Peak Usage", f"{filtered_df['count'].max():,}", "#f59e0b"),
        ("🌡️", "Avg Temperature", f"{filtered_df['temp_real_C'].mean():.1f}°C", "#ef4444")
    ]
    
    for i, (icon, label, value, color) in enumerate(metrics_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Advanced Charts Section
    st.markdown("## 📊 Advanced Data Visualizations")
    
    # First row - Advanced charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_hourly = create_advanced_hourly_chart(filtered_df)
            st.plotly_chart(fig_hourly, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_weather = create_advanced_weather_chart(filtered_df)
            st.plotly_chart(fig_weather, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_seasonal = create_advanced_seasonal_chart(filtered_df)
            st.plotly_chart(fig_seasonal, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_temp = create_advanced_temperature_scatter(filtered_df)
            st.plotly_chart(fig_temp, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Third row
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_daily = create_advanced_daily_trend(filtered_df)
            st.plotly_chart(fig_daily, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_weekday = create_advanced_weekday_chart(filtered_df)
            st.plotly_chart(fig_weekday, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Insight Cards Section
    st.markdown("## 💡 Key Insights")
    st.markdown('<div class="insights-grid">', unsafe_allow_html=True)

    # Peak Hour Insight
    peak_hour = filtered_df.groupby('hour')['count'].mean().idxmax()
    st.markdown(f"""
    <div class="insight-card peak-hours">
        <div class="insight-title">⏰ Peak Hour Usage</div>
        <div class="insight-text">
            The highest average bike usage occurs at <strong>{peak_hour}:00</strong> hours, indicating peak commute periods in the city.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Weather Insight
    top_weather = filtered_df.groupby('weather')['count'].mean().idxmax()
    st.markdown(f"""
    <div class="insight-card weather-impact">
        <div class="insight-title">🌦️ Weather Influence</div>
        <div class="insight-text">
            Riders prefer <strong>{top_weather}</strong> weather conditions, showing how environment impacts user behavior.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Temperature Insight
    optimal_temp = filtered_df.groupby('temp_real_C')['count'].mean().idxmax()
    st.markdown(f"""
    <div class="insight-card temperature">
        <div class="insight-title">🌡️ Optimal Riding Temperature</div>
        <div class="insight-text">
            The most favorable riding temperature is around <strong>{optimal_temp:.1f}°C</strong>, based on usage trends.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="portfolio-footer">
        🚴‍♂️ Developed with love using Python, Pandas, Plotly & Streamlit<br>
        <small>© 2025 London Bike Analytics Dashboard | Gul Amiz Portfolio Project</small>
    </div>
    """, unsafe_allow_html=True)

# Run the main app
if __name__ == "__main__":
    main()
