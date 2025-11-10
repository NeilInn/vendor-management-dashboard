import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Vendor Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Vendor & Project Management Dashboard"
    }
)

# Custom CSS for Dark Mode styling
st.markdown("""
    <style>
    /* Dark mode background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Sidebar dark mode */
    [data-testid="stSidebar"] {
        background-color: #1a1d24;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #58a6ff;
        margin-bottom: 0.5rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #1a1d24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #58a6ff;
    }
    
    /* Status colors */
    .status-active {
        color: #3fb950;
        font-weight: bold;
    }
    .status-onboarding {
        color: #d29922;
        font-weight: bold;
    }
    .status-inactive {
        color: #f85149;
        font-weight: bold;
    }
    
    /* Alert boxes */
    .alert-warning {
        background-color: #4d3800;
        border-left: 4px solid #d29922;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #ffd700;
    }
    .alert-danger {
        background-color: #4d1f1f;
        border-left: 4px solid #f85149;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #ff6b6b;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #1a1d24;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #238636;
        color: white;
        border: none;
    }
    .stButton button:hover {
        background-color: #2ea043;
    }
    
    /* Text and markdown */
    p, li, label {
        color: #c9d1d9 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #1a1d24;
        color: #fafafa;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #fafafa;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
def initialize_session_state():
    if 'vendors' not in st.session_state:
        st.session_state.vendors = create_sample_vendors()
    if 'contracts' not in st.session_state:
        st.session_state.contracts = create_sample_contracts()
    if 'projects' not in st.session_state:
        st.session_state.projects = create_sample_projects()
    if 'tickets' not in st.session_state:
        st.session_state.tickets = create_sample_tickets()

# Sample data generation functions
def create_sample_vendors():
    vendors = pd.DataFrame({
        'vendor_id': ['VND001', 'VND002', 'VND003', 'VND004', 'VND005', 'VND006', 'VND007', 'VND008'],
        'vendor_name': ['DataAnnotation Pro', 'CloudScale Solutions', 'TechVendor Inc', 'AI Training Partners', 
                       'Quality Data Services', 'Rapid Response Team', 'Global Workforce Co', 'Precision Labels Ltd'],
        'contact_name': ['Sarah Johnson', 'Michael Chen', 'Emily Rodriguez', 'David Kim', 
                        'Jessica Williams', 'Robert Taylor', 'Amanda Martinez', 'Chris Anderson'],
        'contact_email': ['sarah.j@dataannotation.com', 'mchen@cloudscale.com', 'emily.r@techvendor.com', 
                         'dkim@aitraining.com', 'jwilliams@qualitydata.com', 'rtaylor@rapidresponse.com',
                         'amartinez@globalworkforce.com', 'canderson@precisionlabels.com'],
        'location': ['San Francisco, CA', 'Austin, TX', 'New York, NY', 'Seattle, WA', 
                    'Remote (US)', 'Denver, CO', 'Remote (Global)', 'Boston, MA'],
        'vendor_type': ['Data Annotation', 'Infrastructure', 'Software', 'Software', 
                       'Infrastructure', 'Support Services', 'Staffing', 'Software'],
        'status': ['Active', 'Active', 'Onboarding', 'Active', 'Active', 'Onboarding', 'Active', 'Inactive'],
        'onboarding_stage': ['Completed', 'Completed', 'Access Provisioning', 'Completed', 
                            'Completed', 'Contract Review', 'Completed', 'N/A'],
        'date_added': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-10-28', '2024-03-10', 
                                     '2024-05-15', '2024-10-25', '2024-06-01', '2023-11-10']),
        'primary_services': ['Human feedback collection', 'Cloud infrastructure', 'Project management tools', 
                           'Dataset labeling', 'Quality assurance', 'Administrative support', 
                           'Contract staffing', 'Image annotation']
    })
    return vendors

def create_sample_contracts():
    contracts = pd.DataFrame({
        'contract_id': ['CNT001', 'CNT002', 'CNT003', 'CNT004', 'CNT005', 'CNT006', 'CNT007'],
        'vendor_id': ['VND001', 'VND002', 'VND003', 'VND004', 'VND005', 'VND007', 'VND008'],
        'contract_type': ['MSA', 'SOW', 'MSA', 'MSA', 'SOW', 'MSA', 'MSA'],
        'start_date': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-11-01', '2024-03-10', 
                                     '2024-05-15', '2024-06-01', '2023-11-10']),
        'end_date': pd.to_datetime(['2025-01-14', '2024-12-31', '2025-10-31', '2025-03-09', 
                                   '2024-11-30', '2025-05-31', '2024-11-09']),
        'contract_value': [250000, 120000, 85000, 180000, 45000, 200000, 95000],
        'po_number': ['PO-2024-001', 'PO-2024-015', 'PO-2024-089', 'PO-2024-023', 
                     'PO-2024-047', 'PO-2024-055', 'PO-2023-142'],
        'status': ['Active', 'Active', 'In Review', 'Active', 'Active', 'Active', 'Expired'],
        'renewal_notice_days': [60, 30, 90, 60, 30, 60, 0]
    })
    return contracts

def create_sample_projects():
    projects = pd.DataFrame({
        'project_id': ['PRJ001', 'PRJ002', 'PRJ003', 'PRJ004', 'PRJ005', 'PRJ006'],
        'project_name': ['Q4 Dataset Annotation', 'Infrastructure Migration', 'Model Feedback Collection', 
                        'Quality Audit Initiative', 'Emergency Support Coverage', 'Image Classification Project'],
        'vendor_id': ['VND001', 'VND002', 'VND004', 'VND005', 'VND006', 'VND008'],
        'status': ['In Progress', 'Completed', 'In Progress', 'Planning', 'Completed', 'In Progress'],
        'start_date': pd.to_datetime(['2024-10-01', '2024-08-15', '2024-09-20', '2024-11-05', 
                                     '2024-10-28', '2024-07-10']),
        'target_end_date': pd.to_datetime(['2024-12-31', '2024-10-30', '2024-11-30', '2024-12-15', 
                                          '2024-11-15', '2025-01-15']),
        'completion_pct': [65, 100, 45, 10, 80, 25],
        'budget': [150000, 120000, 95000, 35000, 25000, 85000],
        'project_lead': ['Internal Team A', 'Internal Team B', 'Internal Team A', 'Internal Team C', 
                        'Internal Team B', 'Internal Team A']
    })
    return projects

def create_sample_tickets():
    tickets = pd.DataFrame({
        'ticket_id': ['TKT001', 'TKT002', 'TKT003', 'TKT004', 'TKT005', 'TKT006', 'TKT007', 'TKT008', 'TKT009', 'TKT010', 'TKT011', 'TKT012'],
        'vendor_id': ['VND001', 'VND003', 'VND004', 'VND002', 'VND005', 'VND006', 'VND007', 'VND001', 'VND002', 'VND004', 'VND003', 'VND005'],
        'ticket_type': ['Access Request', 'Tooling Setup', 'Admin Support', 'Technical Issue', 
                       'Document Request', 'Access Request', 'Contract Question', 'Payment Query', 
                       'Tooling Setup', 'Access Request', 'Technical Issue', 'Document Request'],
        'priority': ['High', 'Medium', 'Low', 'High', 'Medium', 'High', 'Low', 'Medium', 'High', 'Medium', 'High', 'Low'],
        'status': ['In Progress', 'Open', 'Resolved', 'In Progress', 'Resolved', 'Open', 'Resolved', 'In Progress', 'Open', 'Resolved', 'In Progress', 'Open'],
        'created_date': pd.to_datetime(['2024-11-08', '2024-11-09', '2024-11-05', '2024-11-07', 
                                       '2024-11-04', '2024-11-09', '2024-11-01', '2024-11-08', 
                                       '2024-11-10', '2024-11-06', '2024-11-09', '2024-11-03']),
        'description': ['Need access to annotation platform', 'Setup project management tool access', 
                       'Update contact information', 'API integration not working', 
                       'Request W9 form', 'VPN access for remote team', 
                       'Question about renewal terms', 'Invoice processing delay',
                       'New tool integration needed', 'Quality metrics documentation', 
                       'Connection timeout issues', 'Additional contract documents needed']
    })
    return tickets

# Helper function to convert dataframe to CSV download
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Main application
def main():
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.markdown("### 📊 Vendor Management System")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard Overview", "Vendor Directory", "Contract Tracker", 
         "Project Coordination", "Ticket System", "Data Management"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Total Vendors", len(st.session_state.vendors))
    st.sidebar.metric("Active Contracts", len(st.session_state.contracts[st.session_state.contracts['status'] == 'Active']))
    st.sidebar.metric("Active Projects", len(st.session_state.projects[st.session_state.projects['status'] == 'In Progress']))
    st.sidebar.metric("Open Tickets", len(st.session_state.tickets[st.session_state.tickets['status'].isin(['Open', 'In Progress'])]))
    
    # Page routing
    if page == "Dashboard Overview":
        show_dashboard()
    elif page == "Vendor Directory":
        show_vendor_directory()
    elif page == "Contract Tracker":
        show_contract_tracker()
    elif page == "Project Coordination":
        show_project_coordination()
    elif page == "Ticket System":
        show_ticket_system()
    elif page == "Data Management":
        show_data_management()

def show_dashboard():
    st.markdown('<p class="main-header">Dashboard Overview</p>', unsafe_allow_html=True)
    st.markdown("**Comprehensive view of vendor operations and key metrics**")
    st.markdown("---")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    vendors_df = st.session_state.vendors
    contracts_df = st.session_state.contracts
    projects_df = st.session_state.projects
    tickets_df = st.session_state.tickets
    
    with col1:
        active_vendors = len(vendors_df[vendors_df['status'] == 'Active'])
        st.metric("Active Vendors", active_vendors, delta=f"{len(vendors_df[vendors_df['status'] == 'Onboarding'])} onboarding")
    
    with col2:
        active_contracts = len(contracts_df[contracts_df['status'] == 'Active'])
        expiring_soon = len(contracts_df[(contracts_df['end_date'] - datetime.now()) <= timedelta(days=30)])
        st.metric("Active Contracts", active_contracts, delta=f"-{expiring_soon} expiring soon", delta_color="inverse")
    
    with col3:
        active_projects = len(projects_df[projects_df['status'] == 'In Progress'])
        completed_projects = len(projects_df[projects_df['status'] == 'Completed'])
        st.metric("Active Projects", active_projects, delta=f"{completed_projects} completed")
    
    with col4:
        open_tickets = len(tickets_df[tickets_df['status'].isin(['Open', 'In Progress'])])
        high_priority = len(tickets_df[(tickets_df['status'].isin(['Open', 'In Progress'])) & (tickets_df['priority'] == 'High')])
        st.metric("Open Tickets", open_tickets, delta=f"{high_priority} high priority", delta_color="inverse")
    
    st.markdown("---")
    
    # Alerts Section
    st.subheader("🔔 Important Alerts")
    
    # Contract expiration alerts
    today = datetime.now()
    expiring_30 = contracts_df[(contracts_df['end_date'] - today <= timedelta(days=30)) & 
                                (contracts_df['end_date'] >= today) &
                                (contracts_df['status'] == 'Active')]
    expiring_60 = contracts_df[(contracts_df['end_date'] - today <= timedelta(days=60)) & 
                                (contracts_df['end_date'] - today > timedelta(days=30)) &
                                (contracts_df['status'] == 'Active')]
    
    if len(expiring_30) > 0:
        st.markdown(f'<div class="alert-danger">⚠️ <strong>{len(expiring_30)} contracts expiring within 30 days</strong></div>', 
                   unsafe_allow_html=True)
        for _, contract in expiring_30.iterrows():
            vendor_name = vendors_df[vendors_df['vendor_id'] == contract['vendor_id']]['vendor_name'].values[0]
            days_left = (contract['end_date'] - today).days
            st.warning(f"📄 {vendor_name} - Contract {contract['contract_id']} expires in {days_left} days ({contract['end_date'].strftime('%Y-%m-%d')})")
    
    if len(expiring_60) > 0:
        st.markdown(f'<div class="alert-warning">⚡ <strong>{len(expiring_60)} contracts expiring within 60 days</strong></div>', 
                   unsafe_allow_html=True)
    
    # High priority open tickets
    high_priority_tickets = tickets_df[(tickets_df['priority'] == 'High') & 
                                       (tickets_df['status'].isin(['Open', 'In Progress']))]
    if len(high_priority_tickets) > 0:
        st.markdown(f'<div class="alert-warning">🎫 <strong>{len(high_priority_tickets)} high priority tickets need attention</strong></div>', 
                   unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vendor Status Distribution")
        status_counts = vendors_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, 
                    color_discrete_sequence=['#28a745', '#ffc107', '#dc3545'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Vendor Types")
        type_counts = vendors_df['vendor_type'].value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values,
                    labels={'x': 'Vendor Type', 'y': 'Count'},
                    color=type_counts.values,
                    color_continuous_scale='Blues')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Status Overview")
        project_status = projects_df['status'].value_counts()
        fig = px.bar(x=project_status.index, y=project_status.values,
                    labels={'x': 'Status', 'y': 'Number of Projects'},
                    color=project_status.values,
                    color_continuous_scale='Viridis')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Ticket Priority Breakdown")
        ticket_priority = tickets_df[tickets_df['status'].isin(['Open', 'In Progress'])]['priority'].value_counts()
        colors = {'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
        fig = go.Figure(data=[go.Pie(labels=ticket_priority.index, values=ticket_priority.values,
                                     marker=dict(colors=[colors.get(x, '#1f77b4') for x in ticket_priority.index]))])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Contract Value Timeline
    st.subheader("Contract Timeline & Value")
    contracts_sorted = contracts_df[contracts_df['status'] == 'Active'].sort_values('end_date')
    fig = px.timeline(contracts_sorted, x_start='start_date', x_end='end_date', 
                     y='contract_id', color='contract_value',
                     labels={'contract_value': 'Contract Value ($)'},
                     color_continuous_scale='Blues')
    fig.update_yaxes(title='Contract ID')
    st.plotly_chart(fig, use_container_width=True)

def show_vendor_directory():
    st.markdown('<p class="main-header">Vendor Directory</p>', unsafe_allow_html=True)
    st.markdown("**Manage vendor profiles, contact information, and onboarding status**")
    st.markdown("---")
    
    vendors_df = st.session_state.vendors
    
    # Search and Filter Section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search vendors", placeholder="Search by name, contact, or location...")
    
    with col2:
        status_filter = st.multiselect("Filter by Status", 
                                       options=vendors_df['status'].unique(),
                                       default=vendors_df['status'].unique())
    
    with col3:
        type_filter = st.multiselect("Filter by Type", 
                                     options=vendors_df['vendor_type'].unique(),
                                     default=vendors_df['vendor_type'].unique())
    
    # Apply filters
    filtered_vendors = vendors_df[
        (vendors_df['status'].isin(status_filter)) &
        (vendors_df['vendor_type'].isin(type_filter))
    ]
    
    if search_term:
        filtered_vendors = filtered_vendors[
            filtered_vendors.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
        ]
    
    st.markdown(f"**Showing {len(filtered_vendors)} of {len(vendors_df)} vendors**")
    st.markdown("---")
    
    # Add New Vendor Section
    st.markdown("---")
    st.subheader("➕ Add New Vendor")
    
    with st.expander("Add New Vendor with Google Drive Integration"):
        with st.form("add_vendor_form"):
            st.markdown("**Vendor Information**")
            col1, col2 = st.columns(2)
            
            with col1:
                new_vendor_name = st.text_input("Vendor Name *", placeholder="e.g., DataPro Services")
                new_contact_name = st.text_input("Contact Name", placeholder="e.g., John Smith")
                new_email = st.text_input("Email", placeholder="contact@vendor.com")
                new_phone = st.text_input("Phone", placeholder="555-0100")
            
            with col2:
                new_location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
                new_vendor_type = st.selectbox("Vendor Type", 
                    ["Data Annotation", "Software", "Infrastructure", "Support Services", "Staffing", "Other"])
                new_status = st.selectbox("Status", ["Pending", "Onboarding", "Active", "Inactive"])
                new_services = st.text_input("Primary Services", placeholder="e.g., Data labeling, QA services")
            
            new_notes = st.text_area("Notes", placeholder="Additional information about the vendor...")
            
            # Google Drive Integration
            st.markdown("---")
            st.markdown("**🗂️ Google Drive Folder Creation**")
            create_gdrive_folder = st.checkbox("Create Google Drive folder for this vendor", value=True)
            
            if create_gdrive_folder:
                st.info("""
                📁 **This will create:**
                - Vendor Name/
                  - Contracts/
                  - Documents/
                  - Communications/
                  - Invoices/
                """)
            
            submitted = st.form_submit_button("Add Vendor", type="primary")
            
            if submitted:
                if new_vendor_name:
                    # Generate vendor ID
                    new_vendor_id = f"VND{len(vendors_df) + 1:03d}"
                    
                    # Create new vendor
                    new_vendor = pd.DataFrame({
                        'vendor_id': [new_vendor_id],
                        'vendor_name': [new_vendor_name],
                        'contact_name': [new_contact_name],
                        'contact_email': [new_email],
                        'location': [new_location],
                        'vendor_type': [new_vendor_type],
                        'status': [new_status],
                        'onboarding_stage': ['Contract Review' if new_status == 'Onboarding' else 'Completed' if new_status == 'Active' else 'Pending'],
                        'date_added': [pd.Timestamp.now()],
                        'primary_services': [new_services]
                    })
                    
                    # Add to session state
                    st.session_state.vendors = pd.concat([st.session_state.vendors, new_vendor], ignore_index=True)
                    
                    st.success(f"✅ Vendor '{new_vendor_name}' added successfully! (ID: {new_vendor_id})")
                    
                    # Create Google Drive folder if requested
                    if create_gdrive_folder:
                        st.markdown("---")
                        st.markdown("**📁 Google Drive Folder Creation**")
                        
                        # Check if google drive is configured
                        from google_drive import get_drive_manager
                        drive_manager = get_drive_manager()
                        
                        if drive_manager.is_configured():
                            with st.spinner("Creating Google Drive folder structure..."):
                                try:
                                    # Create vendor folder structure
                                    folder_result = drive_manager.create_project_folder_structure(
                                        new_vendor_name,
                                        parent_folder_id=None
                                    )
                                    
                                    if folder_result:
                                        st.success(f"✅ Google Drive folders created!")
                                        st.markdown(f"📂 [Open Vendor Folder]({folder_result['main_folder_link']})")
                                        
                                        # Show created subfolders
                                        st.markdown("**Created subfolders:**")
                                        for folder_name in folder_result['subfolders'].keys():
                                            st.markdown(f"  - ✅ {folder_name}/")
                                    else:
                                        st.warning("Could not create Google Drive folders. Please check your credentials.")
                                except Exception as e:
                                    st.error(f"Error creating folders: {str(e)}")
                        else:
                            st.warning("""
                            ⚠️ **Google Drive not configured**
                            
                            To enable folder creation:
                            1. Follow instructions in `GOOGLE_DRIVE_SETUP.md`
                            2. Add `credentials.json` to project directory
                            3. Authenticate on first use
                            
                            For now, you can manually create the folder structure in Google Drive.
                            """)
                    
                    st.balloons()
                    st.info("Refresh the page to see the new vendor in the list!")
                else:
                    st.error("❌ Please provide at least a vendor name.")
    
    st.markdown("---")
    
    # Display vendors
    for _, vendor in filtered_vendors.iterrows():
        with st.expander(f"**{vendor['vendor_name']}** - {vendor['vendor_id']} | Status: {vendor['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Contact Information**")
                st.write(f"👤 {vendor['contact_name']}")
                st.write(f"📧 {vendor['contact_email']}")
                st.write(f"📍 {vendor['location']}")
            
            with col2:
                st.markdown("**Vendor Details**")
                st.write(f"**Type:** {vendor['vendor_type']}")
                st.write(f"**Status:** {vendor['status']}")
                st.write(f"**Onboarding Stage:** {vendor['onboarding_stage']}")
            
            with col3:
                st.markdown("**Additional Info**")
                st.write(f"**Date Added:** {vendor['date_added'].strftime('%Y-%m-%d')}")
                st.write(f"**Services:** {vendor['primary_services']}")
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button(f"Edit", key=f"edit_{vendor['vendor_id']}"):
                    st.info("Edit functionality would open here")
            with col2:
                if st.button(f"View Contracts", key=f"contracts_{vendor['vendor_id']}"):
                    st.info("Contract details would display here")
    
    # Summary Statistics
    st.markdown("---")
    st.subheader("Vendor Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Vendors", len(filtered_vendors))
    with col2:
        st.metric("Active", len(filtered_vendors[filtered_vendors['status'] == 'Active']))
    with col3:
        st.metric("Onboarding", len(filtered_vendors[filtered_vendors['status'] == 'Onboarding']))
    with col4:
        st.metric("Inactive", len(filtered_vendors[filtered_vendors['status'] == 'Inactive']))

def show_contract_tracker():
    st.markdown('<p class="main-header">Contract & Agreement Tracker</p>', unsafe_allow_html=True)
    st.markdown("**Monitor contracts, purchase orders, and renewal timelines**")
    st.markdown("---")
    
    contracts_df = st.session_state.contracts
    vendors_df = st.session_state.vendors
    
    # Merge vendor names
    contracts_display = contracts_df.merge(vendors_df[['vendor_id', 'vendor_name']], on='vendor_id', how='left')
    
    # Filter Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect("Contract Status", 
                                       options=contracts_display['status'].unique(),
                                       default=['Active', 'In Review'])
    
    with col2:
        contract_type_filter = st.multiselect("Contract Type", 
                                              options=contracts_display['contract_type'].unique(),
                                              default=contracts_display['contract_type'].unique())
    
    with col3:
        days_to_expiry = st.slider("Days to Expiry", 0, 365, 365)
    
    # Apply filters
    today = datetime.now()
    filtered_contracts = contracts_display[
        (contracts_display['status'].isin(status_filter)) &
        (contracts_display['contract_type'].isin(contract_type_filter)) &
        ((contracts_display['end_date'] - today).dt.days <= days_to_expiry)
    ]
    
    st.markdown(f"**Showing {len(filtered_contracts)} contracts**")
    st.markdown("---")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_value = filtered_contracts['contract_value'].sum()
        st.metric("Total Contract Value", f"${total_value:,.0f}")
    
    with col2:
        active_count = len(filtered_contracts[filtered_contracts['status'] == 'Active'])
        st.metric("Active Contracts", active_count)
    
    with col3:
        expiring_30 = len(filtered_contracts[(filtered_contracts['end_date'] - today).dt.days <= 30])
        st.metric("Expiring in 30 Days", expiring_30, delta_color="inverse")
    
    with col4:
        expiring_60 = len(filtered_contracts[((filtered_contracts['end_date'] - today).dt.days <= 60) & 
                                            ((filtered_contracts['end_date'] - today).dt.days > 30)])
        st.metric("Expiring in 31-60 Days", expiring_60)
    
    st.markdown("---")
    
    # Contracts Table
    st.subheader("Contract Details")
    
    # Calculate days to expiry
    filtered_contracts['days_to_expiry'] = (filtered_contracts['end_date'] - today).dt.days
    
    # Display table
    display_cols = ['contract_id', 'vendor_name', 'contract_type', 'start_date', 'end_date', 
                   'days_to_expiry', 'contract_value', 'po_number', 'status']
    
    display_df = filtered_contracts[display_cols].copy()
    display_df['start_date'] = display_df['start_date'].dt.strftime('%Y-%m-%d')
    display_df['end_date'] = display_df['end_date'].dt.strftime('%Y-%m-%d')
    display_df['contract_value'] = display_df['contract_value'].apply(lambda x: f"${x:,.0f}")
    
    # Color code by days to expiry
    def highlight_expiry(row):
        if row['days_to_expiry'] < 0:
            return ['background-color: #f8d7da; color: #721c24'] * len(row)
        elif row['days_to_expiry'] <= 30:
            return ['background-color: #fff3cd; color: #856404'] * len(row)
        elif row['days_to_expiry'] <= 60:
            return ['background-color: #d1ecf1; color: #0c5460'] * len(row)
        return [''] * len(row)
    
    styled_df = display_df.style.apply(highlight_expiry, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Renewal Timeline Visualization
    st.subheader("Contract Renewal Timeline")
    
    # Simplified approach - build fresh timeline data
    timeline_data = []
    
    for _, contract in contracts_df.iterrows():
        if contract['status'] == 'Active':
            # Get vendor name
            vendor_match = vendors_df[vendors_df['vendor_id'] == contract['vendor_id']]
            if len(vendor_match) > 0:
                vendor_name = vendor_match.iloc[0]['vendor_name']
                
                # Check if it matches current filters
                if (contract['contract_type'] in contract_type_filter and
                    (contract['end_date'] - today).days <= days_to_expiry):
                    
                    timeline_data.append({
                        'contract_id': contract['contract_id'],
                        'vendor_name': vendor_name,
                        'start_date': contract['start_date'],
                        'end_date': contract['end_date'],
                        'contract_value': contract['contract_value'],
                        'renewal_notice_days': int(contract['renewal_notice_days'])
                    })
    
    if len(timeline_data) > 0:
        fig = go.Figure()
        
        for contract_info in timeline_data:
            # Calculate renewal date using timedelta
            from datetime import timedelta
            renewal_date = contract_info['end_date'] - timedelta(days=contract_info['renewal_notice_days'])
            
            # Contract period line
            fig.add_trace(go.Scatter(
                x=[contract_info['start_date'], contract_info['end_date']],
                y=[contract_info['vendor_name'], contract_info['vendor_name']],
                mode='lines',
                line=dict(color='royalblue', width=10),
                showlegend=False,
                hovertemplate=f"{contract_info['contract_id']}<br>Value: ${contract_info['contract_value']:,.0f}<extra></extra>"
            ))
            
            # Renewal notice marker
            fig.add_trace(go.Scatter(
                x=[renewal_date],
                y=[contract_info['vendor_name']],
                mode='markers',
                marker=dict(color='orange', size=12, symbol='diamond'),
                showlegend=False,
                hovertemplate=f"Renewal Notice<br>{contract_info['renewal_notice_days']} days before expiry<extra></extra>"
            ))
        
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Vendor",
            height=400,
            hovermode='closest',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No active contracts to display in timeline. Adjust filters to show active contracts.")
    
    # Add Contract Button
    st.markdown("---")
    if st.button("➕ Add New Contract"):
        st.info("Feature: Add new contract form would appear here")

def show_project_coordination():
    st.markdown('<p class="main-header">Project Coordination Dashboard</p>', unsafe_allow_html=True)
    st.markdown("**Track active projects, deliverables, and stakeholder assignments**")
    st.markdown("---")
    
    projects_df = st.session_state.projects
    vendors_df = st.session_state.vendors
    
    # Merge vendor names
    projects_display = projects_df.merge(vendors_df[['vendor_id', 'vendor_name']], on='vendor_id', how='left')
    
    # Filter Section
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.multiselect("Project Status", 
                                       options=projects_display['status'].unique(),
                                       default=projects_display['status'].unique())
    
    with col2:
        lead_filter = st.multiselect("Project Lead", 
                                     options=projects_display['project_lead'].unique(),
                                     default=projects_display['project_lead'].unique())
    
    filtered_projects = projects_display[
        (projects_display['status'].isin(status_filter)) &
        (projects_display['project_lead'].isin(lead_filter))
    ]
    
    st.markdown(f"**Showing {len(filtered_projects)} projects**")
    st.markdown("---")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_budget = filtered_projects['budget'].sum()
        st.metric("Total Budget", f"${total_budget:,.0f}")
    
    with col2:
        in_progress = len(filtered_projects[filtered_projects['status'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    
    with col3:
        completed = len(filtered_projects[filtered_projects['status'] == 'Completed'])
        st.metric("Completed", completed)
    
    with col4:
        avg_completion = filtered_projects['completion_pct'].mean()
        st.metric("Avg Completion", f"{avg_completion:.1f}%")
    
    st.markdown("---")
    
    # Project Cards
    st.subheader("Active Projects")
    
    for _, project in filtered_projects.iterrows():
        with st.expander(f"**{project['project_name']}** - {project['project_id']} | {project['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Project Details**")
                st.write(f"**Vendor:** {project['vendor_name']}")
                st.write(f"**Status:** {project['status']}")
                st.write(f"**Lead:** {project['project_lead']}")
            
            with col2:
                st.markdown("**Timeline**")
                st.write(f"**Start:** {project['start_date'].strftime('%Y-%m-%d')}")
                st.write(f"**Target End:** {project['target_end_date'].strftime('%Y-%m-%d')}")
                days_remaining = (project['target_end_date'] - datetime.now()).days
                st.write(f"**Days Remaining:** {days_remaining}")
            
            with col3:
                st.markdown("**Budget & Progress**")
                st.write(f"**Budget:** ${project['budget']:,.0f}")
                st.write(f"**Completion:** {project['completion_pct']}%")
            
            # Progress Bar
            st.progress(project['completion_pct'] / 100)
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("View Details", key=f"view_{project['project_id']}"):
                    st.info("Detailed project view would open here")
            with col2:
                if st.button("Update Status", key=f"update_{project['project_id']}"):
                    st.info("Status update form would appear here")
    
    st.markdown("---")
    
    # Google Drive Automation Section
    st.subheader("🗂️ Google Drive Folder Automation")
    st.markdown("**Automatically create organized folder structures for new projects**")
    
    with st.expander("Create Google Drive Project Folder"):
        st.info("📁 **Feature:** This creates a standardized folder structure in Google Drive for your project")
        st.markdown("""
        **Folder Structure Created:**
        - 📂 Project Name/
          - 📁 Contracts/
          - 📁 Deliverables/
          - 📁 Meeting Notes/
          - 📁 Documentation/
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            project_name_gdrive = st.text_input("Project Name", placeholder="e.g., Q4 Dataset Collection")
        with col2:
            vendor_select = st.selectbox("Associated Vendor", 
                                        options=[''] + list(vendors_df['vendor_name'].values),
                                        index=0)
        
        if st.button("🚀 Create Google Drive Folder Structure", type="primary"):
            if project_name_gdrive:
                st.success(f"✅ Folder structure would be created for: **{project_name_gdrive}**")
                st.markdown("""
                **Next Steps to Enable:**
                1. Set up Google Drive API credentials (see `GOOGLE_DRIVE_SETUP.md`)
                2. Place `credentials.json` in the project directory
                3. Run authentication flow on first use
                4. Folder links will be automatically added to project records
                """)
                st.code(f"""
# Folder structure that will be created:
📂 {project_name_gdrive}/
├── 📁 Contracts/
├── 📁 Deliverables/
├── 📁 Meeting Notes/
└── 📁 Documentation/
                """, language="text")
            else:
                st.warning("Please enter a project name")
    
    st.markdown("---")
    
    # Project Health Chart
    st.subheader("Project Completion Overview")
    
    fig = go.Figure()
    
    for _, project in filtered_projects.iterrows():
        color = 'green' if project['completion_pct'] >= 75 else 'orange' if project['completion_pct'] >= 50 else 'red'
        fig.add_trace(go.Bar(
            x=[project['completion_pct']],
            y=[project['project_name']],
            orientation='h',
            marker=dict(color=color),
            text=f"{project['completion_pct']}%",
            textposition='inside',
            showlegend=False,
            hovertemplate=f"{project['project_name']}<br>Completion: {project['completion_pct']}%<br>Budget: ${project['budget']:,.0f}<extra></extra>"
        ))
    
    fig.update_layout(
        xaxis_title="Completion %",
        yaxis_title="Project",
        height=400,
        xaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Budget Allocation
    st.subheader("Budget Allocation by Status")
    
    budget_by_status = filtered_projects.groupby('status')['budget'].sum().reset_index()
    fig = px.pie(budget_by_status, values='budget', names='status',
                title='Budget Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Add Project Button
    st.markdown("---")
    if st.button("➕ Add New Project"):
        st.info("Feature: Add new project form would appear here")

def show_ticket_system():
    st.markdown('<p class="main-header">Ticket & Issue Tracker</p>', unsafe_allow_html=True)
    st.markdown("**Log and track vendor requests, issues, and support tickets**")
    st.markdown("---")
    
    tickets_df = st.session_state.tickets
    vendors_df = st.session_state.vendors
    
    # Merge vendor names
    tickets_display = tickets_df.merge(vendors_df[['vendor_id', 'vendor_name']], on='vendor_id', how='left')
    
    # Filter Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.multiselect("Status", 
                                       options=tickets_display['status'].unique(),
                                       default=['Open', 'In Progress'])
    
    with col2:
        priority_filter = st.multiselect("Priority", 
                                         options=tickets_display['priority'].unique(),
                                         default=tickets_display['priority'].unique())
    
    with col3:
        type_filter = st.multiselect("Type", 
                                     options=tickets_display['ticket_type'].unique(),
                                     default=tickets_display['ticket_type'].unique())
    
    with col4:
        date_range = st.selectbox("Date Range", 
                                 ["All", "Last 7 Days", "Last 30 Days", "Last 90 Days"])
    
    # Apply filters
    filtered_tickets = tickets_display[
        (tickets_display['status'].isin(status_filter)) &
        (tickets_display['priority'].isin(priority_filter)) &
        (tickets_display['ticket_type'].isin(type_filter))
    ]
    
    if date_range == "Last 7 Days":
        filtered_tickets = filtered_tickets[filtered_tickets['created_date'] >= datetime.now() - timedelta(days=7)]
    elif date_range == "Last 30 Days":
        filtered_tickets = filtered_tickets[filtered_tickets['created_date'] >= datetime.now() - timedelta(days=30)]
    elif date_range == "Last 90 Days":
        filtered_tickets = filtered_tickets[filtered_tickets['created_date'] >= datetime.now() - timedelta(days=90)]
    
    st.markdown(f"**Showing {len(filtered_tickets)} tickets**")
    st.markdown("---")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tickets = len(filtered_tickets)
        st.metric("Total Tickets", total_tickets)
    
    with col2:
        open_tickets = len(filtered_tickets[filtered_tickets['status'] == 'Open'])
        st.metric("Open", open_tickets, delta_color="inverse")
    
    with col3:
        in_progress_tickets = len(filtered_tickets[filtered_tickets['status'] == 'In Progress'])
        st.metric("In Progress", in_progress_tickets)
    
    with col4:
        high_priority = len(filtered_tickets[filtered_tickets['priority'] == 'High'])
        st.metric("High Priority", high_priority, delta_color="inverse")
    
    st.markdown("---")
    
    # Add New Ticket Button
    if st.button("➕ Create New Ticket"):
        st.info("Feature: New ticket form would appear here")
    
    st.markdown("###")
    
    # Tickets List
    st.subheader("Ticket List")
    
    # Sort by priority and date
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    filtered_tickets['priority_rank'] = filtered_tickets['priority'].map(priority_order)
    filtered_tickets_sorted = filtered_tickets.sort_values(['priority_rank', 'created_date'], ascending=[True, False])
    
    for _, ticket in filtered_tickets_sorted.iterrows():
        # Priority color coding
        if ticket['priority'] == 'High':
            priority_color = "🔴"
        elif ticket['priority'] == 'Medium':
            priority_color = "🟡"
        else:
            priority_color = "🟢"
        
        # Status badge
        status_emoji = "⏳" if ticket['status'] == 'In Progress' else "📋" if ticket['status'] == 'Open' else "✅"
        
        with st.expander(f"{priority_color} {status_emoji} **{ticket['ticket_id']}** - {ticket['ticket_type']} | {ticket['vendor_name']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Ticket Details**")
                st.write(f"**ID:** {ticket['ticket_id']}")
                st.write(f"**Type:** {ticket['ticket_type']}")
                st.write(f"**Priority:** {ticket['priority']}")
            
            with col2:
                st.markdown("**Vendor & Status**")
                st.write(f"**Vendor:** {ticket['vendor_name']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Created:** {ticket['created_date'].strftime('%Y-%m-%d')}")
            
            with col3:
                st.markdown("**Description**")
                st.write(ticket['description'])
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("Update", key=f"update_{ticket['ticket_id']}"):
                    st.info("Update ticket form would appear here")
            with col2:
                if st.button("Resolve", key=f"resolve_{ticket['ticket_id']}"):
                    st.success("Ticket marked as resolved")
    
    st.markdown("---")
    
    # Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets by Type")
        type_counts = filtered_tickets['ticket_type'].value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values,
                    labels={'x': 'Ticket Type', 'y': 'Count'},
                    color=type_counts.values,
                    color_continuous_scale='Reds')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Tickets by Status")
        status_counts = filtered_tickets['status'].value_counts()
        colors_map = {'Open': '#ffc107', 'In Progress': '#17a2b8', 'Resolved': '#28a745'}
        fig = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values,
                                     marker=dict(colors=[colors_map.get(x, '#1f77b4') for x in status_counts.index]))])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

def show_data_management():
    st.markdown('<p class="main-header">Data Management</p>', unsafe_allow_html=True)
    st.markdown("**Import, export, and manage system data**")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📤 Export Data", "📥 Import Data", "📊 Data Overview"])
    
    with tab1:
        st.subheader("Export Data to CSV")
        st.markdown("Download current data for backup or external analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Vendors")
            csv_vendors = convert_df_to_csv(st.session_state.vendors)
            st.download_button(
                label="⬇️ Download Vendors CSV",
                data=csv_vendors,
                file_name=f"vendors_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption(f"📊 {len(st.session_state.vendors)} records")
            
            st.markdown("### Projects")
            csv_projects = convert_df_to_csv(st.session_state.projects)
            st.download_button(
                label="⬇️ Download Projects CSV",
                data=csv_projects,
                file_name=f"projects_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption(f"📊 {len(st.session_state.projects)} records")
        
        with col2:
            st.markdown("### Contracts")
            csv_contracts = convert_df_to_csv(st.session_state.contracts)
            st.download_button(
                label="⬇️ Download Contracts CSV",
                data=csv_contracts,
                file_name=f"contracts_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption(f"📊 {len(st.session_state.contracts)} records")
            
            st.markdown("### Tickets")
            csv_tickets = convert_df_to_csv(st.session_state.tickets)
            st.download_button(
                label="⬇️ Download Tickets CSV",
                data=csv_tickets,
                file_name=f"tickets_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption(f"📊 {len(st.session_state.tickets)} records")
    
    with tab2:
        st.subheader("Import Data from CSV")
        st.markdown("Upload CSV files to update system data")
        st.warning("⚠️ Note: This is a demo feature. In production, implement proper validation and backup procedures.")
        
        data_type = st.selectbox("Select Data Type", ["Vendors", "Contracts", "Projects", "Tickets"])
        
        uploaded_file = st.file_uploader(f"Upload {data_type} CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! Found {len(df)} records.")
                
                st.markdown("### Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                if st.button("Import Data"):
                    st.success(f"✅ {len(df)} {data_type.lower()} records imported successfully!")
                    st.info("Note: In production, this would validate and merge with existing data.")
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
    
    with tab3:
        st.subheader("Data Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Database Statistics")
            st.metric("Total Vendors", len(st.session_state.vendors))
            st.metric("Total Contracts", len(st.session_state.contracts))
            st.metric("Total Projects", len(st.session_state.projects))
            st.metric("Total Tickets", len(st.session_state.tickets))
        
        with col2:
            st.markdown("### Data Quality")
            vendors_complete = len(st.session_state.vendors[st.session_state.vendors['status'] != ''])
            vendors_pct = (vendors_complete / len(st.session_state.vendors)) * 100
            st.metric("Vendor Records Complete", f"{vendors_pct:.1f}%")
            
            active_contracts = len(st.session_state.contracts[st.session_state.contracts['status'] == 'Active'])
            contracts_pct = (active_contracts / len(st.session_state.contracts)) * 100
            st.metric("Active Contracts", f"{contracts_pct:.1f}%")
        
        st.markdown("---")
        
        st.subheader("Sample Data")
        st.markdown("**Vendor Table Preview**")
        st.dataframe(st.session_state.vendors.head(), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()

