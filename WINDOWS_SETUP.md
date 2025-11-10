# Windows Setup Guide

Complete setup instructions for Windows users.

## 🚀 Quick Start (Easiest Method)

### Option 1: Double-Click to Run

1. **Download or clone this repository**
2. **Double-click `run.bat`** in the project folder
3. Wait for installation (first time only)
4. Dashboard opens automatically in your browser!

That's it! 🎉

---

## 📋 Step-by-Step Setup (First Time)

### Requirements

- **Windows 10 or 11**
- **Python 3.8+** installed
  - Check: Open Command Prompt and type `python --version`
  - Download from: https://www.python.org/downloads/
  - ✅ Make sure to check "Add Python to PATH" during installation

### Installation Steps

#### Step 1: Download the Project

**Option A: Download ZIP**
1. Click the green **"Code"** button on GitHub
2. Click **"Download ZIP"**
3. Extract to a folder (e.g., `C:\Users\YourName\Documents\vendor-management-dashboard`)

**Option B: Clone with Git**
```cmd
git clone https://github.com/NeilInn/vendor-management-dashboard.git
cd vendor-management-dashboard
```

#### Step 2: Install Dependencies

**Easy Method** - Double-click `run.bat` (it installs automatically!)

**Manual Method:**
```cmd
cd vendor-management-dashboard
pip install -r requirements.txt
```

#### Step 3: Run the Dashboard

**Method 1: Use the launcher**
- Double-click `run.bat`

**Method 2: Command line**
```cmd
cd vendor-management-dashboard
streamlit run app.py
```

#### Step 4: Access Dashboard

- Browser opens automatically at: http://localhost:8501
- Or manually open: http://localhost:8501

---

## 🗂️ Google Drive Setup (Optional)

Want automatic folder creation? Follow these steps:

### 1. Get Google API Credentials

1. Go to: https://console.cloud.google.com/
2. Create a new project: "Vendor Management Dashboard"
3. Enable: **Google Drive API**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download the JSON file
6. Rename to: `credentials.json`
7. Place in project folder: `C:\Users\...\vendor-management-dashboard\credentials.json`

### 2. Add Yourself as Test User

1. In Google Cloud Console → **OAuth consent screen**
2. Scroll to **Test users**
3. Click **+ ADD USERS**
4. Add your email
5. Click **SAVE**

### 3. First-Time Authentication

1. Run the dashboard
2. Go to **Vendor Directory**
3. Try adding a vendor with "Create Google Drive folder" checked
4. Browser popup will ask for permission
5. Click **Advanced** → **Go to Vendor Management Dashboard**
6. Click **Allow**
7. Done! Folders will now be created automatically

**Detailed guide:** See `GOOGLE_DRIVE_SETUP.md`

---

## 🎨 Features

- ✅ **Dark Mode** - Easy on the eyes
- ✅ **Vendor Management** - Track vendors and contacts
- ✅ **Contract Tracking** - Monitor contracts and renewals
- ✅ **Project Coordination** - Visual scorecards (red/yellow/green)
- ✅ **Google Drive Integration** - Auto-create folders
- ✅ **Analytics & Reports** - Export to CSV
- ✅ **Ticket System** - Track vendor requests

---

## 🔧 Troubleshooting

### "Python is not recognized"

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. During installation, check **"Add Python to PATH"**
3. Restart Command Prompt

### "streamlit: command not found"

**Solution:**
```cmd
pip install streamlit
```

### Port 8501 already in use

**Solution:**
```cmd
streamlit run app.py --server.port 8502
```

Then open: http://localhost:8502

### Dashboard won't start

**Solution:**
```cmd
# Delete these files if they exist
del vendor_management.db
del __pycache__

# Then run again
streamlit run app.py
```

### "Module not found" errors

**Solution:**
```cmd
pip install -r requirements.txt --upgrade
```

---

## 🎯 Quick Commands (Windows)

### Start Dashboard
```cmd
streamlit run app.py
```

### Stop Dashboard
- Press `Ctrl + C` in the Command Prompt window

### Install Dependencies
```cmd
pip install -r requirements.txt
```

### Update Dependencies
```cmd
pip install -r requirements.txt --upgrade
```

### Check Python Version
```cmd
python --version
```

---

## 📁 Project Structure

```
vendor-management-dashboard/
├── app.py                      # Main dashboard
├── database.py                 # Database operations
├── google_drive.py             # Google Drive integration
├── requirements.txt            # Python packages
├── run.bat                     # Windows launcher
├── README.md                   # Main documentation
├── WINDOWS_SETUP.md            # This file
├── GOOGLE_DRIVE_SETUP.md       # Google Drive guide
├── .streamlit/
│   └── config.toml             # Dark mode theme
└── .gitignore                  # Security (protects credentials)
```

---

## 💡 Tips for Windows Users

### Creating a Desktop Shortcut

1. **Right-click** on `run.bat`
2. Click **"Create shortcut"**
3. **Drag the shortcut** to your Desktop
4. Rename to: "Vendor Dashboard"
5. Now double-click the desktop icon to launch!

### Keeping Terminal Open

If the Command Prompt closes immediately:
1. **Right-click** `run.bat`
2. Click **"Edit"**
3. Add `pause` at the end
4. Save and close

### Running in Background

The dashboard runs in the Command Prompt window. To stop it:
- Click the window
- Press `Ctrl + C`
- Close the window

---

## 🌐 Deploy to Web (Optional)

Want to host it online?

1. **Go to:** https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Select:** Your repository
5. **Main file:** `app.py`
6. **Click "Deploy"**
7. Get your public URL!

---

## ✅ System Requirements

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 500MB
- **Internet:** For Google Drive API (optional)

---

## 📞 Need Help?

1. Check `README.md` for main documentation
2. See `GOOGLE_DRIVE_SETUP.md` for API setup
3. Review `CHANGELOG_FIXES.md` for recent changes
4. Check GitHub issues

---

## 🎉 You're All Set!

**To run your dashboard:**
1. Double-click `run.bat`
2. Wait for browser to open
3. Start managing vendors and projects!

**Enjoy your dashboard!** 📊

