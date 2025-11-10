# Vendor & Project Management Dashboard

A comprehensive operations management dashboard for vendor relationships, contract tracking, and project coordination with Google Drive automation.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

Professional operations management tool designed for HDO (Human Data Operations) teams. Features vendor lifecycle management, contract administration, project coordination with visual scorecards, and automated Google Drive folder creation.

Perfect for operations associates managing multiple vendors, contracts, and projects simultaneously.

## ✨ Features

### 🌙 **Dark Mode Theme**
- Professional dark blue-black color scheme
- Easy on the eyes for extended use
- Optimized for all dashboard elements

### 👥 **Vendor Management**
- Complete vendor profile management
- Track onboarding status (Pending → In Progress → Active → Inactive)
- Contact information and location tracking
- Vendor type categorization
- **Google Drive Integration**: Auto-create folder structure for new vendors
- CSV export functionality

### 📄 **Contract & Agreement Tracking**
- Link contracts to vendors
- Monitor contract lifecycle (Draft → Active → Pending Renewal → Expired)
- Track contract values and PO numbers
- **Contract Renewal Timeline**: Visual timeline with renewal notice markers
- Expiration alerts and notifications
- Document management with links

### 🚀 **Project Coordination Dashboard**
- **Visual Scorecard**: Red/Yellow/Green status indicators
  - 🟢 **Green**: On track
  - 🟡 **Yellow**: At risk / Needs attention
  - 🔴 **Red**: Off track / Critical issues
- **Google Drive Integration**: Auto-create organized project folders
- Timeline tracking (start date, target date, completion)
- Deliverables management
- Quick status updates

### 🗂️ **Google Drive API Integration**
- Automatic folder creation for vendors and projects
- Organized structure: Contracts / Deliverables / Meeting Notes / Documentation
- Direct links to folders in dashboard
- OAuth 2.0 secure authentication
- Configurable parent folder

### 📊 **Analytics & Reports**
- Vendor status distribution (pie charts)
- Contract status breakdown
- Project health scorecard (bar charts)
- Summary metrics and KPIs
- Exportable reports (CSV format)

### 🎫 **Ticket System**
- Log and track vendor requests
- Priority management (High / Medium / Low)
- Status tracking (Open / In Progress / Resolved)
- Ticket type categorization

## 🚀 Quick Start

### 🪟 **Windows Users** (Recommended)

1. **Download this repository** (Click "Code" → "Download ZIP")
2. **Extract** to a folder
3. **Double-click `run.bat`** to install and start
4. Dashboard opens automatically at http://localhost:8501

**Detailed guide:** See [`WINDOWS_SETUP.md`](WINDOWS_SETUP.md)

### 🐧 **Mac/Linux Users**

```bash
# Clone repository
git clone https://github.com/NeilInn/vendor-management-dashboard.git
cd vendor-management-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

## 📋 Requirements

- **Python 3.8+**
- **Operating System**: Windows 10/11, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB
- **Internet**: Optional (for Google Drive API integration)

## 🗂️ Google Drive Setup (Optional)

Want automatic folder creation? Follow these steps:

1. **Create Google Cloud Project** and enable Google Drive API
2. **Create OAuth 2.0 credentials** (Desktop app)
3. **Download credentials** as `credentials.json`
4. **Place in project folder**
5. **Add yourself as test user** in OAuth consent screen
6. **Authenticate** on first use

**Detailed guide:** See [`GOOGLE_DRIVE_SETUP.md`](GOOGLE_DRIVE_SETUP.md)

**Note:** Dashboard works perfectly without Google Drive - this is an optional automation feature!

## 📁 Project Structure

```
vendor-management-dashboard/
├── app.py                      # Main Streamlit dashboard (1000+ lines)
├── database.py                 # Database operations (SQLite)
├── google_drive.py             # Google Drive API integration
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows launcher script
├── README.md                   # Main documentation (this file)
├── WINDOWS_SETUP.md            # Windows setup guide
├── GOOGLE_DRIVE_SETUP.md       # Google Drive API setup guide
├── CHANGELOG_FIXES.md          # Recent fixes and updates
├── START_HERE.txt              # Quick start reference
├── .streamlit/
│   └── config.toml             # Dark mode theme configuration
├── .gitignore                  # Security (protects credentials)
└── credentials.json            # Google API credentials (not in repo)
```

## 💻 Technology Stack

- **[Python 3.8+](https://www.python.org/)** - Programming language
- **[Streamlit](https://streamlit.io/)** - Web framework
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[Plotly](https://plotly.com/python/)** - Interactive visualizations
- **[Google Drive API](https://developers.google.com/drive)** - Cloud integration
- **SQLite** - Data storage (for real implementation)

## 🎨 Screenshots

### Dashboard Overview
![Dashboard](screenshots/dashboard.png)

### Project Scorecard (Red/Yellow/Green Status)
![Scorecard](screenshots/scorecard.png)

*Note: Add screenshots to `/screenshots` folder*

## 🔧 Usage

### Running the Dashboard

**Windows:**
```cmd
run.bat
```

**Mac/Linux:**
```bash
streamlit run app.py
```

### First-Time Setup

1. **Load sample data**: In sidebar, click "Initialize Sample Data"
2. **Explore pages**: Use sidebar navigation
3. **Add vendors**: Go to Vendor Directory → Add New Vendor
4. **Create projects**: Go to Project Coordination → Create Project

### Google Drive Folder Creation

**For Vendors:**
1. Go to **Vendor Directory**
2. Click **"Add New Vendor with Google Drive Integration"**
3. Fill in details
4. Check **"Create Google Drive folder for this vendor"**
5. Click **"Add Vendor"**
6. Folders created automatically!

**For Projects:**
1. Go to **Project Coordination**
2. Expand **"Create Google Drive Project Folder"**
3. Enter project name
4. Click **"Create Google Drive Folder Structure"**
5. Folders created in your Drive!

## 🌐 Deploy to Web

### Streamlit Community Cloud (Free)

1. Push code to GitHub (already done!)
2. Go to: https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select: `NeilInn/vendor-management-dashboard`
6. Main file: `app.py`
7. Click "Deploy"
8. Get your public URL!

**Note:** Google Drive features work locally. For production deployment, you'd add Streamlit secrets.

## 🔒 Security

- ✅ Credentials protected by `.gitignore`
- ✅ OAuth 2.0 authentication
- ✅ No hardcoded sensitive data
- ✅ Token-based API access
- ✅ No mention of specific companies (per requirements)

**Never commit:**
- `credentials.json`
- `token.pickle`
- `.env` files

## 🎯 Key Differentiators

1. **Fully Functional** - Not mockups, real working software
2. **Professional Quality** - Production-ready code with documentation
3. **Automation Focus** - Google Drive integration shows technical initiative
4. **Visual Scorecard** - Red/Yellow/Green status exactly as specified in ops roles
5. **Comprehensive** - Covers all aspects of vendor operations management
6. **Dark Mode** - Modern, professional appearance

## 🤝 Contributing

This is a portfolio project, but feedback is welcome!

## 📄 License

MIT License - Free to use and modify

## 👤 Author

**Neil Inn**
- GitHub: [@NeilInn](https://github.com/NeilInn)
- Repository: [vendor-management-dashboard](https://github.com/NeilInn/vendor-management-dashboard)

## 🙏 Acknowledgments

Built to demonstrate operational excellence and technical proficiency for HDO Operations Associate roles.

---

**Built with Python, Streamlit, and attention to operational detail** 📊✨
