"""
Dashboard Page - Overview and key metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def render(system):
    """Render dashboard page"""

    # Page header
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">📊 Dashboard</h1>
            <p class="page-subtitle">Overview of your outreach campaigns</p>
        </div>
    """, unsafe_allow_html=True)

    # Get metrics
    metrics = system.db.get_dashboard_metrics()

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Prospects</div>
                <div class="metric-value">{metrics['total_prospects']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Email Sequences</div>
                <div class="metric-value">{metrics['with_sequences']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Emails Sent</div>
                <div class="metric-value">{metrics['emails_sent']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_rate = 0
        if metrics['total_prospects'] > 0:
            avg_rate = round((metrics['emails_sent'] / metrics['total_prospects']) * 100)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Emails/Prospect</div>
                <div class="metric-value">{metrics['avg_emails_per_prospect']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row of metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Sent Today</div>
                <div class="metric-value" style="color: #10B981;">{metrics['emails_sent_today']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Sent This Week</div>
                <div class="metric-value" style="color: #3B82F6;">{metrics['emails_sent_week']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Recent Activities</div>
                <div class="metric-value" style="color: #F59E0B;">{metrics['recent_activities']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts section
    col1, col2 = st.columns(2)

    with col1:
        # Prospects by status chart
        st.markdown("### 📈 Prospects by Status")
        if metrics['by_status']:
            status_df = pd.DataFrame(
                list(metrics['by_status'].items()),
                columns=['Status', 'Count']
            )
            fig = px.pie(
                status_df,
                values='Count',
                names='Status',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(
                showlegend=True,
                height=350,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No prospects yet")

    with col2:
        # Categories chart
        st.markdown("### 🏷️ Prospects by Category")
        if metrics['categories']:
            prospects = system.db.get_all_prospects()
            category_counts = {}
            for p in prospects:
                cat = p.get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1

            cat_df = pd.DataFrame(
                list(category_counts.items()),
                columns=['Category', 'Count']
            )
            fig = px.bar(
                cat_df,
                x='Category',
                y='Count',
                color='Count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title="",
                yaxis_title="Number of Prospects"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categories yet")

    # Emails sent timeline
    st.markdown("### 📅 Email Activity (Last 7 Days)")
    if metrics['emails_by_day']:
        # Create full 7-day range
        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

        # Create data with zeros for missing days
        email_data = {day: 0 for day in last_7_days}
        for item in metrics['emails_by_day']:
            if item['date'] in email_data:
                email_data[item['date']] = item['count']

        timeline_df = pd.DataFrame(
            list(email_data.items()),
            columns=['Date', 'Emails Sent']
        )

        fig = px.area(
            timeline_df,
            x='Date',
            y='Emails Sent',
            color_discrete_sequence=['#6366F1']
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="",
            yaxis_title="Emails Sent",
            hovermode='x unified'
        )
        fig.update_traces(
            fill='tozeroy',
            line=dict(width=2),
            fillcolor='rgba(99, 102, 241, 0.1)'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No email activity in the last 7 days")

    # Recent activity
    st.markdown("### ⏱️ Recent Activity")
    activities = system.db.get_recent_activities(limit=10)

    if activities:
        for activity in activities:
            # Format timestamp
            created_at = activity['created_at']
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    created_at = datetime.now()

            time_str = created_at.strftime('%Y-%m-%d %H:%M')

            # Activity type icon
            icon = {
                'research': '🔍',
                'email_generated': '📝',
                'email_sent': '📤',
                'prospect_added': '➕',
                'status_changed': '🔄'
            }.get(activity['activity_type'], '📌')

            st.markdown(f"""
                <div class="timeline-content" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
                            <strong>{activity['description']}</strong>
                        </div>
                        <div style="color: #6B7280; font-size: 0.875rem;">{time_str}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity")

    # Quick actions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔍 Research New Brands", use_container_width=True, type="primary"):
            st.session_state.current_page = 'Research'
            st.rerun()

    with col2:
        if st.button("👥 View Prospects", use_container_width=True):
            st.session_state.current_page = 'Prospects'
            st.rerun()

    with col3:
        if st.button("📝 Generate Emails", use_container_width=True):
            st.session_state.current_page = 'Email Sequences'
            st.rerun()

    with col4:
        if st.button("📤 Send Campaign", use_container_width=True):
            st.session_state.current_page = 'Send Emails'
            st.rerun()
