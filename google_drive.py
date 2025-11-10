"""
Google Drive API integration for automatic folder creation.
"""

import os
import pickle
from typing import Optional, Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveManager:
    """Manages Google Drive folder creation and organization."""
    
    def __init__(self):
        """Initialize Google Drive manager."""
        self.creds = None
        self.service = None
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Drive API.
        Returns True if authentication successful, False otherwise.
        """
        try:
            # The file token.pickle stores the user's access and refresh tokens
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            
            # If there are no (valid) credentials available, let the user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    # Check if credentials.json exists
                    if not os.path.exists('credentials.json'):
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)
            
            # Build the service
            self.service = build('drive', 'v3', credentials=self.creds)
            self.authenticated = True
            return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> Optional[Dict]:
        """
        Create a folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_folder_id: ID of the parent folder (optional)
        
        Returns:
            Dictionary with folder_id and folder_link, or None if failed
        """
        if not self.authenticated:
            if not self.authenticate():
                return None
        
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, webViewLink'
            ).execute()
            
            return {
                'folder_id': folder.get('id'),
                'folder_link': folder.get('webViewLink')
            }
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def create_project_folder_structure(self, project_name: str, 
                                       parent_folder_id: Optional[str] = None) -> Optional[Dict]:
        """
        Create a complete folder structure for a new project.
        
        Structure:
        - Project Name/
          - Contracts/
          - Deliverables/
          - Meeting Notes/
          - Documentation/
        
        Args:
            project_name: Name of the project
            parent_folder_id: ID of parent folder (optional)
        
        Returns:
            Dictionary with main folder info and subfolders, or None if failed
        """
        if not self.authenticated:
            if not self.authenticate():
                return None
        
        try:
            # Create main project folder
            main_folder = self.create_folder(project_name, parent_folder_id)
            
            if not main_folder:
                return None
            
            main_folder_id = main_folder['folder_id']
            
            # Create subfolders
            subfolders = ['Contracts', 'Deliverables', 'Meeting Notes', 'Documentation']
            subfolder_info = {}
            
            for subfolder_name in subfolders:
                subfolder = self.create_folder(subfolder_name, main_folder_id)
                if subfolder:
                    subfolder_info[subfolder_name] = subfolder
            
            return {
                'main_folder_id': main_folder_id,
                'main_folder_link': main_folder['folder_link'],
                'subfolders': subfolder_info
            }
            
        except Exception as e:
            print(f"Error creating project structure: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Check if Google Drive API is properly configured."""
        return os.path.exists('credentials.json')
    
    def get_folder_link(self, folder_id: str) -> str:
        """Generate a Google Drive folder link from folder ID."""
        return f"https://drive.google.com/drive/folders/{folder_id}"


# Singleton instance
_drive_manager = None


def get_drive_manager() -> GoogleDriveManager:
    """Get or create the GoogleDriveManager singleton instance."""
    global _drive_manager
    if _drive_manager is None:
        _drive_manager = GoogleDriveManager()
    return _drive_manager

