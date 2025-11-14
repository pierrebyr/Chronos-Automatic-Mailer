#!/usr/bin/env python3
"""
Web Interface - Streamlit app for reviewing and sending emails
"""

import streamlit as st
import pandas as pd
from datetime import datetime


def launch_app(system):
    """Launch the Streamlit web interface"""
    st.set_page_config(
        page_title="Chronos Outreach System",
        page_icon="📧",
        layout="wide"
    )
    
    # Sidebar navigation
    st.sidebar.title("📧 Chronos Outreach")
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Prospects", "Email Sequences", "Send Emails"]
    )
    
    if page == "Dashboard":
        show_dashboard(system)
    elif page == "Prospects":
        show_prospects(system)
    elif page == "Email Sequences":
        show_email_sequences(system)
    elif page == "Send Emails":
        show_send_emails(system)


def show_dashboard(system):
    """Show dashboard with statistics"""
    st.title("📊 Dashboard")
    
    stats = system.get_statistics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Prospects", stats['total_prospects'])
    
    with col2:
        st.metric("With Email Sequences", stats['with_sequences'])
    
    with col3:
        st.metric("Emails Sent", stats['emails_sent'])
    
    with col4:
        st.metric("Categories", len(stats['categories']))
    
    st.markdown("---")
    
    # Status breakdown
    st.subheader("Prospects by Status")
    col1, col2 = st.columns(2)
    
    with col1:
        status_df = pd.DataFrame([
            {"Status": k, "Count": v} 
            for k, v in stats.get('status_counts', {}).items()
        ])
        if not status_df.empty:
            st.bar_chart(status_df.set_index('Status'))
    
    with col2:
        st.subheader("Categories")
        for category in stats['categories']:
            st.write(f"• {category}")
    
    # Quick actions
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Research New Category"):
            st.session_state['show_research_form'] = True
    
    with col2:
        if st.button("✉️ Generate Email Sequences"):
            prospects_without = system.db.get_prospects_without_emails()
            if prospects_without:
                with st.spinner(f"Generating sequences for {len(prospects_without)} prospects..."):
                    system.generate_email_sequences()
                st.success(f"✓ Generated sequences for {len(prospects_without)} prospects")
            else:
                st.info("All prospects already have email sequences")
    
    with col3:
        if st.button("📊 Refresh Stats"):
            st.rerun()
    
    # Research form
    if st.session_state.get('show_research_form', False):
        st.markdown("---")
        st.subheader("Research New Category")
        
        with st.form("research_form"):
            category = st.text_input("Category (e.g., 'Irish Whiskey', 'Premium Gin')")
            limit = st.number_input("Number of brands to research", min_value=5, max_value=50, value=20)
            
            if st.form_submit_button("Start Research"):
                if category:
                    with st.spinner(f"Researching {category} brands..."):
                        brands = system.research_category(category, limit)
                    st.success(f"✓ Found and saved {len(brands)} brands")
                    st.session_state['show_research_form'] = False
                    st.rerun()


def show_prospects(system):
    """Show all prospects with filtering and editing"""
    st.title("👥 Prospects")
    
    prospects = system.db.get_all_prospects()
    
    if not prospects:
        st.info("No prospects yet. Use the Research feature to add some!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = list(set(p['category'] for p in prospects if p['category']))
        selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    with col2:
        statuses = list(set(p['status'] for p in prospects))
        selected_status = st.selectbox("Filter by Status", ["All"] + statuses)
    
    with col3:
        search = st.text_input("Search", placeholder="Company name...")
    
    # Filter prospects
    filtered = prospects
    if selected_category != "All":
        filtered = [p for p in filtered if p['category'] == selected_category]
    if selected_status != "All":
        filtered = [p for p in filtered if p['status'] == selected_status]
    if search:
        filtered = [p for p in filtered if search.lower() in p['company'].lower()]
    
    st.write(f"Showing {len(filtered)} of {len(prospects)} prospects")
    
    # Display prospects
    for prospect in filtered:
        with st.expander(f"**{prospect['company']}** - {prospect['sector']} ({prospect['status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Email:** {prospect['email']}")
                st.write(f"**Website:** {prospect['website']}")
                st.write(f"**Category:** {prospect['category']}")
                st.write(f"**Added:** {prospect['created_at']}")
            
            with col2:
                st.write(f"**Products:**")
                for product in prospect['products'][:5]:
                    st.write(f"• {product}")
                
                if prospect['description']:
                    st.write(f"**Description:** {prospect['description']}")
            
            # Actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_status = st.selectbox(
                    "Status",
                    ["prospect", "contacted", "lead", "client"],
                    index=["prospect", "contacted", "lead", "client"].index(prospect['status']),
                    key=f"status_{prospect['id']}"
                )
                if new_status != prospect['status']:
                    system.db.update_prospect_status(prospect['id'], new_status)
                    st.success("Status updated!")
                    st.rerun()
            
            with col2:
                if st.button("View Emails", key=f"view_{prospect['id']}"):
                    st.session_state['selected_prospect'] = prospect['id']
                    st.session_state['page'] = 'Email Sequences'
                    st.rerun()


def show_email_sequences(system):
    """Show email sequences with preview and editing"""
    st.title("✉️ Email Sequences")
    
    prospects = system.db.get_all_prospects()
    
    if not prospects:
        st.info("No prospects yet.")
        return
    
    # Select prospect
    prospect_options = {p['id']: f"{p['company']} ({p['sector']})" for p in prospects}
    
    selected_id = st.selectbox(
        "Select Prospect",
        options=list(prospect_options.keys()),
        format_func=lambda x: prospect_options[x],
        index=0 if 'selected_prospect' not in st.session_state else 
              list(prospect_options.keys()).index(st.session_state['selected_prospect'])
    )
    
    prospect = system.db.get_prospect(selected_id)
    emails = system.db.get_all_email_sequences(selected_id)
    
    if not emails:
        st.warning("No email sequence generated for this prospect yet.")
        if st.button("Generate Email Sequence"):
            with st.spinner("Generating personalized emails..."):
                system.generate_email_sequences(prospect_ids=[selected_id])
            st.success("✓ Email sequence generated!")
            st.rerun()
        return
    
    # Display emails
    st.subheader(f"Email Sequence for {prospect['company']}")
    
    for email in emails:
        email_num = email['email_number']
        is_sent = system.db.get_email_status(selected_id, email_num)
        
        status_icon = "✅" if is_sent else "📧"
        status_text = "SENT" if is_sent else "NOT SENT"
        
        with st.expander(f"{status_icon} Email {email_num} - {status_text}"):
            st.write(f"**Subject:** {email['subject']}")
            st.markdown("---")
            st.text_area("Body", email['body'], height=300, key=f"body_{email['id']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not is_sent:
                    if st.button(f"Send Email {email_num}", key=f"send_{email['id']}"):
                        success = system.email_sender.send_email(
                            to_email=prospect['email'],
                            subject=email['subject'],
                            body=email['body'],
                            html_body=email.get('html_body')
                        )
                        
                        if success:
                            system.db.mark_email_sent(selected_id, email_num)
                            st.success(f"✓ Email {email_num} sent!")
                            st.rerun()
                        else:
                            st.error("Failed to send email")
            
            with col2:
                if st.button(f"Preview HTML", key=f"preview_{email['id']}"):
                    st.markdown(email.get('html_body', ''), unsafe_allow_html=True)


def show_send_emails(system):
    """Batch send emails interface"""
    st.title("📤 Send Emails")
    
    st.write("Send emails in batches with customizable settings.")
    
    # Select email number
    email_number = st.radio("Which email to send?", [1, 2, 3])
    
    # Get prospects who haven't received this email yet
    all_prospects = system.db.get_all_prospects()
    unsent_prospects = []
    
    for prospect in all_prospects:
        if not system.db.get_email_status(prospect['id'], email_number):
            # Check if they have this email in sequence
            email = system.db.get_email_sequence(prospect['id'], email_number)
            if email:
                unsent_prospects.append(prospect)
    
    if not unsent_prospects:
        st.info(f"All prospects have already received Email #{email_number}")
        return
    
    st.write(f"**{len(unsent_prospects)} prospects** ready to receive Email #{email_number}")
    
    # Select prospects
    st.subheader("Select Prospects")
    
    select_all = st.checkbox("Select All", value=True)
    
    selected_prospects = []
    
    if select_all:
        selected_prospects = [p['id'] for p in unsent_prospects]
    else:
        for prospect in unsent_prospects:
            if st.checkbox(f"{prospect['company']} ({prospect['email']})", 
                          key=f"select_{prospect['id']}"):
                selected_prospects.append(prospect['id'])
    
    if not selected_prospects:
        st.warning("No prospects selected")
        return
    
    st.write(f"**{len(selected_prospects)} prospects selected**")
    
    # Settings
    st.subheader("Send Settings")
    
    delay = st.slider("Delay between emails (seconds)", min_value=10, max_value=120, value=30)
    
    # Preview
    if st.button("Preview First Email"):
        first_prospect = system.db.get_prospect(selected_prospects[0])
        first_email = system.db.get_email_sequence(selected_prospects[0], email_number)
        
        st.write(f"**To:** {first_prospect['email']}")
        st.write(f"**Subject:** {first_email['subject']}")
        st.text_area("Body", first_email['body'], height=200)
    
    # Send button
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col2:
        if st.button("🚀 SEND EMAILS", type="primary", use_container_width=True):
            st.warning("Are you sure? This will send emails to all selected prospects.")
            
            if st.button("✓ Yes, Send Now"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, prospect_id in enumerate(selected_prospects):
                    prospect = system.db.get_prospect(prospect_id)
                    email = system.db.get_email_sequence(prospect_id, email_number)
                    
                    status_text.text(f"Sending to {prospect['company']}... ({i+1}/{len(selected_prospects)})")
                    
                    success = system.email_sender.send_email(
                        to_email=prospect['email'],
                        subject=email['subject'],
                        body=email['body'],
                        html_body=email.get('html_body')
                    )
                    
                    if success:
                        system.db.mark_email_sent(prospect_id, email_number)
                    
                    progress_bar.progress((i + 1) / len(selected_prospects))
                    
                    if i < len(selected_prospects) - 1:
                        import time
                        time.sleep(delay)
                
                status_text.empty()
                progress_bar.empty()
                st.success(f"✓ Sent emails to {len(selected_prospects)} prospects!")
                st.balloons()


if __name__ == '__main__':
    # Run with: streamlit run web_interface.py
    st.write("This module should be run from main.py")
