"""
Send Emails Page - Send email campaigns with tracking
"""

import streamlit as st
import time


def render(system):
    """Render send emails page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">📤 Send Emails</h1>
            <p class="page-subtitle">Launch your outreach campaigns with real-time tracking</p>
        </div>
    """, unsafe_allow_html=True)

    # Get prospects with sequences
    all_prospects = system.db.get_all_prospects()
    prospects_with_sequences = [p for p in all_prospects if system.db.get_all_email_sequences(p['id'])]

    if not prospects_with_sequences:
        st.warning("⚠️ No email sequences available. Generate sequences first!")
        if st.button("📝 Go to Email Sequences"):
            st.session_state.current_page = 'Email Sequences'
            st.rerun()
        return

    st.markdown("### 📊 Campaign Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Prospects with Sequences", len(prospects_with_sequences))

    with col2:
        # Count unsent
        unsent_count = sum(
            1 for p in prospects_with_sequences
            if not system.db.get_email_status(p['id'], 1)
        )
        st.metric("Unsent (Email #1)", unsent_count)

    with col3:
        sent_today = system.db.get_dashboard_metrics()['emails_sent_today']
        st.metric("Sent Today", sent_today)

    with col4:
        total_sent = system.db.get_dashboard_metrics()['emails_sent']
        st.metric("Total Sent", total_sent)

    st.markdown("<br>", unsafe_allow_html=True)

    # Email selection
    email_number = st.selectbox(
        "Select Email in Sequence",
        options=[1, 2, 3],
        format_func=lambda x: f"Email #{x}",
        help="Choose which email in the sequence to send"
    )

    # Filter prospects who haven't received this email
    unsent_prospects = [
        p for p in prospects_with_sequences
        if not system.db.get_email_status(p['id'], email_number)
    ]

    st.markdown(f"### 📋 Ready to Send: {len(unsent_prospects)} prospects")

    if not unsent_prospects:
        st.success(f"✅ Email #{email_number} has been sent to all prospects!")
        return

    # Category filter
    categories = list(set(p.get('category', 'Unknown') for p in unsent_prospects))
    selected_category = st.multiselect(
        "Filter by Category",
        options=categories,
        default=categories
    )

    filtered_prospects = [
        p for p in unsent_prospects
        if p.get('category', 'Unknown') in selected_category
    ]

    st.info(f"📤 Will send to **{len(filtered_prospects)}** prospects")

    # Preview first email
    if filtered_prospects:
        with st.expander("👁️ Preview First Email", expanded=False):
            first_prospect = filtered_prospects[0]
            email = system.db.get_email_sequence(first_prospect['id'], email_number)

            if email:
                st.write(f"**To:** {first_prospect['email']} ({first_prospect['company']})")
                st.write(f"**Subject:** {email['subject']}")
                st.markdown("---")
                st.text_area("Body", email['body'], height=200, disabled=True)

    # Sending options
    st.markdown("### ⚙️ Sending Options")

    col1, col2 = st.columns(2)

    with col1:
        delay = st.slider(
            "Delay between emails (seconds)",
            min_value=5,
            max_value=120,
            value=30,
            help="Wait time between each email to avoid spam filters"
        )

    with col2:
        test_mode = st.checkbox(
            "Test Mode (don't actually send)",
            value=False,
            help="Simulate sending without actually sending emails"
        )

    # Send button with confirmation
    st.markdown("<br>", unsafe_allow_html=True)

    if 'confirm_send' not in st.session_state:
        st.session_state.confirm_send = False

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if not st.session_state.confirm_send:
            if st.button(
                f"🚀 Send Email #{email_number} to {len(filtered_prospects)} Prospects",
                type="primary",
                use_container_width=True
            ):
                st.session_state.confirm_send = True
                st.rerun()
        else:
            st.warning(f"⚠️ You are about to send {len(filtered_prospects)} emails. This action cannot be undone.")

            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("✓ Confirm Send", type="primary", use_container_width=True):
                    # Send emails
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    success_count = 0
                    error_count = 0

                    for i, prospect in enumerate(filtered_prospects):
                        email = system.db.get_email_sequence(prospect['id'], email_number)

                        status_text.text(f"Sending to {prospect['company']}... ({i+1}/{len(filtered_prospects)})")

                        try:
                            if not test_mode:
                                # Actual send
                                success = system.email_sender.send_email(
                                    to_email=prospect['email'],
                                    subject=email['subject'],
                                    body=email['body']
                                )
                            else:
                                # Test mode
                                success = True
                                time.sleep(0.5)

                            if success:
                                system.db.mark_email_sent(prospect['id'], email_number)
                                system.db.log_activity(
                                    'email_sent',
                                    f"Email #{email_number} sent to {prospect['company']}",
                                    prospect_id=prospect['id'],
                                    metadata={'email_number': email_number, 'test_mode': test_mode}
                                )
                                success_count += 1
                            else:
                                error_count += 1

                        except Exception as e:
                            error_count += 1
                            st.warning(f"⚠️ Failed to send to {prospect['company']}: {e}")

                        progress_bar.progress((i + 1) / len(filtered_prospects))

                        if i < len(filtered_prospects) - 1:
                            time.sleep(delay)

                    status_text.empty()
                    progress_bar.empty()

                    if test_mode:
                        st.info(f"🧪 Test complete: Simulated {success_count} emails")
                    else:
                        st.success(f"✅ Campaign complete! Sent {success_count} emails, {error_count} errors")

                    st.balloons()
                    st.session_state.confirm_send = False
                    st.rerun()

            with col_no:
                if st.button("✗ Cancel", use_container_width=True):
                    st.session_state.confirm_send = False
                    st.rerun()

    # Recent sends
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📬 Recent Sends")

    recent_sends = [
        a for a in system.db.get_recent_activities(limit=20)
        if a['activity_type'] == 'email_sent'
    ]

    if recent_sends:
        for send in recent_sends[:10]:
            metadata = send.get('metadata', {})
            email_num = metadata.get('email_number', '?') if metadata else '?'
            test_badge = " 🧪" if (metadata and metadata.get('test_mode')) else ""

            st.markdown(f"""
                <div class="timeline-content" style="margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>📤 <strong>{send['description']}</strong>{test_badge}</div>
                        <div style="color: #6B7280; font-size: 0.875rem;">{send['created_at'][:16]}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent sends")
