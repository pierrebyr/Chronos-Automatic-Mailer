"""
Settings Page - System configuration
"""

import streamlit as st
import json


def render(system):
    """Render settings page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">⚙️ Settings</h1>
            <p class="page-subtitle">Configure your outreach system</p>
        </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🔑 API Keys", "📧 Sender Info", "📊 System Info", "🗄️ Database"])

    # API Keys tab
    with tabs[0]:
        st.markdown("### 🔑 API Configuration")
        st.info("💡 For security, use environment variables (.env file) instead of storing keys in config.json")

        with st.form("api_keys_form"):
            anthropic_key = st.text_input(
                "Anthropic API Key",
                value=system.config.get('anthropic_api_key', ''),
                type="password",
                help="Your Anthropic API key for Claude AI"
            )

            brave_key = st.text_input(
                "Brave Search API Key",
                value=system.config.get('brave_api_key', ''),
                type="password",
                help="Your Brave Search API key (optional)"
            )

            if st.form_submit_button("💾 Save API Keys", type="primary"):
                try:
                    # Load current config
                    with open('config.json', 'r') as f:
                        config = json.load(f)

                    # Update keys
                    config['anthropic_api_key'] = anthropic_key
                    config['brave_api_key'] = brave_key

                    # Save
                    with open('config.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    st.success("✅ API keys updated successfully!")
                    st.info("🔄 Restart the application for changes to take effect")

                except Exception as e:
                    st.error(f"❌ Failed to save: {e}")

    # Sender Info tab
    with tabs[1]:
        st.markdown("### 📧 Sender Information")
        st.info("This information will be used in email signatures")

        with st.form("sender_info_form"):
            col1, col2 = st.columns(2)

            with col1:
                sender_name = st.text_input(
                    "Your Name",
                    value=system.config.get('sender_name', '')
                )

                sender_email = st.text_input(
                    "Your Email",
                    value=system.config.get('sender_email', '')
                )

            with col2:
                sender_phone = st.text_input(
                    "Your Phone",
                    value=system.config.get('sender_phone', '')
                )

                sender_website = st.text_input(
                    "Your Website",
                    value=system.config.get('sender_website', '')
                )

            if st.form_submit_button("💾 Save Sender Info", type="primary"):
                try:
                    with open('config.json', 'r') as f:
                        config = json.load(f)

                    config['sender_name'] = sender_name
                    config['sender_email'] = sender_email
                    config['sender_phone'] = sender_phone
                    config['sender_website'] = sender_website

                    with open('config.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    st.success("✅ Sender information updated!")
                    st.info("🔄 Restart the application for changes to take effect")

                except Exception as e:
                    st.error(f"❌ Failed to save: {e}")

    # System Info tab
    with tabs[2]:
        st.markdown("### 📊 System Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🗂️ Files")
            import os
            st.write(f"**Config:** `{os.path.abspath('config.json')}`")
            st.write(f"**Database:** `{os.path.abspath(system.config['database_path'])}`")

            if os.path.exists('.env'):
                st.write(f"**Environment:** `.env` ✅")
            else:
                st.write(f"**Environment:** `.env` ❌ (not found)")

        with col2:
            st.markdown("#### 📦 Loaded Configuration")
            config_display = {
                k: v if k not in ['anthropic_api_key', 'brave_api_key'] else '***hidden***'
                for k, v in system.config.items()
                if k not in ['gmail_credentials_path', 'smtp']
            }
            st.json(config_display)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📚 Documentation")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("[📖 README](README.md)")
        with col2:
            st.markdown("[🚀 Quick Start](QUICKSTART.md)")
        with col3:
            st.markdown("[🏗️ Architecture](ARCHITECTURE.md)")

    # Database tab
    with tabs[3]:
        st.markdown("### 🗄️ Database Management")

        metrics = system.db.get_dashboard_metrics()

        st.markdown("#### 📊 Database Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Prospects", metrics['total_prospects'])
        with col2:
            st.metric("Email Sequences", metrics['with_sequences'])
        with col3:
            st.metric("Emails Sent", metrics['emails_sent'])
        with col4:
            activities = system.db.get_recent_activities(limit=1000)
            st.metric("Activities", len(activities))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ⚠️ Danger Zone")

        st.warning("🚨 These actions cannot be undone!")

        if st.button("🗑️ Clear All Activity Logs", type="secondary"):
            if st.checkbox("I understand this will delete all activity history"):
                # Note: You'd need to add a method to clear activities in database.py
                st.error("Not implemented - add clear_activities() method to database.py")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📥 Export Database", type="primary"):
            st.info("Database export feature - coming soon!")
            st.code(f"Database location: {system.config['database_path']}", language="bash")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #6B7280; padding: 2rem;">
                <h3>Chronos Outreach System</h3>
                <p>Version 1.0.0 | Built with ❤️ and AI</p>
            </div>
        """, unsafe_allow_html=True)
