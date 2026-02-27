# app.py - Beyond the Pantry: Food Coverage Predictor
# =====================================================
# A simple, user-friendly app for predicting neighborhood food coverage

import streamlit as st
import joblib
import json
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="🍎 Beyond the Pantry",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* BIG CAPTIVATING HEADER */
    .main-title {
        font-size: 5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #1B5E20, #4CAF50, #81C784);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .subtitle {
        font-size: 1.8rem;
        color: #333;
        text-align: center;
        font-weight: 600;
        margin-top: 0;
    }
    .tagline {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E8F5E9;
    }
    /* Prediction result boxes */
    .result-high {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        border-left: 8px solid #2E7D32;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .result-low {
        background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
        border-left: 8px solid #C62828;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    /* Scenario explanation boxes */
    .scenario-card {
        background: #F5F5F5;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 5px solid #2196F3;
    }
    .scenario-positive {
        border-left-color: #4CAF50;
        background: #F1F8E9;
    }
    .scenario-negative {
        border-left-color: #F44336;
        background: #FFF3E0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LOAD MODEL AND DATA
# =============================================================================
@st.cache_resource
def load_model():
    return joblib.load("coverage_model.pkl")

@st.cache_resource
def load_scaler():
    return joblib.load("scaler.pkl")

@st.cache_data
def load_metadata():
    with open("model_metadata.json", "r") as f:
        return json.load(f)

try:
    model = load_model()
    scaler = load_scaler()
    meta = load_metadata()
except Exception as e:
    st.error(f"⚠️ Error loading files: {e}")
    st.info("Make sure coverage_model.pkl, scaler.pkl, and model_metadata.json are in the same folder as app.py")
    st.stop()

# =============================================================================
# BIG CAPTIVATING HEADER
# =============================================================================
st.markdown('<h1 class="main-title">🍎 Beyond the Pantry</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">NYC Food Coverage Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Identify neighborhoods that need more food assistance resources</p>', unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.markdown("## 📊 Model Performance")
st.sidebar.metric("Precision (High)", "91%")
st.sidebar.metric("Recall (Catch low coverage neighborhood)", "92%")
st.sidebar.caption(f"Trained on {meta['training_info']['total_samples']} NYC neighborhoods")

st.sidebar.markdown("---")
st.sidebar.markdown("## Input Neighborhood Details")

# Get feature stats for slider ranges
feat_stats = meta['feature_statistics']

# Input widgets
food_insecure = st.sidebar.slider(
    "Food Insecurity Rate (%)",
    min_value=0.0,
    max_value=40.0,
    value=15.0,
    step=1.0,
    help="% of residents experiencing food insecurity"
)

unemployment = st.sidebar.slider(
    "Unemployment Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=8.0,
    step=0.5,
    help="% of labor force unemployed"
)

high_shelter = st.sidebar.checkbox(
    "High Shelter Population",
    value=False,
    help="Above-average shelter population in this area?"
)

has_kitchen = st.sidebar.checkbox(
    "Has Soup Kitchen",
    value=False,
    help="Are there soup kitchens in this neighborhood?"
)

has_weekend = st.sidebar.checkbox(
    "Has Weekend Hours",
    value=False,
    help="Are food sites open on weekends?"
)

st.sidebar.markdown("---")

predict_btn = st.sidebar.button("Predict Coverage", type="primary", use_container_width=True)

# =============================================================================
# MAIN CONTENT - TWO COLUMNS
# =============================================================================
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 Your Neighborhood Profile")
    
    profile_data = pd.DataFrame({
        "Factor": [
            "🍽️ Food Insecurity Rate",
            "💼 Unemployment Rate", 
            "🏠 High Shelter Area",
            "🍲 Has Soup Kitchen",
            "📅 Weekend Hours"
        ],
        "Value": [
            f"{food_insecure:.0f}%",
            f"{unemployment:.1f}%",
            "Yes ✓" if high_shelter else "No",
            "Yes ✓" if has_kitchen else "No",
            "Yes ✓" if has_weekend else "No"
        ]
    })
    st.dataframe(profile_data, use_container_width=True, hide_index=True)
    
    # Comparison chart
    st.markdown("#### Inputs vs NYC Average")
    
    comp_data = pd.DataFrame({
        'Metric': ['Food Insecurity', 'Unemployment'],
        'Your Input': [food_insecure, unemployment],
        'NYC Average': [feat_stats['food_insecure_percentage']['mean'], 
                       feat_stats['unemployment_rate']['mean']]
    }).melt(id_vars=['Metric'], var_name='Type', value_name='Rate')
    
    chart = alt.Chart(comp_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X('Metric:N', axis=alt.Axis(labelAngle=0, title='')),
        y=alt.Y('Rate:Q', title='Rate (%)'),
        color=alt.Color('Type:N', scale=alt.Scale(
            domain=['Your Input', 'NYC Average'],
            range=['#78c679', '#BDBDBD']
        )),
        xOffset='Type:N'
    ).properties(height=220).configure_legend(orient='bottom', title=None)
    
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.markdown("### Prediction Result")
    
    if predict_btn:
        # Prepare and scale input
        input_data = np.array([[food_insecure, unemployment, float(high_shelter), 
                               int(has_kitchen), int(has_weekend)]])
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        proba = model.predict_proba(input_scaled)[0]
        
        if prediction == 1:
            st.markdown("""
            <div class="result-high">
                <h2 style="color:#1B5E20; margin:0;">✅ HIGH COVERAGE</h2>
                <p style="font-size:1.2rem; margin-top:0.5rem;">This neighborhood likely has adequate food assistance.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**Confidence: {proba[1]*100:.0f}%**")
            st.progress(proba[1])
        else:
            st.markdown("""
            <div class="result-low">
                <h2 style="color:#B71C1C; margin:0;">⚠️ LOW COVERAGE</h2>
                <p style="font-size:1.2rem; margin-top:0.5rem;">This neighborhood needs more food assistance resources.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**Confidence: {proba[0]*100:.0f}%**")
            st.progress(proba[0])
        
        st.markdown("---")
        st.markdown("### Recommended Actions")
        
        if prediction == 0:
            st.markdown("""
            - **Add new food sites** in this area
            - **Extend hours** at existing locations  
            - **Partner** with local organizations
            - **Prioritize** in next funding cycle
            """)
        else:
            st.markdown("""
            - **Maintain** current service levels
            - **Monitor** for changes in need
            - **Share** best practices with other areas
            """)
    else:
        st.info("👈 Enter neighborhood details and click **Predict Coverage**")
        
        st.markdown("---")
        st.markdown("### Quick Guide")
        st.markdown("""
        **Likely LOW coverage:**
        - High food insecurity + No weekend hours
        
        **Likely HIGH coverage:**  
        - Has soup kitchen + Weekend hours available
        """)

# =============================================================================
# MODEL DETAILS (SIMPLIFIED - NO "HOW IT WORKS")
# =============================================================================
st.markdown("---")
st.markdown("## 📊 Model Details")

tab1, tab2 = st.tabs(["📈 Performance", "🔍 What Affects Coverage"])

# TAB 1: Performance Metrics
with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### Accuracy Metrics")
        
        metrics_df = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision (High)', 'Recall (Low)', 'F1 Score'],
            'Score': [0.86, 0.91, 0.92, 0.86]
        })
        
        bar = alt.Chart(metrics_df).mark_bar(color='#78c679', cornerRadiusTopRight=5, cornerRadiusTopLeft=5).encode(
            x=alt.X('Metric:N', axis=alt.Axis(labelAngle=0, title='')),
            y=alt.Y('Score:Q', scale=alt.Scale(domain=[0,1]), title='Score')
        ).properties(height=280)
        
        text = bar.mark_text(dy=-10, fontSize=14, fontWeight='bold').encode(
            text=alt.Text('Score:Q', format='.0%')
        )
        
        st.altair_chart(bar + text, use_container_width=True)
        
        st.markdown("""
        **What these mean:**
        - **86% Accuracy** - Correct 86 out of 100 times
        - **91% Precision** - When we say HIGH, we're right 91%
        - **92% Recall** - We catch 92% of LOW coverage areas
        """)
    
    with c2:
        st.markdown("#### Confusion Matrix")
        
        # Create confusion matrix with BLACK text
        fig, ax = plt.subplots(figsize=(5, 4))
        
        # User's actual confusion matrix values
        cm = np.array([[23, 2], [5, 20]])
        
        # Light green colormap
        ax.imshow(cm, cmap=plt.cm.Greens, alpha=0.3)
        
        # Labels
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Predicted\nLow', 'Predicted\nHigh'], fontsize=11)
        ax.set_yticklabels(['Actual\nLow', 'Actual\nHigh'], fontsize=11)
        
        # BLACK text values
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha='center', va='center', 
                       fontsize=22, fontweight='bold', color='black')
        
        ax.set_title('Test Results (50 neighborhoods)', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        st.markdown("""
        **Reading this:**
        - **23** - Correctly found LOW coverage ✓
        - **20** - Correctly found HIGH coverage ✓
        - **7 errors** out of 50 predictions
        """)

# TAB 2: What Affects Coverage (SCENARIOS, NO ODDS RATIOS)
with tab2:
    st.markdown("#### How Each Factor Affects Coverage")
    st.markdown("*Simple scenarios to understand each factor's impact:*")
    
    # Food Insecurity - NEGATIVE
    st.markdown("""
    <div class="scenario-card scenario-negative">
        <h4 style="margin:0;">🍽️ Food Insecurity Rate</h4>
        <p style="margin:0.5rem 0;"><strong>Effect: Makes LOW coverage more likely</strong></p>
        <p style="margin:0;"><em>Scenario:</em> Compare two neighborhoods - one with 10% food insecurity and another with 25%. 
        The neighborhood with <strong>higher food insecurity is more likely to have LOW coverage</strong>. 
        This shows that areas with the greatest need often have the fewest resources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Unemployment - POSITIVE  
    st.markdown("""
    <div class="scenario-card scenario-positive">
        <h4 style="margin:0;">💼 Unemployment Rate</h4>
        <p style="margin:0.5rem 0;"><strong>Effect: Makes HIGH coverage more likely</strong></p>
        <p style="margin:0;"><em>Scenario:</em> Areas with higher unemployment tend to have <strong>better food coverage</strong>. 
        This is good news - food programs have successfully targeted economically distressed areas!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # High Shelter - Variable (using actual coefficient which is positive)
    st.markdown("""
    <div class="scenario-card scenario-positive">
        <h4 style="margin:0;">🏠 High Shelter Population</h4>
        <p style="margin:0.5rem 0;"><strong>Effect: Makes HIGH coverage more likely</strong></p>
        <p style="margin:0;"><em>Scenario:</em> Neighborhoods with large shelter populations tend to have <strong>more food resources</strong>. 
        This suggests programs are reaching these vulnerable populations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Has Kitchen - POSITIVE
    st.markdown("""
    <div class="scenario-card scenario-positive">
        <h4 style="margin:0;">🍲 Has Soup Kitchen</h4>
        <p style="margin:0.5rem 0;"><strong>Effect: Makes HIGH coverage more likely</strong></p>
        <p style="margin:0;"><em>Scenario:</em> Neighborhoods with soup kitchens are <strong>much more likely to have good coverage</strong>. 
        Soup kitchens are a strong sign that an area has adequate food resources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Has Weekend - POSITIVE
    st.markdown("""
    <div class="scenario-card scenario-positive">
        <h4 style="margin:0;">📅 Weekend Hours</h4>
        <p style="margin:0.5rem 0;"><strong>Effect: Makes HIGH coverage more likely</strong></p>
        <p style="margin:0;"><em>Scenario:</em> Areas with weekend food services have <strong>better coverage</strong>. 
        Weekend availability matters because many working families can only access services on weekends.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    st.success("**Key Insight:** Soup kitchens and weekend hours are the strongest positive factors. High food insecurity is the strongest predictor of poor coverage.")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
fc1, fc2 = st.columns([2, 1])

with fc1:
    st.markdown("""
    **🍎 Beyond the Pantry** | NYC Food Insecurity Analysis  
    *Helping policymakers identify neighborhoods that need more food assistance.*
    """)
