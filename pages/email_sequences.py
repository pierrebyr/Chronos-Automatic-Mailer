"""
Email Sequences Page - Generate and manage email sequences
"""

import streamlit as st


def render(system):
    """Render email sequences page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">📝 Email Sequences</h1>
            <p class="page-subtitle">Generate personalized email campaigns for your prospects</p>
        </div>
    """, unsafe_allow_html=True)

    # Get prospects without email sequences
    prospects_without_emails = system.db.get_prospects_without_emails()
    all_prospects = system.db.get_all_prospects()

    # Stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Prospects", len(all_prospects))

    with col2:
        with_sequences = len(all_prospects) - len(prospects_without_emails)
        st.metric("With Sequences", with_sequences)

    with col3:
        st.metric("Pending Generation", len(prospects_without_emails))

    st.markdown("<br>", unsafe_allow_html=True)

    # Generate for all or selected
    tab1, tab2 = st.tabs(["📊 Batch Generation", "✏️ Single Prospect"])

    with tab1:
        st.markdown("### 🚀 Generate Emails for Multiple Prospects")

        if prospects_without_emails:
            st.info(f"📋 {len(prospects_without_emails)} prospects need email sequences")

            category_filter = st.selectbox(
                "Filter by Category",
                options=['All'] + list(set(p.get('category', 'Unknown') for p in prospects_without_emails))
            )

            filtered = prospects_without_emails
            if category_filter != 'All':
                filtered = [p for p in prospects_without_emails if p.get('category') == category_filter]

            st.write(f"Will generate for **{len(filtered)}** prospects")

            if st.button("🎨 Generate Email Sequences", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, prospect in enumerate(filtered):
                    status_text.text(f"Generating for {prospect['company']}... ({i+1}/{len(filtered)})")

                    try:
                        # Generate sequence
                        sequence = system.email_gen.generate_sequence(prospect)
                        system.db.add_email_sequence(prospect['id'], sequence)

                        # Log activity
                        system.db.log_activity(
                            'email_generated',
                            f"Generated email sequence for {prospect['company']}",
                            prospect_id=prospect['id']
                        )

                    except Exception as e:
                        st.warning(f"⚠️ Failed for {prospect['company']}: {e}")

                    progress_bar.progress((i + 1) / len(filtered))

                status_text.empty()
                progress_bar.empty()
                st.success(f"✅ Generated sequences for {len(filtered)} prospects!")
                st.rerun()
        else:
            st.success("✅ All prospects have email sequences!")

    with tab2:
        st.markdown("### ✏️ Generate for Single Prospect")

        if all_prospects:
            # Select prospect
            prospect_options = {f"{p['company']} ({p['email']})": p['id'] for p in all_prospects}
            selected_prospect_name = st.selectbox(
                "Select Prospect",
                options=list(prospect_options.keys())
            )

            prospect_id = prospect_options[selected_prospect_name]
            prospect = system.db.get_prospect(prospect_id)

            # Check if already has sequences
            existing_sequences = system.db.get_all_email_sequences(prospect_id)

            if existing_sequences:
                st.warning(f"⚠️ This prospect already has {len(existing_sequences)} email sequences. Regenerating will replace them.")

            # Preview prospect info
            with st.expander("📋 Prospect Information", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Company:** {prospect['company']}")
                    st.write(f"**Email:** {prospect['email']}")
                    st.write(f"**Sector:** {prospect.get('sector', 'N/A')}")
                with col2:
                    st.write(f"**Category:** {prospect.get('category', 'N/A')}")
                    st.write(f"**Products:** {len(prospect.get('products', []))}")

            if st.button("🎨 Generate Email Sequence", type="primary", use_container_width=True):
                with st.spinner(f"Generating personalized emails for {prospect['company']}..."):
                    try:
                        sequence = system.email_gen.generate_sequence(prospect)
                        system.db.add_email_sequence(prospect_id, sequence)

                        system.db.log_activity(
                            'email_generated',
                            f"Generated email sequence for {prospect['company']}",
                            prospect_id=prospect_id
                        )

                        st.success("✅ Email sequence generated successfully!")

                        # Show preview
                        for i in range(1, 4):
                            email = system.db.get_email_sequence(prospect_id, i)
                            if email:
                                with st.expander(f"📧 Email {i}: {email['subject']}", expanded=False):
                                    st.markdown(f"**Subject:** {email['subject']}")
                                    st.markdown("---")
                                    st.text_area(
                                        "Body",
                                        email['body'],
                                        height=200,
                                        key=f"preview_{i}",
                                        disabled=True
                                    )

                    except Exception as e:
                        st.error(f"❌ Generation failed: {e}")

    # View existing sequences
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📚 Existing Sequences")

    prospects_with_sequences = [p for p in all_prospects if system.db.get_all_email_sequences(p['id'])]

    if prospects_with_sequences:
        selected_prospect = st.selectbox(
            "View sequences for:",
            options=[f"{p['company']} - {p['email']}" for p in prospects_with_sequences],
            key="view_sequences"
        )

        if selected_prospect:
            # Find prospect
            prospect = next(
                p for p in prospects_with_sequences
                if f"{p['company']} - {p['email']}" == selected_prospect
            )

            sequences = system.db.get_all_email_sequences(prospect['id'])

            for seq in sequences:
                sent = system.db.get_email_status(prospect['id'], seq['email_number'])
                status = "✅ Sent" if sent else "⏳ Not Sent"

                with st.expander(f"📧 Email {seq['email_number']}: {seq['subject']} - {status}"):
                    st.markdown(f"**Subject:** {seq['subject']}")
                    st.markdown("---")
                    st.text_area(
                        "Body",
                        seq['body'],
                        height=250,
                        key=f"seq_{prospect['id']}_{seq['email_number']}",
                        disabled=True
                    )
    else:
        st.info("No email sequences generated yet")
