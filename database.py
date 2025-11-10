"""
Database module for vendor management dashboard.
Handles all data operations using SQLite.
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class Database:
    """Database handler for vendor management system."""
    
    def __init__(self, db_path: str = "vendor_management.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Vendors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_name TEXT,
                email TEXT,
                phone TEXT,
                location TEXT,
                status TEXT DEFAULT 'Pending',
                onboarding_date TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Contracts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                contract_name TEXT NOT NULL,
                contract_type TEXT,
                start_date TEXT,
                end_date TEXT,
                contract_value REAL,
                status TEXT DEFAULT 'Draft',
                po_number TEXT,
                document_link TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id)
            )
        """)
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                vendor_id INTEGER,
                status TEXT DEFAULT 'Green',
                start_date TEXT,
                target_date TEXT,
                completion_date TEXT,
                deliverables TEXT,
                drive_folder_id TEXT,
                drive_folder_link TEXT,
                project_owner TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # VENDOR OPERATIONS
    
    def add_vendor(self, name: str, contact_name: str = "", email: str = "", 
                   phone: str = "", location: str = "", status: str = "Pending", 
                   notes: str = "") -> int:
        """Add a new vendor."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        onboarding_date = datetime.now().strftime("%Y-%m-%d") if status != "Pending" else None
        
        cursor.execute("""
            INSERT INTO vendors (name, contact_name, email, phone, location, status, onboarding_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, contact_name, email, phone, location, status, onboarding_date, notes))
        
        vendor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vendor_id
    
    def get_vendors(self, status_filter: Optional[str] = None) -> pd.DataFrame:
        """Get all vendors or filtered by status."""
        conn = self.get_connection()
        
        if status_filter and status_filter != "All":
            query = "SELECT * FROM vendors WHERE status = ? ORDER BY created_at DESC"
            df = pd.read_sql_query(query, conn, params=(status_filter,))
        else:
            query = "SELECT * FROM vendors ORDER BY created_at DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def get_vendor_by_id(self, vendor_id: int) -> Optional[Dict]:
        """Get vendor by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors WHERE id = ?", (vendor_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_vendor(self, vendor_id: int, **kwargs):
        """Update vendor information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        
        fields.append("updated_at = ?")
        values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values.append(vendor_id)
        
        query = f"UPDATE vendors SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def delete_vendor(self, vendor_id: int):
        """Delete a vendor."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendors WHERE id = ?", (vendor_id,))
        conn.commit()
        conn.close()
    
    # CONTRACT OPERATIONS
    
    def add_contract(self, vendor_id: int, contract_name: str, contract_type: str = "",
                     start_date: str = "", end_date: str = "", contract_value: float = 0,
                     status: str = "Draft", po_number: str = "", document_link: str = "",
                     notes: str = "") -> int:
        """Add a new contract."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO contracts (vendor_id, contract_name, contract_type, start_date, 
                                 end_date, contract_value, status, po_number, document_link, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (vendor_id, contract_name, contract_type, start_date, end_date, 
              contract_value, status, po_number, document_link, notes))
        
        contract_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return contract_id
    
    def get_contracts(self, status_filter: Optional[str] = None) -> pd.DataFrame:
        """Get all contracts with vendor information."""
        conn = self.get_connection()
        
        query = """
            SELECT c.*, v.name as vendor_name
            FROM contracts c
            LEFT JOIN vendors v ON c.vendor_id = v.id
        """
        
        if status_filter and status_filter != "All":
            query += " WHERE c.status = ?"
            df = pd.read_sql_query(query + " ORDER BY c.created_at DESC", conn, params=(status_filter,))
        else:
            df = pd.read_sql_query(query + " ORDER BY c.created_at DESC", conn)
        
        conn.close()
        return df
    
    def get_contract_by_id(self, contract_id: int) -> Optional[Dict]:
        """Get contract by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_contract(self, contract_id: int, **kwargs):
        """Update contract information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        
        fields.append("updated_at = ?")
        values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values.append(contract_id)
        
        query = f"UPDATE contracts SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def delete_contract(self, contract_id: int):
        """Delete a contract."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
        conn.commit()
        conn.close()
    
    # PROJECT OPERATIONS
    
    def add_project(self, project_name: str, vendor_id: int = None, status: str = "Green",
                    start_date: str = "", target_date: str = "", deliverables: str = "",
                    project_owner: str = "", notes: str = "", 
                    drive_folder_id: str = "", drive_folder_link: str = "") -> int:
        """Add a new project."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO projects (project_name, vendor_id, status, start_date, target_date, 
                                deliverables, project_owner, notes, drive_folder_id, drive_folder_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_name, vendor_id, status, start_date, target_date, 
              deliverables, project_owner, notes, drive_folder_id, drive_folder_link))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def get_projects(self, status_filter: Optional[str] = None) -> pd.DataFrame:
        """Get all projects with vendor information."""
        conn = self.get_connection()
        
        query = """
            SELECT p.*, v.name as vendor_name
            FROM projects p
            LEFT JOIN vendors v ON p.vendor_id = v.id
        """
        
        if status_filter and status_filter != "All":
            query += " WHERE p.status = ?"
            df = pd.read_sql_query(query + " ORDER BY p.created_at DESC", conn, params=(status_filter,))
        else:
            df = pd.read_sql_query(query + " ORDER BY p.created_at DESC", conn)
        
        conn.close()
        return df
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        """Get project by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_project(self, project_id: int, **kwargs):
        """Update project information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        
        fields.append("updated_at = ?")
        values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values.append(project_id)
        
        query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def delete_project(self, project_id: int):
        """Delete a project."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
    
    # ANALYTICS OPERATIONS
    
    def get_dashboard_stats(self) -> Dict:
        """Get summary statistics for dashboard."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Vendor stats
        cursor.execute("SELECT COUNT(*) FROM vendors")
        stats['total_vendors'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vendors WHERE status = 'Active'")
        stats['active_vendors'] = cursor.fetchone()[0]
        
        # Contract stats
        cursor.execute("SELECT COUNT(*) FROM contracts")
        stats['total_contracts'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM contracts WHERE status = 'Active'")
        stats['active_contracts'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(contract_value) FROM contracts WHERE status = 'Active'")
        result = cursor.fetchone()[0]
        stats['total_contract_value'] = result if result else 0
        
        # Project stats
        cursor.execute("SELECT COUNT(*) FROM projects")
        stats['total_projects'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Green'")
        stats['green_projects'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Yellow'")
        stats['yellow_projects'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Red'")
        stats['red_projects'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def get_vendor_status_distribution(self) -> pd.DataFrame:
        """Get vendor status distribution."""
        conn = self.get_connection()
        query = "SELECT status, COUNT(*) as count FROM vendors GROUP BY status"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_contract_status_distribution(self) -> pd.DataFrame:
        """Get contract status distribution."""
        conn = self.get_connection()
        query = "SELECT status, COUNT(*) as count FROM contracts GROUP BY status"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_project_status_distribution(self) -> pd.DataFrame:
        """Get project status distribution."""
        conn = self.get_connection()
        query = "SELECT status, COUNT(*) as count FROM projects GROUP BY status"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def initialize_sample_data(self):
        """Initialize database with sample data for demonstration."""
        # Check if data already exists
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendors")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return  # Data already exists
        conn.close()
        
        # Add sample vendors
        vendor1 = self.add_vendor(
            name="TechSolutions Inc",
            contact_name="John Smith",
            email="john.smith@techsolutions.com",
            phone="555-0101",
            location="San Francisco, CA",
            status="Active",
            notes="Primary technology vendor"
        )
        
        vendor2 = self.add_vendor(
            name="DataPro Services",
            contact_name="Sarah Johnson",
            email="sarah.j@datapro.com",
            phone="555-0102",
            location="New York, NY",
            status="Active",
            notes="Data annotation specialist"
        )
        
        vendor3 = self.add_vendor(
            name="CloudOps Partners",
            contact_name="Mike Chen",
            email="mike.chen@cloudops.com",
            phone="555-0103",
            location="Seattle, WA",
            status="In Progress",
            notes="Cloud infrastructure support"
        )
        
        vendor4 = self.add_vendor(
            name="QA Experts LLC",
            contact_name="Emily Davis",
            email="emily@qaexperts.com",
            phone="555-0104",
            location="Austin, TX",
            status="Pending",
            notes="Quality assurance team"
        )
        
        # Add sample contracts
        self.add_contract(
            vendor_id=vendor1,
            contract_name="Annual Support Agreement",
            contract_type="Service Agreement",
            start_date="2024-01-01",
            end_date="2024-12-31",
            contract_value=150000,
            status="Active",
            po_number="PO-2024-001",
            notes="Covers technical support and maintenance"
        )
        
        self.add_contract(
            vendor_id=vendor2,
            contract_name="Data Labeling Services",
            contract_type="Statement of Work",
            start_date="2024-03-15",
            end_date="2024-09-15",
            contract_value=75000,
            status="Active",
            po_number="PO-2024-002",
            notes="Phase 1 data annotation project"
        )
        
        self.add_contract(
            vendor_id=vendor3,
            contract_name="Cloud Infrastructure",
            contract_type="Master Service Agreement",
            start_date="2024-06-01",
            end_date="2025-05-31",
            contract_value=200000,
            status="Pending Renewal",
            po_number="PO-2024-003"
        )
        
        # Add sample projects
        self.add_project(
            project_name="Q4 Data Collection Initiative",
            vendor_id=vendor2,
            status="Green",
            start_date="2024-10-01",
            target_date="2024-12-31",
            deliverables="10,000 labeled images, quality report",
            project_owner="Operations Team",
            notes="On track, weekly check-ins scheduled"
        )
        
        self.add_project(
            project_name="Infrastructure Migration",
            vendor_id=vendor3,
            status="Yellow",
            start_date="2024-09-01",
            target_date="2024-11-30",
            deliverables="Complete cloud migration, documentation",
            project_owner="IT Team",
            notes="Minor delays due to resource constraints"
        )
        
        self.add_project(
            project_name="Vendor Onboarding Automation",
            vendor_id=vendor1,
            status="Green",
            start_date="2024-11-01",
            target_date="2025-01-31",
            deliverables="Automated workflow system",
            project_owner="Operations Team",
            notes="Requirements gathering phase completed"
        )
        
        self.add_project(
            project_name="Quality Assurance Framework",
            vendor_id=vendor4,
            status="Red",
            start_date="2024-08-01",
            target_date="2024-10-31",
            deliverables="QA processes and documentation",
            project_owner="Quality Team",
            notes="Significant delays, needs immediate attention"
        )

