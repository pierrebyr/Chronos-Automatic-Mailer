#!/usr/bin/env python3
"""
Chronos Outreach Web App - Modern Interface
Main application entry point
"""

import streamlit as st
import json
from pathlib import Path

# Import modules
from main import ChronosSystem, setup_logging
from web_styles import get_custom_css
import logging

# Import pages
from pages import (
    dashboard,
    research,
    prospects,
    email_sequences,
    send_emails,
    history,
    analytics,
    settings
)


def init_session_state():
    """Initialize session state variables"""
    if 'system' not in st.session_state:
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            st.session_state.system = ChronosSystem(config)
        except FileNotFoundError:
            st.error("❌ Configuration not found. Please run setup first.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading system: {e}")
            st.stop()

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'


def render_sidebar():
    """Render modern sidebar navigation"""
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem 0;'>
                <h1 style='color: white; font-size: 1.75rem; margin: 0;'>📧 Chronos</h1>
                <p style='color: #9CA3AF; font-size: 0.875rem; margin-top: 0.5rem;'>Outreach System</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation menu
        pages = {
            '🏠 Dashboard': 'Dashboard',
            '🔍 Research': 'Research',
            '👥 Prospects': 'Prospects',
            '📝 Email Sequences': 'Email Sequences',
            '📤 Send Emails': 'Send Emails',
            '📊 Analytics': 'Analytics',
            '⏱️ History': 'History',
            '⚙️ Settings': 'Settings'
        }

        for label, page_name in pages.items():
            if st.button(
                label,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_name else "secondary"
            ):
                st.session_state.current_page = page_name
                st.rerun()

        st.markdown("---")

        # Quick stats in sidebar
        try:
            stats = st.session_state.system.db.get_dashboard_metrics()
            st.markdown(f"""
                <div style='color: #9CA3AF; padding: 1rem 0; font-size: 0.875rem;'>
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='color: #6B7280;'>Total Prospects</div>
                        <div style='color: white; font-size: 1.5rem; font-weight: 700;'>{stats['total_prospects']}</div>
                    </div>
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='color: #6B7280;'>Emails Sent</div>
                        <div style='color: white; font-size: 1.5rem; font-weight: 700;'>{stats['emails_sent']}</div>
                    </div>
                    <div>
                        <div style='color: #6B7280;'>Today</div>
                        <div style='color: #10B981; font-size: 1.25rem; font-weight: 700;'>{stats['emails_sent_today']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        except:
            pass


def main():
    """Main application"""
    # Page config
    st.set_page_config(
        page_title="Chronos Outreach System",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Setup logging
    setup_logging()

    # Inject custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Initialize
    init_session_state()

    # Render sidebar
    render_sidebar()

    # Render current page
    current_page = st.session_state.current_page
    system = st.session_state.system

    if current_page == 'Dashboard':
        dashboard.render(system)
    elif current_page == 'Research':
        research.render(system)
    elif current_page == 'Prospects':
        prospects.render(system)
    elif current_page == 'Email Sequences':
        email_sequences.render(system)
    elif current_page == 'Send Emails':
        send_emails.render(system)
    elif current_page == 'Analytics':
        analytics.render(system)
    elif current_page == 'History':
        history.render(system)
    elif current_page == 'Settings':
        settings.render(system)


if __name__ == '__main__':
    main()
