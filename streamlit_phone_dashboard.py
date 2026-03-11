"""
Mobile Phone Recommendation System - Streamlit Dashboard
Professional dashboard showcasing data science skills
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Phone Recommendation System",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    .main {
        padding: 1rem 2rem;
        background-color: #f5f7fa;
    }
    
    .stAlert {
        margin-top: 1rem;
        border-radius: 8px;
    }
    
    h1 {
        color: #1a1a2e;
        font-weight: 700;
        padding-bottom: 1rem;
    }
    
    h2 {
        color: #16213e;
        font-weight: 600;
        padding-top: 1rem;
    }
    
    h3 {
        color: #0f3460;
        font-weight: 600;
    }
    
    .phone-card {
        border: 1px solid #e8eaf6;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .phone-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }
    
    .recommendation-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 6px 16px;
        border-radius: 16px;
        font-weight: 500;
        font-size: 0.9rem;
        margin: 4px;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 24px;
        font-size: 1.4rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(17, 153, 142, 0.3);
    }
    
    .feature-badge {
        background: #f1f3f5;
        padding: 8px 16px;
        border-radius: 16px;
        margin: 4px 8px 4px 0;
        display: inline-block;
        font-size: 0.85rem;
        border: 1px solid #dee2e6;
        color: #495057;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f3460;
    }
    
    .rating-display {
        background: #fff3cd;
        color: #856404;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)


class PhoneAnalytics:
    """Class to handle phone data analytics and recommendations"""
    
    def __init__(self, csv_file='smartprix_phones_data.csv'):
        """Initialize with phone data"""
        import os
        
        # Try to find the CSV file in multiple locations
        possible_paths = [
            csv_file,  # Current directory
            os.path.join(os.path.dirname(__file__), csv_file),  # Same dir as script
            os.path.join(os.path.dirname(__file__), 'advanced-web-scraping-master', csv_file),  # Subfolder
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path is None:
            raise FileNotFoundError(f"Could not find {csv_file}. Please ensure the file exists.")
        
        self.df = pd.read_csv(csv_path)
        self.clean_data()
    
    def clean_data(self):
        """Clean and preprocess the data"""
        # Extract numeric values
        self.df['price_numeric'] = self.df['price'].apply(self.extract_price)
        self.df['camera_mp'] = self.df['camera'].apply(self.extract_camera_mp)
        self.df['ram_gb'] = self.df['ram'].apply(self.extract_ram_gb)
        self.df['battery_mah'] = self.df['battery'].apply(self.extract_battery)
        self.df['display_inches'] = self.df['display'].apply(self.extract_display)
        self.df['rating_numeric'] = pd.to_numeric(self.df['rating'], errors='coerce')
        self.df['processor_score'] = self.df['processor'].apply(self.score_processor)
        
        # Filter valid data
        self.df = self.df[self.df['price_numeric'] > 0].copy()
        
        # Create price categories
        self.df['price_category'] = pd.cut(
            self.df['price_numeric'], 
            bins=[0, 10000, 20000, 30000, 50000, 100000, 200000],
            labels=['Budget (<10K)', 'Mid-Range (10-20K)', 'Premium (20-30K)', 
                   'Flagship (30-50K)', 'Ultra Premium (50K-1L)', 'Luxury (>1L)']
        )
    
    def extract_price(self, price_str):
        if pd.isna(price_str):
            return 0
        match = re.search(r'[\d,]+', str(price_str))
        return int(match.group().replace(',', '')) if match else 0
    
    def extract_camera_mp(self, camera_str):
        if pd.isna(camera_str):
            return 0
        matches = re.findall(r'(\d+\.?\d*)\s*MP', str(camera_str))
        return float(max(matches, key=float)) if matches else 0
    
    def extract_ram_gb(self, ram_str):
        if pd.isna(ram_str):
            return 0
        match = re.search(r'(\d+)\s*GB', str(ram_str))
        return int(match.group(1)) if match else 0
    
    def extract_battery(self, battery_str):
        if pd.isna(battery_str):
            return 0
        match = re.search(r'(\d+)\s*mAh', str(battery_str))
        return int(match.group(1)) if match else 0
    
    def extract_display(self, display_str):
        if pd.isna(display_str):
            return 0
        match = re.search(r'(\d+\.?\d*)\s*(?:inch|")', str(display_str))
        return float(match.group(1)) if match else 0
    
    def score_processor(self, processor_str):
        if pd.isna(processor_str):
            return 0
        
        processor_str = str(processor_str).lower()
        score = 50
        
        if 'snapdragon 8' in processor_str or 'dimensity 9' in processor_str:
            score += 50
        elif 'snapdragon 7' in processor_str or 'dimensity 8' in processor_str:
            score += 40
        elif 'snapdragon 6' in processor_str or 'dimensity 7' in processor_str:
            score += 30
        elif 'snapdragon' in processor_str or 'dimensity' in processor_str:
            score += 20
        elif 'helio' in processor_str:
            score += 15
        
        match = re.search(r'(\d{3,4})', processor_str)
        if match:
            score += int(match.group(1)) / 50
            
        return score
    
    def normalize(self, series):
        """Normalize series to 0-100"""
        if series.max() == series.min():
            return series * 0
        return (series - series.min()) / (series.max() - series.min()) * 100
    
    def get_recommendations(self, budget, criteria='overall', top_n=5):
        """Get phone recommendations based on criteria"""
        filtered = self.df[self.df['price_numeric'] <= budget].copy()
        
        if len(filtered) == 0:
            return None
        
        if criteria == 'camera':
            filtered['score'] = filtered['camera_mp'] * 0.7 + filtered['rating_numeric'].fillna(0) * 10
            sort_col = 'score'
        elif criteria == 'processor':
            filtered['score'] = filtered['processor_score'] * 0.7 + filtered['rating_numeric'].fillna(0) * 10
            sort_col = 'score'
        elif criteria == 'ram':
            filtered['score'] = filtered['ram_gb'] * 10 + filtered['rating_numeric'].fillna(0) * 5
            sort_col = 'score'
        elif criteria == 'battery':
            filtered['score'] = filtered['battery_mah'] / 100 + filtered['rating_numeric'].fillna(0) * 10
            sort_col = 'score'
        elif criteria == 'rating':
            filtered = filtered[filtered['rating_numeric'].notna()]
            sort_col = 'rating_numeric'
        else:  # overall
            filtered['camera_score'] = self.normalize(filtered['camera_mp'])
            filtered['ram_score'] = self.normalize(filtered['ram_gb'])
            filtered['battery_score'] = self.normalize(filtered['battery_mah'])
            filtered['processor_norm'] = self.normalize(filtered['processor_score'])
            filtered['rating_score'] = self.normalize(filtered['rating_numeric'].fillna(0))
            filtered['display_score'] = self.normalize(filtered['display_inches'])
            
            filtered['overall_score'] = (
                filtered['camera_score'] * 0.20 +
                filtered['processor_norm'] * 0.25 +
                filtered['ram_score'] * 0.15 +
                filtered['battery_score'] * 0.15 +
                filtered['rating_score'] * 0.15 +
                filtered['display_score'] * 0.10
            )
            sort_col = 'overall_score'
        
        return filtered.nlargest(top_n, sort_col)


@st.cache_data
def load_data():
    """Load and cache data"""
    try:
        analytics = PhoneAnalytics()
        return analytics
    except FileNotFoundError:
        st.error("❌ Data file not found! Please run smartprix-phones.ipynb first.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def main():
    """Main Streamlit application"""
    
    # Load data
    analytics = load_data()
    df = analytics.df
    
    # Header with professional design
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px; border-radius: 12px; margin-bottom: 32px;
                    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);">
            <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem; font-weight: 700;">
                Mobile Phone Recommendation System
            </h1>
            <p style="color: white; text-align: center; font-size: 1.1rem; margin-top: 12px; opacity: 0.95;">
                AI-Powered Recommendations | Advanced Analytics | 1000+ Phones Database
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with enhanced design
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 24px 12px;">
                <h2 style="margin: 12px 0; color: #1a1a2e; font-size: 1.5rem;">Control Panel</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate to:",
            ["Home - Recommendations", "Data Analytics", "Phone Explorer", "Market Insights"],
            label_visibility="visible"
        )
        
        st.markdown("---")
        
        # Dataset metrics
        st.markdown("### Dataset Overview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Total Phones", 
                f"{len(df):,}",
                delta=None
            )
        with col2:
            st.metric(
                "Avg Price", 
                f"₹{df['price_numeric'].mean()/1000:.0f}K",
                delta=None
            )
        
        st.markdown("---")
        
        # Price range display
        st.markdown("### Price Range")
        min_price = df['price_numeric'].min()
        max_price = df['price_numeric'].max()
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                        padding: 16px; border-radius: 10px; color: white; text-align: center;">
                <div style="font-size: 0.85rem; opacity: 0.9;">Minimum</div>
                <div style="font-size: 1.3rem; font-weight: 700;">₹{min_price:,.0f}</div>
                <div style="margin: 12px 0; font-size: 1.2rem;">↓</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">Maximum</div>
                <div style="font-size: 1.3rem; font-weight: 700;">₹{max_price:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### Quick Statistics")
        avg_camera = df['camera_mp'].mean()
        avg_battery = df['battery_mah'].mean()
        avg_ram = df['ram_gb'].mean()
        
        st.markdown(f"""
            <div style="font-size: 0.9rem; line-height: 2.2; color: #495057;">
                <b>Avg Camera:</b> {avg_camera:.0f} MP<br>
                <b>Avg Battery:</b> {avg_battery:.0f} mAh<br>
                <b>Avg RAM:</b> {avg_ram:.0f} GB
            </div>
        """, unsafe_allow_html=True)
    
    # Page routing
    if "Home" in page:
        show_recommendations_page(analytics, df)
    elif "Data Analytics" in page:
        show_analytics_page(df)
    elif "Phone Explorer" in page:
        show_explorer_page(df)
    else:
        show_insights_page(df)


def show_recommendations_page(analytics, df):
    """Recommendation page"""
    
    # Page header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 32px;">
            <h2 style="color: #1a1a2e; font-size: 2.2rem; margin-bottom: 12px; font-weight: 700;">
                Get Your Perfect Phone Match
            </h2>
            <p style="color: #6c757d; font-size: 1.05rem;">
                Smart AI recommendations tailored to your budget and preferences
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Budget and recommendation settings
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("#### Set Your Budget")
        budget = st.slider(
            "Budget Range (₹)",
            min_value=int(df['price_numeric'].min()),
            max_value=int(df['price_numeric'].max()),
            value=30000,
            step=1000,
            format="₹%d",
            help="Slide to set your maximum budget",
            label_visibility="collapsed"
        )
        
        # Display budget info
        st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 16px; border-radius: 10px; margin-top: 12px;">
                <div style="font-size: 0.85rem; opacity: 0.9;">Your Budget</div>
                <div style="font-size: 1.8rem; font-weight: 700;">₹{budget:,}</div>
                <div style="font-size: 0.8rem; opacity: 0.85;">{len(df[df['price_numeric'] <= budget])} phones available</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Number of Results")
        top_n = st.select_slider(
            "Results count",
            options=[3, 5, 8, 10],
            value=5,
            label_visibility="collapsed"
        )
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: #f8f9fa; 
                        border-radius: 10px; margin-top: 12px; border: 2px solid #dee2e6;">
                <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{top_n}</div>
                <div style="font-size: 0.8rem; color: #6c757d;">recommendations</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Minimum Rating")
        min_rating = st.slider(
            "Min rating",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.5,
            label_visibility="collapsed"
        )
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: #fff3cd; 
                        border-radius: 10px; margin-top: 12px; border: 2px solid #ffc107;">
                <div style="font-size: 2rem; color: #856404; font-weight: 700;">{min_rating}+</div>
                <div style="font-size: 0.8rem; color: #856404;">rating filter</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Criteria selection
    st.markdown("""
        <div style="text-align: center; margin: 24px 0 20px 0;">
            <h3 style="color: #1a1a2e; font-size: 1.6rem; font-weight: 600;">Choose Your Priority</h3>
            <p style="color: #6c757d;">Select what matters most to you in a smartphone</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for criteria buttons
    criteria_col1, criteria_col2, criteria_col3 = st.columns(3)
    
    with criteria_col1:
        if st.button("Best Camera", use_container_width=True, key="cam", type="primary"):
            st.session_state.criteria = 'camera'
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Best Battery", use_container_width=True, key="bat"):
            st.session_state.criteria = 'battery'
    
    with criteria_col2:
        if st.button("Best Processor", use_container_width=True, key="proc"):
            st.session_state.criteria = 'processor'
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Best Rated", use_container_width=True, key="rate"):
            st.session_state.criteria = 'rating'
    
    with criteria_col3:
        if st.button("Best RAM", use_container_width=True, key="ram"):
            st.session_state.criteria = 'ram'
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Overall Best", use_container_width=True, key="overall", type="primary"):
            st.session_state.criteria = 'overall'
    
    st.markdown("---")
    
    # Get recommendations
    if 'criteria' not in st.session_state:
        st.session_state.criteria = 'overall'
    
    criteria = st.session_state.criteria
    recommendations = analytics.get_recommendations(budget, criteria, top_n)
    
    # Apply rating filter
    if recommendations is not None and min_rating > 0:
        # Fix rating before filtering
        recommendations['rating_numeric'] = recommendations['rating_numeric'].apply(
            lambda x: x / 10 if pd.notna(x) and x > 10 else x
        )
        recommendations = recommendations[recommendations['rating_numeric'].fillna(0) >= min_rating]
    
    if recommendations is None or len(recommendations) == 0:
        st.warning("No phones found matching your criteria. Try adjusting your budget or filters!")
        return
    
    # Display criteria banner
    criteria_names = {
        'camera': 'Best Camera Quality',
        'processor': 'Best Processor Performance',
        'ram': 'Best RAM Capacity',
        'battery': 'Best Battery Life',
        'rating': 'Highest User Ratings',
        'overall': 'Overall Best Value'
    }
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 28px;
                    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);">
            <h2 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 600;">
                {criteria_names[criteria]}
            </h2>
            <p style="color: white; margin: 10px 0 0 0; opacity: 0.95; font-size: 1.05rem;">
                Showing top {len(recommendations)} recommendations within ₹{budget:,}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display recommendations
    for idx, (_, phone) in enumerate(recommendations.iterrows(), 1):
        with st.container():
            # Create a styled card
            st.markdown(f"""
                <div style="background: white; 
                            border-radius: 12px; padding: 28px; margin: 20px 0;
                            box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-left: 4px solid #667eea;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### #{idx}. {phone['model']}")
                st.markdown(f"<div class='price-tag'>₹ {phone['price']}</div>", unsafe_allow_html=True)
                st.write("")
                if pd.notna(phone['rating_numeric']):
                    # Fix rating display - divide by 10 if it's > 10
                    rating_value = phone['rating_numeric'] / 10 if phone['rating_numeric'] > 10 else phone['rating_numeric']
                    st.markdown(f"<div class='rating-display'>Rating: {rating_value:.1f}/10</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Specifications:**")
                st.markdown(f"<div class='feature-badge'>Processor: {phone['processor'][:30]}...</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='feature-badge'>RAM: {phone['ram']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='feature-badge'>Battery: {phone['battery']}</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Highlights:**")
                st.metric("Camera", f"{phone['camera_mp']:.1f} MP", delta=None)
                st.metric("Display", f"{phone['display_inches']:.2f}\"", delta=None)
                if 'overall_score' in phone and pd.notna(phone['overall_score']):
                    st.metric("Score", f"{phone['overall_score']:.0f}/100", delta=None)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced comparison charts
    if len(recommendations) > 1:
        st.markdown("---")
        st.markdown("### Advanced Comparison Dashboard")
        
        # Prepare data
        comparison_data = recommendations[['model', 'price_numeric', 'camera_mp', 
                                          'ram_gb', 'battery_mah', 'rating_numeric', 
                                          'processor_score', 'display_inches']].copy()
        comparison_data['model_short'] = comparison_data['model'].str[:25]
        
        # Fix rating display
        comparison_data['rating_numeric'] = comparison_data['rating_numeric'].apply(
            lambda x: x / 10 if pd.notna(x) and x > 10 else x
        )
        
        # Tab layout for different comparisons
        tab1, tab2, tab3, tab4 = st.tabs(["Radar Comparison", "Bar Charts", "Feature Matrix", "Value Analysis"])
        
        with tab1:
            st.markdown("#### Multi-Parameter Radar Chart")
            
            # Create radar chart for top 3 phones
            top_phones = comparison_data.head(3)
            
            # Normalize scores to 0-100 scale
            features = ['camera_mp', 'ram_gb', 'battery_mah', 'processor_score', 'display_inches']
            feature_names = ['Camera', 'RAM', 'Battery', 'Processor', 'Display']
            
            fig = go.Figure()
            
            colors = ['#667eea', '#11998e', '#f093fb', '#fbc531', '#e74c3c']
            
            for idx, (_, phone) in enumerate(top_phones.iterrows()):
                values = []
                for feature in features:
                    val = phone[feature]
                    # Normalize
                    max_val = comparison_data[feature].max()
                    min_val = comparison_data[feature].min()
                    if max_val != min_val:
                        normalized = ((val - min_val) / (max_val - min_val)) * 100
                    else:
                        normalized = 50
                    values.append(normalized)
                
                values.append(values[0])  # Close the radar
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=feature_names + [feature_names[0]],
                    fill='toself',
                    name=phone['model_short'],
                    line=dict(color=colors[idx], width=2),
                    fillcolor=colors[idx],
                    opacity=0.25
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        showticklabels=True,
                        ticks='outside',
                        gridcolor='#e0e0e0'
                    ),
                    bgcolor='rgba(255,255,255,1)'
                ),
                showlegend=True,
                title="Performance Comparison Radar",
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("How to read: Larger area indicates better overall performance. Compare shapes to identify strengths and weaknesses.")
        
        with tab2:
            st.markdown("#### Feature-by-Feature Comparison")
            
            # Create subplots with 2 rows
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Camera Quality (MP)', 'RAM Capacity (GB)', 
                              'Battery Life (mAh)', 'Processor Score'),
                specs=[[{'type': 'bar'}, {'type': 'bar'}],
                       [{'type': 'bar'}, {'type': 'bar'}]]
            )
            
            # Camera
            fig.add_trace(go.Bar(
                x=comparison_data['model_short'],
                y=comparison_data['camera_mp'],
                name='Camera (MP)',
                marker_color='#667eea',
                text=[f"{x:.1f}" for x in comparison_data['camera_mp']],
                textposition='outside',
            ), row=1, col=1)
            
            # RAM
            fig.add_trace(go.Bar(
                x=comparison_data['model_short'],
                y=comparison_data['ram_gb'],
                name='RAM (GB)',
                marker_color='#11998e',
                text=comparison_data['ram_gb'],
                textposition='outside',
            ), row=1, col=2)
            
            # Battery
            fig.add_trace(go.Bar(
                x=comparison_data['model_short'],
                y=comparison_data['battery_mah'],
                name='Battery (mAh)',
                marker_color='#f093fb',
                text=comparison_data['battery_mah'],
                textposition='outside',
            ), row=2, col=1)
            
            # Processor
            fig.add_trace(go.Bar(
                x=comparison_data['model_short'],
                y=comparison_data['processor_score'],
                name='Processor Score',
                marker_color='#fbc531',
                text=[f"{x:.0f}" for x in comparison_data['processor_score']],
                textposition='outside',
            ), row=2, col=2)
            
            fig.update_layout(
                height=700,
                showlegend=False,
                title_text="Detailed Feature Comparison",
                title_font_size=18,
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            
            fig.update_xaxes(tickangle=-45)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("#### Feature Comparison Matrix")
            
            # Create feature matrix
            matrix_data = comparison_data[['model_short', 'camera_mp', 'ram_gb', 
                                          'battery_mah', 'price_numeric', 
                                          'rating_numeric']].copy()
            matrix_data.columns = ['Model', 'Camera (MP)', 'RAM (GB)', 
                                  'Battery (mAh)', 'Price (₹)', 'Rating']
            
            # Format the dataframe
            matrix_display = matrix_data.copy()
            matrix_display['Price (₹)'] = matrix_display['Price (₹)'].apply(lambda x: f'₹{x:,.0f}')
            matrix_display['Camera (MP)'] = matrix_display['Camera (MP)'].apply(lambda x: f'{x:.1f}')
            matrix_display['Battery (mAh)'] = matrix_display['Battery (mAh)'].apply(lambda x: f'{x:.0f}')
            matrix_display['Rating'] = matrix_display['Rating'].apply(lambda x: f'{x:.1f}' if pd.notna(x) else 'N/A')
            
            st.dataframe(
                matrix_display,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # Show best values
            col1, col2, col3 = st.columns(3)
            with col1:
                best_camera_phone = matrix_data.loc[matrix_data['Camera (MP)'].idxmax(), 'Model']
                st.success(f"Best Camera: {best_camera_phone}")
            with col2:
                best_battery_phone = matrix_data.loc[matrix_data['Battery (mAh)'].idxmax(), 'Model']
                st.success(f"Best Battery: {best_battery_phone}")
            with col3:
                cheapest_phone = matrix_data.loc[matrix_data['Price (₹)'].idxmin(), 'Model']
                st.info(f"Best Price: {cheapest_phone}")
        
        with tab4:
            st.markdown("#### Value for Money Analysis")
            
            # Create value score
            comparison_data['value_score'] = (
                (comparison_data['camera_mp'] / comparison_data['camera_mp'].max() * 25) +
                (comparison_data['ram_gb'] / comparison_data['ram_gb'].max() * 20) +
                (comparison_data['battery_mah'] / comparison_data['battery_mah'].max() * 20) +
                (comparison_data['processor_score'] / comparison_data['processor_score'].max() * 25) +
                ((1 - (comparison_data['price_numeric'] / comparison_data['price_numeric'].max())) * 10)
            )
            
            # Create bubble chart
            fig = px.scatter(
                comparison_data,
                x='price_numeric',
                y='value_score',
                size='camera_mp',
                color='rating_numeric',
                hover_name='model',
                labels={
                    'price_numeric': 'Price (₹)',
                    'value_score': 'Value Score (0-100)',
                    'rating_numeric': 'User Rating'
                },
                title='Price vs Value Analysis (bubble size = camera quality)',
                color_continuous_scale='RdYlGn',
                size_max=60
            )
            
            fig.update_layout(
                height=500,
                xaxis=dict(gridcolor='#e0e0e0'),
                yaxis=dict(gridcolor='#e0e0e0'),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Best value phone
            best_value_idx = comparison_data['value_score'].idxmax()
            best_value = comparison_data.loc[best_value_idx]
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                            color: white; padding: 24px; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 16px rgba(17, 153, 142, 0.3);">
                    <h3 style="margin: 0 0 8px 0;">Best Value for Money</h3>
                    <h2 style="margin: 0 0 12px 0;">{best_value['model']}</h2>
                    <p style="font-size: 1.2rem; font-weight: 600; margin: 0;">
                        Value Score: {best_value['value_score']:.1f}/100
                    </p>
                </div>
            """, unsafe_allow_html=True)


def show_analytics_page(df):
    """Data analytics page"""
    st.header("Advanced Data Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Phones", f"{len(df):,}")
    with col2:
        st.metric("Avg Price", f"₹{df['price_numeric'].mean():,.0f}")
    with col3:
        st.metric("Median Price", f"₹{df['price_numeric'].median():,.0f}")
    with col4:
        st.metric("Avg Rating", f"{df['rating_numeric'].mean():.2f}/10")
    with col5:
        st.metric("Brands", f"{df['model'].str.split().str[0].nunique()}")
    
    st.markdown("---")
    
    # Statistical Summary Section
    st.markdown("### Statistical Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Price Statistics")
        price_stats = df['price_numeric'].describe()
        stats_df = pd.DataFrame({
            'Metric': ['Minimum', 'Maximum', 'Mean', 'Median', 'Std Dev', '25th %ile', '75th %ile'],
            'Value': [
                f"₹{price_stats['min']:,.0f}",
                f"₹{price_stats['max']:,.0f}",
                f"₹{price_stats['mean']:,.0f}",
                f"₹{price_stats['50%']:,.0f}",
                f"₹{price_stats['std']:,.0f}",
                f"₹{price_stats['25%']:,.0f}",
                f"₹{price_stats['75%']:,.0f}"
            ]
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Feature Statistics")
        feature_stats = pd.DataFrame({
            'Feature': ['Camera (MP)', 'RAM (GB)', 'Battery (mAh)', 'Display (inch)', 'Processor'],
            'Average': [
                f"{df['camera_mp'].mean():.1f}",
                f"{df['ram_gb'].mean():.1f}",
                f"{df['battery_mah'].mean():.0f}",
                f"{df['display_inches'].mean():.2f}",
                f"{df['processor_score'].mean():.0f}"
            ],
            'Max': [
                f"{df['camera_mp'].max():.1f}",
                f"{df['ram_gb'].max():.0f}",
                f"{df['battery_mah'].max():.0f}",
                f"{df['display_inches'].max():.2f}",
                f"{df['processor_score'].max():.0f}"
            ],
            'Min': [
                f"{df['camera_mp'].min():.1f}",
                f"{df['ram_gb'].min():.0f}",
                f"{df['battery_mah'].min():.0f}",
                f"{df['display_inches'].min():.2f}",
                f"{df['processor_score'].min():.0f}"
            ]
        })
        st.dataframe(feature_stats, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution with box plot
        fig = px.histogram(
            df, 
            x='price_numeric',
            nbins=50,
            title='Price Distribution Analysis',
            labels={'price_numeric': 'Price (₹)', 'count': 'Number of Phones'},
            color_discrete_sequence=['#667eea'],
            marginal='box'  # Added box plot on top
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        
        # Price insights
        st.info(f"""
        **Key Insights:**
        - Most phones are in ₹{price_stats['25%']:,.0f} - ₹{price_stats['75%']:,.0f} range
        - Price spread from ₹{price_stats['min']:,.0f} to ₹{price_stats['max']:,.0f}
        - Standard deviation: ₹{price_stats['std']:,.0f}
        """)
    
    with col2:
        # Price category distribution - Donut chart
        category_counts = df['price_category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Market Segmentation by Price',
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'],
            hole=0.4  # Donut chart
        )
        fig.update_traces(textinfo='percent+label+value', textposition='outside')
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        dominant_category = category_counts.idxmax()
        st.success(f"**Market Focus:** {dominant_category} dominates with {category_counts.max()} models ({category_counts.max()/len(df)*100:.1f}%)")
    
    st.markdown("---")
    
    # Correlation Analysis
    st.markdown("### Feature Correlation Analysis")
    
    # Calculate correlation matrix
    corr_data = df[['price_numeric', 'camera_mp', 'ram_gb', 'battery_mah', 'rating_numeric', 'processor_score', 'display_inches']].corr()
    
    fig = px.imshow(
        corr_data,
        labels=dict(x="Features", y="Features", color="Correlation"),
        x=['Price', 'Camera', 'RAM', 'Battery', 'Rating', 'Processor', 'Display'],
        y=['Price', 'Camera', 'RAM', 'Battery', 'Rating', 'Processor', 'Display'],
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        aspect='auto',
        title='Feature Correlation Heatmap',
        text_auto='.2f'  # Show correlation values
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation insights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        price_camera_corr = corr_data.loc['price_numeric', 'camera_mp']
        st.metric("Price ↔ Camera", f"{price_camera_corr:.3f}", delta="Correlation")
    with col2:
        price_ram_corr = corr_data.loc['price_numeric', 'ram_gb']
        st.metric("Price ↔ RAM", f"{price_ram_corr:.3f}", delta="Correlation")
    with col3:
        price_processor_corr = corr_data.loc['price_numeric', 'processor_score']
        st.metric("Price ↔ Processor", f"{price_processor_corr:.3f}", delta="Correlation")
    with col4:
        rating_price_corr = corr_data.loc['rating_numeric', 'price_numeric']
        st.metric("Rating ↔ Price", f"{rating_price_corr:.3f}", delta="Correlation")
    
    st.markdown("---")
    
    # Charts row 2 - Feature Relationships
    st.markdown("### Feature Relationship Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Camera vs Price with trendline
        fig = px.scatter(
            df,
            x='camera_mp',
            y='price_numeric',
            color='ram_gb',
            size='battery_mah',
            title='Camera Quality vs Price (size=battery, color=RAM)',
            labels={
                'camera_mp': 'Camera (MP)',
                'price_numeric': 'Price (₹)',
                'ram_gb': 'RAM (GB)'
            },
            color_continuous_scale='Viridis',
            trendline='ols',  # Ordinary Least Squares regression line
            hover_data=['model']
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Battery vs Price with trendline
        fig = px.scatter(
            df[df['battery_mah'] > 0],
            x='battery_mah',
            y='price_numeric',
            color='processor_score',
            size='camera_mp',
            title='Battery Capacity vs Price (size=camera, color=processor)',
            labels={
                'battery_mah': 'Battery (mAh)',
                'price_numeric': 'Price (₹)',
                'processor_score': 'Processor Score'
            },
            color_continuous_scale='Plasma',
            trendline='ols',
            hover_data=['model']
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Charts row 3 - RAM & Battery
    st.markdown("### RAM & Battery Capacity Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # RAM distribution
        ram_counts = df['ram_gb'].value_counts().sort_index()
        fig = px.bar(
            x=ram_counts.index,
            y=ram_counts.values,
            title='Phones by RAM Capacity',
            labels={'x': 'RAM (GB)', 'y': 'Number of Phones'},
            color=ram_counts.values,
            color_continuous_scale='Greens',
            text=ram_counts.values
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400, showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        
        # RAM insight
        most_common_ram = ram_counts.idxmax()
        st.info(f"**Most Common:** {most_common_ram} GB RAM with {ram_counts.max()} phones")
    
    with col2:
        # Box plot for prices by RAM
        fig = px.box(
            df[df['ram_gb'].between(4, 16)],
            x='ram_gb',
            y='price_numeric',
            title='Price Distribution by RAM Capacity',
            labels={'ram_gb': 'RAM (GB)', 'price_numeric': 'Price (₹)'},
            color='ram_gb',
            color_discrete_sequence=px.colors.sequential.Plasma,
            points='outliers'  # Show outliers
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Brand Analysis
    st.markdown("### Brand Performance Analysis")
    df_temp = df.copy()
    df_temp['brand'] = df_temp['model'].str.split().str[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top brands by count
        brand_counts = df_temp['brand'].value_counts().head(10)
        
        fig = px.bar(
            x=brand_counts.index,
            y=brand_counts.values,
            title='Top 10 Brands by Model Count',
            labels={'x': 'Brand', 'y': 'Number of Models'},
            color=brand_counts.values,
            color_continuous_scale='Blues',
            text=brand_counts.values
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400, showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average price by brand
        top_brands = brand_counts.head(10).index
        brand_avg_price = df_temp[df_temp['brand'].isin(top_brands)].groupby('brand')['price_numeric'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=brand_avg_price.index,
            y=brand_avg_price.values,
            title='Average Price by Top Brands',
            labels={'x': 'Brand', 'y': 'Average Price (₹)'},
            color=brand_avg_price.values,
            color_continuous_scale='Reds',
            text=[f"₹{v:,.0f}" for v in brand_avg_price.values]
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400, showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Market Insights
    st.markdown("### Market Insights & Key Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Best value phones
        df_temp['value_score'] = (
            (df_temp['camera_mp'] / df_temp['camera_mp'].max() * 25) +
            (df_temp['ram_gb'] / df_temp['ram_gb'].max() * 25) +
            (df_temp['battery_mah'] / df_temp['battery_mah'].max() * 25) +
            (df_temp['processor_score'] / df_temp['processor_score'].max() * 25)
        )
        
        best_value = df_temp.nlargest(1, 'value_score').iloc[0]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    padding: 20px; border-radius: 10px; color: white;">
            <h4 style="margin: 0;">Best Overall Features</h4>
            <p style="margin: 5px 0; font-size: 0.9rem;">{best_value['model'][:30]}</p>
            <p style="margin: 0; font-weight: 600;">Score: {best_value['value_score']:.1f}/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Most popular price range
        popular_category = df_temp['price_category'].mode()[0]
        popular_count = len(df_temp[df_temp['price_category'] == popular_category])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 10px; color: white;">
            <h4 style="margin: 0;">Market Focus</h4>
            <p style="margin: 5px 0; font-size: 0.9rem;">{popular_category} Segment</p>
            <p style="margin: 0; font-weight: 600;">{popular_count} phones ({popular_count/len(df_temp)*100:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Average rating insight
        high_rated = len(df_temp[df_temp['rating_numeric'] >= 7.5])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 20px; border-radius: 10px; color: white;">
            <h4 style="margin: 0;">High Quality Phones</h4>
            <p style="margin: 5px 0; font-size: 0.9rem;">Rating ≥ 7.5/10</p>
            <p style="margin: 0; font-weight: 600;">{high_rated} phones ({high_rated/len(df_temp)*100:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)


def show_explorer_page(df):
    """Phone explorer page"""
    st.header("Phone Explorer")
    st.markdown("### Filter and explore the phone database")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        price_range = st.slider(
            "Price Range (₹)",
            min_value=int(df['price_numeric'].min()),
            max_value=int(df['price_numeric'].max()),
            value=(int(df['price_numeric'].min()), int(df['price_numeric'].max())),
            step=1000
        )
    
    with col2:
        ram_options = ['All'] + sorted([x for x in df['ram_gb'].unique().tolist() if x > 0])
        ram_filter = st.selectbox("RAM (GB)", ram_options)
    
    with col3:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.5)
    
    # Apply filters
    filtered_df = df[
        (df['price_numeric'].between(price_range[0], price_range[1])) &
        (df['rating_numeric'].fillna(0) >= min_rating)
    ]
    
    if ram_filter != 'All':
        filtered_df = filtered_df[filtered_df['ram_gb'] == ram_filter]
    
    st.markdown(f"### Found {len(filtered_df)} phones matching your criteria")
    
    # Display results
    if len(filtered_df) > 0:
        # Show data table with price_numeric for sorting
        display_df = filtered_df[['model', 'price', 'rating_numeric', 'processor', 'camera', 'ram', 'battery', 'display', 'price_numeric']].copy()
        
        # Fix rating display
        display_df['rating_numeric'] = display_df['rating_numeric'].apply(
            lambda x: x / 10 if pd.notna(x) and x > 10 else x
        )
        
        # Sort by price
        display_df = display_df.sort_values('price_numeric', ascending=False)
        
        # Drop price_numeric before display
        display_columns = display_df.drop(columns=['price_numeric']).copy()
        display_columns.columns = ['Model', 'Price', 'Rating', 'Processor', 'Camera', 'RAM', 'Battery', 'Display']
        
        st.dataframe(
            display_columns,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_phones.csv",
            mime="text/csv"
        )
    else:
        st.warning("No phones match your filter criteria. Try adjusting the filters.")


def show_insights_page(df):
    """Market insights page"""
    st.header("Market Insights & Trends")
    
    # Top brands (from model names)
    st.markdown("### Brand Analysis")
    
    # Extract brand from model name (first word)
    df['brand'] = df['model'].str.split().str[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top brands by count
        top_brands = df['brand'].value_counts().head(10)
        fig = px.bar(
            x=top_brands.values,
            y=top_brands.index,
            orientation='h',
            title='Top 10 Brands by Number of Models',
            labels={'x': 'Number of Models', 'y': 'Brand'},
            color=top_brands.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average price by brand
        brand_avg_price = df.groupby('brand')['price_numeric'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=brand_avg_price.values,
            y=brand_avg_price.index,
            orientation='h',
            title='Top 10 Brands by Average Price',
            labels={'x': 'Average Price (₹)', 'y': 'Brand'},
            color=brand_avg_price.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Feature Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Camera trends
        camera_price = df.groupby('camera_mp')['price_numeric'].mean().reset_index()
        camera_price = camera_price[camera_price['camera_mp'].between(10, 200)]
        
        fig = px.scatter(
            camera_price,
            x='camera_mp',
            y='price_numeric',
            title='Camera Quality vs Average Price',
            labels={'camera_mp': 'Camera (MP)', 'price_numeric': 'Avg Price (₹)'},
            trendline='lowess',
            color='price_numeric',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Rating distribution
        rating_dist = df[df['rating_numeric'].notna()]['rating_numeric']
        fig = px.histogram(
            rating_dist,
            nbins=20,
            title='User Rating Distribution',
            labels={'value': 'Rating', 'count': 'Number of Phones'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.markdown("### Summary Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Price Statistics")
        st.write(f"**Min:** ₹{df['price_numeric'].min():,.0f}")
        st.write(f"**Max:** ₹{df['price_numeric'].max():,.0f}")
        st.write(f"**Mean:** ₹{df['price_numeric'].mean():,.0f}")
        st.write(f"**Median:** ₹{df['price_numeric'].median():,.0f}")
    
    with col2:
        st.markdown("#### Camera Statistics")
        st.write(f"**Min:** {df['camera_mp'].min():.1f} MP")
        st.write(f"**Max:** {df['camera_mp'].max():.1f} MP")
        st.write(f"**Mean:** {df['camera_mp'].mean():.1f} MP")
        st.write(f"**Median:** {df['camera_mp'].median():.1f} MP")
    
    with col3:
        st.markdown("#### Battery Statistics")
        st.write(f"**Min:** {df['battery_mah'].min():.0f} mAh")
        st.write(f"**Max:** {df['battery_mah'].max():.0f} mAh")
        st.write(f"**Mean:** {df['battery_mah'].mean():.0f} mAh")
        st.write(f"**Median:** {df['battery_mah'].median():.0f} mAh")


if __name__ == "__main__":
    main()
