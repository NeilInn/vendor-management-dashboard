# Vendor Management Dashboard

A comprehensive vendor lifecycle management system built with Python and Streamlit.

## Features

- **Vendor Directory**: Complete vendor profile management with contact information, locations, and onboarding status tracking
- **Contract Tracker**: Monitor contracts, purchase orders, expiration dates, and renewal alerts
- **Project Coordination**: Track active projects, deliverables, and stakeholder assignments
- **Metrics & KPIs**: Visual analytics for vendor operations and project health
- **Ticket System**: Log and track vendor requests and issues
- **Data Management**: Import/export CSV data for seamless integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vendor-management-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

The dashboard includes sample demo data to showcase functionality. You can:
- Add, edit, and search vendors
- Track contract lifecycles and renewals
- Manage projects and deliverables
- Monitor key operational metrics
- Export data to CSV for reporting

## Technology Stack

- **Python 3.8+**
- **Streamlit**: Interactive web dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical operations

## Project Structure

```
vendor-management-dashboard/
├── app.py                 # Main Streamlit application
├── data/                  # Sample data files
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Future Enhancements

- Google Drive API integration for automated folder creation
- Email notifications for contract renewals
- Advanced analytics and reporting
- User authentication and role-based access

