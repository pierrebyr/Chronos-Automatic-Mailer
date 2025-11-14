"""
History Page - Complete activity timeline and audit log
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render(system):
    """Render history page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">⏱️ History</h1>
            <p class="page-subtitle">Complete timeline of all system activities</p>
        </div>
    """, unsafe_allow_html=True)

    # Time period filter
    col1, col2 = st.columns(2)

    with col1:
        period = st.selectbox(
            "Time Period",
            options=['Last 24 hours', 'Last 7 days', 'Last 30 days', 'All time'],
            index=1
        )

    with col2:
        activity_types = st.multiselect(
            "Activity Types",
            options=['All', 'research', 'email_generated', 'email_sent', 'status_changed', 'prospect_added'],
            default=['All']
        )

    # Get activities
    limit = 100 if period == 'All time' else 50
    all_activities = system.db.get_recent_activities(limit=limit)

    # Filter by period
    filtered_activities = all_activities

    if period != 'All time':
        days_map = {
            'Last 24 hours': 1,
            'Last 7 days': 7,
            'Last 30 days': 30
        }
        days = days_map.get(period, 7)
        cutoff = datetime.now() - timedelta(days=days)

        filtered_activities = [
            a for a in all_activities
            if datetime.fromisoformat(a['created_at'].replace('Z', '+00:00')) > cutoff
        ]

    # Filter by activity type
    if 'All' not in activity_types and activity_types:
        filtered_activities = [
            a for a in filtered_activities
            if a['activity_type'] in activity_types
        ]

    # Stats
    st.markdown("### 📊 Activity Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Activities", len(filtered_activities))

    with col2:
        research_count = sum(1 for a in filtered_activities if a['activity_type'] == 'research')
        st.metric("Research", research_count)

    with col3:
        sent_count = sum(1 for a in filtered_activities if a['activity_type'] == 'email_sent')
        st.metric("Emails Sent", sent_count)

    with col4:
        generated_count = sum(1 for a in filtered_activities if a['activity_type'] == 'email_generated')
        st.metric("Sequences Generated", generated_count)

    # Timeline view
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📜 Activity Timeline")

    if filtered_activities:
        # Group by date
        activities_by_date = {}
        for activity in filtered_activities:
            created_at = activity['created_at']
            if isinstance(created_at, str):
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    dt = datetime.now()
            else:
                dt = created_at

            date_key = dt.strftime('%Y-%m-%d')

            if date_key not in activities_by_date:
                activities_by_date[date_key] = []

            activities_by_date[date_key].append((dt, activity))

        # Display by date
        for date_key in sorted(activities_by_date.keys(), reverse=True):
            st.markdown(f"#### 📅 {date_key}")

            activities = sorted(activities_by_date[date_key], key=lambda x: x[0], reverse=True)

            for dt, activity in activities:
                time_str = dt.strftime('%H:%M:%S')

                # Activity type icon and color
                type_config = {
                    'research': ('🔍', '#3B82F6'),
                    'email_generated': ('📝', '#10B981'),
                    'email_sent': ('📤', '#8B5CF6'),
                    'status_changed': ('🔄', '#F59E0B'),
                    'prospect_added': ('➕', '#06B6D4')
                }

                icon, color = type_config.get(activity['activity_type'], ('📌', '#6B7280'))

                # Get prospect if available
                prospect_info = ""
                if activity.get('prospect_id'):
                    prospect = system.db.get_prospect(activity['prospect_id'])
                    if prospect:
                        prospect_info = f" - {prospect['company']}"

                st.markdown(f"""
                    <div class="timeline-content" style="margin-bottom: 0.75rem; border-left: 3px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
                                <strong>{activity['description']}</strong>
                                <span style="color: #6B7280;">{prospect_info}</span>
                            </div>
                            <div style="color: #6B7280; font-size: 0.875rem; white-space: nowrap; margin-left: 1rem;">
                                {time_str}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.info("No activities found for the selected filters")

    # Export option
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📥 Export")

    if filtered_activities and st.button("📊 Export to CSV"):
        # Convert to DataFrame
        df_data = []
        for activity in filtered_activities:
            prospect_name = ""
            if activity.get('prospect_id'):
                prospect = system.db.get_prospect(activity['prospect_id'])
                if prospect:
                    prospect_name = prospect['company']

            df_data.append({
                'Date': activity['created_at'],
                'Type': activity['activity_type'],
                'Description': activity['description'],
                'Prospect': prospect_name
            })

        df = pd.DataFrame(df_data)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"chronos_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
