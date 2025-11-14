"""
Prospects Page - Manage and view all prospects
"""

import streamlit as st
import pandas as pd


def render(system):
    """Render prospects page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">👥 Prospects</h1>
            <p class="page-subtitle">Manage your outreach prospects and contacts</p>
        </div>
    """, unsafe_allow_html=True)

    # Get all prospects
    prospects = system.db.get_all_prospects()

    if not prospects:
        st.info("📭 No prospects yet. Start by researching brands!")
        return

    # Filters
    st.markdown("### 🔍 Filters")
    col1, col2, col3 = st.columns(3)

    with col1:
        # Get unique categories
        categories = list(set(p.get('category', 'Unknown') for p in prospects))
        selected_category = st.selectbox(
            "Category",
            options=['All'] + sorted(categories),
            key="filter_category"
        )

    with col2:
        # Get unique statuses
        statuses = list(set(p.get('status', 'prospect') for p in prospects))
        selected_status = st.selectbox(
            "Status",
            options=['All'] + sorted(statuses),
            key="filter_status"
        )

    with col3:
        search_term = st.text_input("🔎 Search", placeholder="Company, email, sector...")

    # Apply filters
    filtered_prospects = prospects

    if selected_category != 'All':
        filtered_prospects = [p for p in filtered_prospects if p.get('category') == selected_category]

    if selected_status != 'All':
        filtered_prospects = [p for p in filtered_prospects if p.get('status') == selected_status]

    if search_term:
        search_lower = search_term.lower()
        filtered_prospects = [
            p for p in filtered_prospects
            if search_lower in p.get('company', '').lower()
            or search_lower in p.get('email', '').lower()
            or search_lower in p.get('sector', '').lower()
        ]

    # Display count
    st.markdown(f"### 📊 Showing {len(filtered_prospects)} of {len(prospects)} prospects")

    # Display as table
    if filtered_prospects:
        # Convert to DataFrame for better display
        df_data = []
        for p in filtered_prospects:
            df_data.append({
                'ID': p['id'],
                'Company': p['company'],
                'Email': p['email'],
                'Sector': p.get('sector', ''),
                'Category': p.get('category', ''),
                'Status': p.get('status', 'prospect'),
                'Created': p.get('created_at', '')[:10] if p.get('created_at') else ''
            })

        df = pd.DataFrame(df_data)

        # Display with selection
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
            hide_index=True
        )

        # Detail view
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Prospect Details")

        selected_id = st.number_input(
            "Select Prospect ID to view details",
            min_value=1,
            max_value=max(p['id'] for p in filtered_prospects),
            value=filtered_prospects[0]['id'],
            key="selected_prospect_id"
        )

        prospect = system.db.get_prospect(selected_id)

        if prospect:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🏢 Company Information")
                st.write(f"**Company:** {prospect['company']}")
                st.write(f"**Contact Name:** {prospect.get('name', 'N/A')}")
                st.write(f"**Email:** {prospect['email']}")
                st.write(f"**Website:** {prospect.get('website', 'N/A')}")

            with col2:
                st.markdown("#### 📊 Classification")
                st.write(f"**Sector:** {prospect.get('sector', 'N/A')}")
                st.write(f"**Category:** {prospect.get('category', 'N/A')}")
                st.write(f"**Status:** {prospect.get('status', 'prospect')}")

            if prospect.get('description'):
                st.markdown("#### 📝 Description")
                st.write(prospect['description'])

            if prospect.get('products'):
                st.markdown("#### 🏷️ Products")
                products = prospect['products']
                if isinstance(products, list):
                    for product in products:
                        st.write(f"- {product}")
                else:
                    st.write(products)

            # Email sequences status
            sequences = system.db.get_all_email_sequences(selected_id)
            if sequences:
                st.markdown("#### 📧 Email Sequences")
                st.write(f"**Sequences generated:** {len(sequences)}")

                for seq in sequences:
                    sent = system.db.get_email_status(selected_id, seq['email_number'])
                    status_icon = "✅" if sent else "⏳"
                    st.write(f"{status_icon} Email {seq['email_number']}: {seq['subject']}")

            # Actions
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### ⚡ Actions")

            col1, col2, col3 = st.columns(3)

            with col1:
                new_status = st.selectbox(
                    "Update Status",
                    options=['prospect', 'contacted', 'lead', 'client'],
                    index=['prospect', 'contacted', 'lead', 'client'].index(prospect.get('status', 'prospect')),
                    key="new_status"
                )

                if st.button("Update Status", key="update_status_btn"):
                    system.db.update_prospect_status(selected_id, new_status)
                    system.db.log_activity(
                        'status_changed',
                        f"Status changed for {prospect['company']}: {new_status}",
                        prospect_id=selected_id
                    )
                    st.success(f"✅ Status updated to {new_status}")
                    st.rerun()

            with col2:
                if st.button("📝 Generate Emails", key="gen_emails_btn", use_container_width=True):
                    st.session_state.current_page = 'Email Sequences'
                    st.session_state.selected_prospect_id = selected_id
                    st.rerun()

            with col3:
                if st.button("📊 View Analytics", key="view_analytics_btn", use_container_width=True):
                    st.session_state.current_page = 'Analytics'
                    st.rerun()

    else:
        st.warning("No prospects match your filters")
