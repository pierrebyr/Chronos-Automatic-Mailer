"""
Research Page - Brand research and discovery
"""

import streamlit as st


def render(system):
    """Render research page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">🔍 Brand Research</h1>
            <p class="page-subtitle">Discover and add new prospects to your outreach campaigns</p>
        </div>
    """, unsafe_allow_html=True)

    # Research form
    with st.form("research_form"):
        st.markdown("### 🎯 Search Parameters")

        col1, col2 = st.columns(2)

        with col1:
            category = st.text_input(
                "Category/Industry",
                placeholder="e.g., Irish Whiskey, Premium Gin, Luxury Watch",
                help="Enter the product category or industry to research"
            )

        with col2:
            limit = st.number_input(
                "Number of brands to find",
                min_value=1,
                max_value=100,
                value=20,
                help="Maximum number of brands to discover"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Start Research", type="primary", use_container_width=True)

    if submitted:
        if not category:
            st.error("❌ Please enter a category")
        else:
            with st.spinner(f"🔍 Researching {category} brands..."):
                try:
                    # Log activity
                    system.db.log_activity(
                        'research',
                        f"Started research for category: {category}",
                        metadata={'category': category, 'limit': limit}
                    )

                    # Run research
                    system.research_category(category, limit)

                    st.success(f"✅ Research complete! Found and added prospects.")

                    # Log completion
                    system.db.log_activity(
                        'research',
                        f"Completed research for category: {category}",
                        metadata={'category': category}
                    )

                    # Show results
                    prospects = system.db.get_prospects_by_category(category)
                    if prospects:
                        st.markdown(f"### 📊 Results: {len(prospects)} prospects")

                        for prospect in prospects[:10]:  # Show first 10
                            with st.expander(f"🏢 {prospect['company']}", expanded=False):
                                col1, col2 = st.columns(2)

                                with col1:
                                    st.write(f"**Email:** {prospect['email']}")
                                    st.write(f"**Website:** {prospect['website']}")
                                    st.write(f"**Sector:** {prospect['sector']}")

                                with col2:
                                    st.write(f"**Category:** {prospect['category']}")
                                    st.write(f"**Status:** {prospect['status']}")

                                if prospect['description']:
                                    st.markdown(f"**Description:** {prospect['description']}")

                        if len(prospects) > 10:
                            st.info(f"Showing 10 of {len(prospects)} prospects. View all in the Prospects page.")

                except Exception as e:
                    st.error(f"❌ Research failed: {e}")
                    system.db.log_activity(
                        'research',
                        f"Research failed for category: {category}",
                        metadata={'error': str(e)}
                    )

    # Recent research history
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📜 Recent Research")

    recent_research = [
        a for a in system.db.get_recent_activities(limit=20)
        if a['activity_type'] == 'research'
    ]

    if recent_research:
        for activity in recent_research[:5]:
            metadata = activity.get('metadata', {})
            category = metadata.get('category', 'Unknown') if metadata else 'Unknown'

            st.markdown(f"""
                <div class="timeline-content" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{activity['description']}</strong>
                        </div>
                        <div style="color: #6B7280; font-size: 0.875rem;">{activity['created_at']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent research activity")

    # Quick stats
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Research Statistics")

    prospects = system.db.get_all_prospects()
    categories = {}
    for p in prospects:
        cat = p.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1

    if categories:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Prospects", len(prospects))

        with col2:
            st.metric("Categories", len(categories))

        with col3:
            avg_per_cat = round(len(prospects) / len(categories), 1) if categories else 0
            st.metric("Avg per Category", avg_per_cat)
    else:
        st.info("No research data yet. Start by researching a category above!")
