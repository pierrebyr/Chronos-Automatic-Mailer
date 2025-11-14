#!/usr/bin/env python3
"""
Web Styles - Modern design system for Chronos web interface
"""

def get_custom_css():
    """Return custom CSS for modern UI"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root Variables - Modern Color Palette */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --primary-light: #818CF8;
        --secondary: #10B981;
        --secondary-dark: #059669;
        --danger: #EF4444;
        --warning: #F59E0B;
        --info: #3B82F6;
        --success: #10B981;
        --background: #F9FAFB;
        --surface: #FFFFFF;
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --border: #E5E7EB;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .main {
        background-color: var(--background);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%);
        padding: 1rem 0;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #F9FAFB;
    }

    /* Navigation Buttons */
    .nav-button {
        background: transparent;
        color: #D1D5DB;
        border: none;
        padding: 0.75rem 1rem;
        text-align: left;
        width: 100%;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
        transition: all 0.2s;
        cursor: pointer;
        font-weight: 500;
    }

    .nav-button:hover {
        background: rgba(99, 102, 241, 0.1);
        color: var(--primary-light);
    }

    .nav-button.active {
        background: var(--primary);
        color: white;
    }

    /* Card Styling */
    .metric-card {
        background: var(--surface);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .metric-change.positive {
        color: var(--success);
    }

    .metric-change.negative {
        color: var(--danger);
    }

    /* Button Styles */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: var(--shadow);
    }

    .stButton > button:hover {
        background: var(--primary-dark);
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }

    .stButton > button[kind="secondary"] {
        background: white;
        color: var(--primary);
        border: 2px solid var(--primary);
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--primary);
        color: white;
    }

    /* Input Styles */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 1.5px solid var(--border);
        padding: 0.75rem;
        transition: all 0.2s;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    /* Table Styles */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    .dataframe thead tr th {
        background: var(--primary) !important;
        color: white !important;
        font-weight: 600;
        padding: 1rem !important;
    }

    .dataframe tbody tr:hover {
        background: rgba(99, 102, 241, 0.05);
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-prospect {
        background: #DBEAFE;
        color: #1E40AF;
    }

    .status-contacted {
        background: #FEF3C7;
        color: #92400E;
    }

    .status-lead {
        background: #D1FAE5;
        color: #065F46;
    }

    .status-client {
        background: #DDD6FE;
        color: #5B21B6;
    }

    /* Page Header */
    .page-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
    }

    .page-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }

    .page-subtitle {
        font-size: 1.125rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Activity Timeline */
    .timeline {
        position: relative;
        padding-left: 2rem;
    }

    .timeline::before {
        content: '';
        position: absolute;
        left: 0.5rem;
        top: 0;
        bottom: 0;
        width: 2px;
        background: var(--border);
    }

    .timeline-item {
        position: relative;
        padding-bottom: 1.5rem;
    }

    .timeline-marker {
        position: absolute;
        left: -1.5rem;
        width: 1rem;
        height: 1rem;
        border-radius: 50%;
        background: var(--primary);
        border: 3px solid white;
        box-shadow: var(--shadow);
    }

    .timeline-content {
        background: var(--surface);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }

    /* Progress Bar */
    .progress-bar {
        height: 0.5rem;
        background: var(--border);
        border-radius: 9999px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
        transition: width 0.3s ease;
    }

    /* Tags */
    .tag {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }

    /* Charts */
    .chart-container {
        background: var(--surface);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }

    /* Loading Spinner */
    @keyframes spin {
        to {transform: rotate(360deg);}
    }

    .spinner {
        border: 3px solid var(--border);
        border-top-color: var(--primary);
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        animation: spin 1s linear infinite;
    }

    /* Alerts */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
    }

    .alert-success {
        background: #D1FAE5;
        border-color: var(--success);
        color: #065F46;
    }

    .alert-warning {
        background: #FEF3C7;
        border-color: var(--warning);
        color: #92400E;
    }

    .alert-error {
        background: #FEE2E2;
        border-color: var(--danger);
        color: #991B1B;
    }

    .alert-info {
        background: #DBEAFE;
        border-color: var(--info);
        color: #1E40AF;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 2rem;
        }

        .page-title {
            font-size: 1.5rem;
        }
    }
    </style>
    """

def get_status_badge(status):
    """Generate HTML for status badge"""
    status_lower = status.lower()
    return f'<span class="status-badge status-{status_lower}">{status}</span>'

def get_metric_card(label, value, change=None, icon=None):
    """Generate HTML for metric card"""
    change_html = ""
    if change:
        change_class = "positive" if change >= 0 else "negative"
        change_symbol = "+" if change >= 0 else ""
        change_html = f'<div class="metric-change {change_class}">{change_symbol}{change}%</div>'

    icon_html = f'<div class="metric-icon">{icon}</div>' if icon else ""

    return f"""
    <div class="metric-card">
        {icon_html}
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """
