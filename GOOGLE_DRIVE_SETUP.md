# Google Drive API Setup Guide

## Where to Find the Google Drive Automation

**Location:** Navigate to **"Project Coordination"** page in the dashboard

1. Open the dashboard (http://localhost:8501)
2. Click **"Project Coordination"** in the left sidebar
3. Scroll down to find **"🗂️ Google Drive Folder Automation"** section
4. Click to expand **"Create Google Drive Project Folder"**

---

## What It Does

This automation automatically creates an organized folder structure in your Google Drive for new projects:

```
📂 Project Name/
├── 📁 Contracts/
├── 📁 Deliverables/
├── 📁 Meeting Notes/
└── 📁 Documentation/
```

Perfect for organizing project files as mentioned in the HDO Operations Associate role requirements!

---

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"** (top left, project dropdown)
3. Name it: "Vendor Management Dashboard"
4. Click **"Create"**

### Step 2: Enable Google Drive API

1. In your new project, go to **"APIs & Services" > "Library"**
2. Search for **"Google Drive API"**
3. Click on it and press **"Enable"**

### Step 3: Create OAuth Credentials

1. Go to **"APIs & Services" > "Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. If prompted to configure consent screen:
   - Choose **"External"** user type
   - Fill in:
     - App name: `Vendor Management Dashboard`
     - User support email: Your email
     - Developer contact: Your email
   - Click **"Save and Continue"** (skip scopes and test users)
   - Click **"Back to Dashboard"**

5. Now create the credential:
   - Application type: **"Desktop app"**
   - Name: `Vendor Management Desktop`
   - Click **"Create"**

### Step 4: Download Credentials

1. After creating, a dialog shows your Client ID and Secret
2. Click **"DOWNLOAD JSON"**
3. **Important:** Rename the downloaded file to exactly: `credentials.json`
4. Move it to your project folder:
   ```
   C:\Users\Owner\vendor-management-dashboard\credentials.json
   ```

### Step 5: First-Time Authentication

1. Make sure `credentials.json` is in the project directory
2. Open the dashboard (http://localhost:8501)
3. Go to **Project Coordination** page
4. Expand **"Create Google Drive Project Folder"**
5. Enter a project name and click **"Create Google Drive Folder Structure"**
6. A browser window will open asking you to sign in to Google
7. Select your Google account
8. Click **"Allow"** to grant permissions
9. Done! A `token.pickle` file will be created for future use

---

## Using the Feature

Once set up, to create folders:

1. Go to **Project Coordination** page
2. Expand **"Create Google Drive Project Folder"**
3. Enter the project name
4. Optionally select an associated vendor
5. Click **"🚀 Create Google Drive Folder Structure"**
6. The folders will be created in your Google Drive
7. A link will be provided to access the main folder

---

## Troubleshooting

### "credentials.json not found"
**Solution:** Make sure the file is named exactly `credentials.json` (not `credentials(1).json` or `client_secret_*.json`) and is in the project root folder.

### "Access denied" or authentication fails
**Solution:** 
- Delete `token.pickle` if it exists
- Try authenticating again
- Make sure you're using the same Google account

### "Permission denied"
**Solution:** 
- Go back to Google Cloud Console
- Check that Google Drive API is enabled
- Verify OAuth consent screen is configured

### Folders not appearing in Drive
**Solution:**
- Check your Google Drive (drive.google.com)
- The folders appear in "My Drive" root
- Search for the project name if you can't find it

---

## Security Notes

✅ **Safe to use:**
- Uses OAuth 2.0 (industry standard)
- You control access permissions
- Only creates folders, doesn't access other files

❌ **Never commit to Git:**
- `credentials.json` - Your API credentials
- `token.pickle` - Your authentication token

These files are already in `.gitignore` for protection!

---

## Alternative: Manual Folder Creation

If you prefer not to set up the API, you can:
1. Manually create the folder structure in Google Drive
2. Copy the folder link
3. Add it to your project records manually

But the automation saves time and ensures consistency! 🚀

---

## Demo Without Setup

The feature shows a preview even without API setup:
- It displays what structure would be created
- Shows the setup instructions
- Demonstrates the capability for interviews

Perfect for showcasing in your portfolio!

---

## Questions?

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)

---

**Ready to automate your project organization!** 📁✨

