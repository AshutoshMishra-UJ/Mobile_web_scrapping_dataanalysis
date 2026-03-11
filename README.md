# 📱 Mobile Phone Recommendation System - Interactive Dashboard

## 🎯 Project Overview
A comprehensive data science project demonstrating web scraping, data analysis, and machine learning recommendation system with an interactive Streamlit dashboard.

## 🚀 Features

### 1. **Web Scraping Module**
- `smartprix.py` - Selenium-based web scraper for Smartprix.com
- Anti-detection features (CAPTCHA handling)
- Dynamic page scrolling for complete data extraction
- Extracts 1000+ phone specifications

### 2. **Data Processing & Analysis**
- `smartprix-phones.ipynb` - Jupyter notebook for data parsing
- BeautifulSoup for HTML parsing
- Pandas for data manipulation
- Feature extraction (price, camera, RAM, battery, etc.)

### 3. **CLI Recommendation System**
- `phone_recommendation_system.py` - Command-line interface
- Multi-criteria recommendations:
  - Best Camera
  - Best Processor
  - Best RAM
  - Best Battery
  - Highest Rated
  - Overall Best (weighted scoring)

### 4. **Interactive Dashboard** ⭐
- `streamlit_phone_dashboard.py` - Professional web dashboard
- **4 Main Pages:**
  1. **Home & Recommendations** - AI-powered personalized recommendations
  2. **Data Analytics** - Interactive visualizations and insights
  3. **Phone Explorer** - Advanced filtering and search
  4. **Market Insights** - Brand analysis and market trends

## 📊 Dashboard Features

### Home & Recommendations
- Budget-based filtering
- 6 recommendation criteria
- Visual comparison charts
- Detailed specifications display

### Data Analytics
- Price distribution analysis
- Category-wise breakdown
- RAM & Battery trends
- Feature correlation heatmap
- Interactive scatter plots

### Phone Explorer
- Real-time filtering by:
  - Price range
  - RAM capacity
  - Minimum rating
- Downloadable filtered results
- Sortable data table

### Market Insights
- Top brands analysis
- Average price by brand
- Camera quality vs price trends
- Rating distribution
- Comprehensive statistics

## 🛠️ Technologies Used

### Web Scraping
- **Selenium** - Browser automation
- **BeautifulSoup** - HTML parsing
- **ChromeDriver** - Chrome browser control

### Data Science
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Python Regex** - Data extraction

### Visualization & Dashboard
- **Streamlit** - Web app framework
- **Plotly** - Interactive charts
- **plotly.express** - Quick visualizations
- **plotly.graph_objects** - Advanced plots

## 📥 Installation

### Prerequisites
```bash
Python 3.8 or higher
ChromeDriver (for web scraping)
```

### Install Dependencies
```bash
# For web scraping
pip install selenium beautifulsoup4 pandas numpy lxml

# For dashboard
pip install streamlit plotly

# Or install all at once
pip install -r requirements_dashboard.txt
```

## 🚀 Usage

### Step 1: Scrape Data
```bash
python smartprix.py
```
This will:
- Launch Chrome browser
- Navigate to Smartprix.com
- Apply filters
- Scroll through all pages
- Save HTML to `smartprix.html`

### Step 2: Process Data
Run all cells in `smartprix-phones.ipynb` to:
- Parse HTML
- Extract phone specifications
- Clean and structure data
- Save to `smartprix_phones_data.csv`

### Step 3: Run Dashboard
```bash
streamlit run streamlit_phone_dashboard.py
```
This will:
- Launch local web server
- Open dashboard in browser (http://localhost:8501)
- Load and cache data
- Display interactive interface

## 📱 Using the Recommendation System

### CLI Version
```bash
python phone_recommendation_system.py
```
Follow the interactive prompts to:
1. Enter your budget
2. Choose recommendation criteria
3. Specify number of recommendations
4. View detailed results

### Dashboard Version
1. Open the dashboard in your browser
2. Navigate to "Home & Recommendations"
3. Set your budget using the slider
4. Click on your priority (Camera, Processor, RAM, etc.)
5. View personalized recommendations
6. Compare phones with interactive charts

## 📊 Data Science Concepts Demonstrated

### 1. **Web Scraping**
- Dynamic content handling
- Anti-detection techniques
- Pagination and infinite scroll
- Robust error handling

### 2. **Data Cleaning & Processing**
- Regular expressions for extraction
- Missing value handling
- Data type conversion
- Feature engineering

### 3. **Feature Engineering**
- Price normalization
- Processor scoring algorithm
- Multi-feature extraction
- Category creation

### 4. **Recommendation Algorithm**
- Feature normalization (0-100 scale)
- Weighted scoring system
- Multi-criteria filtering
- Ranking algorithms

### 5. **Data Visualization**
- Distribution analysis
- Correlation analysis
- Trend identification
- Comparative analysis

### 6. **Interactive Dashboard Development**
- State management
- Real-time filtering
- Dynamic visualizations
- User experience design

## 🎨 Dashboard Screenshots

The dashboard includes:
- 📊 20+ Interactive Charts
- 🎯 6 Recommendation Modes
- 🔍 Advanced Filtering
- 📈 Statistical Analysis
- 💾 Data Export Capability

## 📈 Key Metrics Analyzed

- **Price Range**: ₹3,000 - ₹1,50,000+
- **Total Phones**: 1,020+
- **Camera Range**: 2MP - 200MP
- **RAM Options**: 1GB - 16GB
- **Battery Range**: 1,000mAh - 7,000mAh
- **Display Sizes**: 4" - 7.5"+

## 🔧 Customization

### Modify Recommendation Weights
Edit `streamlit_phone_dashboard.py`, line ~158:
```python
filtered['overall_score'] = (
    filtered['camera_score'] * 0.20 +      # Camera weight
    filtered['processor_norm'] * 0.25 +    # Processor weight
    filtered['ram_score'] * 0.15 +         # RAM weight
    filtered['battery_score'] * 0.15 +     # Battery weight
    filtered['rating_score'] * 0.15 +      # Rating weight
    filtered['display_score'] * 0.10       # Display weight
)
```

### Add New Visualizations
Add custom Plotly charts in the respective page functions.

### Customize Styling
Modify CSS in the `st.markdown()` section at the top of the file.

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Make sure you're in the correct directory
cd "c:\Users\ashut\OneDrive\Desktop\advanced-web-scraping-master\advanced-web-scraping-master"

# Run with full path
streamlit run streamlit_phone_dashboard.py
```

### Data file not found
Ensure you've run:
1. `smartprix.py` to generate HTML
2. All cells in `smartprix-phones.ipynb` to generate CSV

### ChromeDriver issues
- Update ChromeDriver to match your Chrome version
- Update the path in Python files

## 📚 Learning Outcomes

This project demonstrates:
✅ Web scraping with Selenium
✅ Data extraction with BeautifulSoup
✅ Data cleaning and preprocessing
✅ Feature engineering
✅ Recommendation algorithms
✅ Interactive dashboard development
✅ Data visualization with Plotly
✅ Streamlit app development
✅ Python best practices
✅ End-to-end data science pipeline

## 🎓 Portfolio Value

This project showcases:
- **Technical Skills**: Python, web scraping, data science
- **Libraries Mastery**: Selenium, Pandas, Streamlit, Plotly
- **Problem Solving**: Real-world recommendation system
- **User Interface**: Professional dashboard design
- **Documentation**: Comprehensive README and code comments

## 📝 License
This is a portfolio project for educational and demonstration purposes.

## 👤 Author
Ashutosh
Data Science Enthusiast

## 🔗 Files Structure
```
advanced-web-scraping-master/
│
├── smartprix.py                      # Web scraper
├── smartprix-phones.ipynb            # Data processing notebook
├── phone_recommendation_system.py    # CLI recommendation system
├── streamlit_phone_dashboard.py      # Streamlit dashboard
├── requirements_dashboard.txt        # Dependencies
├── README.md                         # This file
│
├── smartprix.html                    # Scraped HTML (generated)
└── smartprix_phones_data.csv         # Processed data (generated)
```

## 🚀 Future Enhancements

- [ ] Add machine learning models (clustering, classification)
- [ ] Implement collaborative filtering
- [ ] Add price prediction model
- [ ] Include user reviews sentiment analysis
- [ ] Add comparison with other e-commerce sites
- [ ] Implement email alerts for price drops
- [ ] Add export to PDF reports

---

Built with ❤️ for data science portfolio
