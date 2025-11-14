"""
Analytics Page - Advanced metrics and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def render(system):
    """Render analytics page"""

    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">📊 Analytics</h1>
            <p class="page-subtitle">Deep insights into your outreach performance</p>
        </div>
    """, unsafe_allow_html=True)

    # Get comprehensive metrics
    metrics = system.db.get_dashboard_metrics()
    prospects = system.db.get_all_prospects()

    # Overview metrics
    st.markdown("### 🎯 Performance Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Prospects", metrics['total_prospects'])

    with col2:
        coverage = 0
        if metrics['total_prospects'] > 0:
            coverage = round((metrics['with_sequences'] / metrics['total_prospects']) * 100)
        st.metric("Coverage", f"{coverage}%")

    with col3:
        st.metric("Total Emails Sent", metrics['emails_sent'])

    with col4:
        st.metric("This Week", metrics['emails_sent_week'])

    with col5:
        st.metric("Today", metrics['emails_sent_today'])

    # Charts
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Prospects by status - donut chart
        st.markdown("#### 🎯 Prospects by Status")
        if metrics['by_status']:
            status_df = pd.DataFrame(
                list(metrics['by_status'].items()),
                columns=['Status', 'Count']
            )

            # Map status to colors
            colors = {
                'prospect': '#3B82F6',
                'contacted': '#F59E0B',
                'lead': '#10B981',
                'client': '#8B5CF6'
            }
            status_df['color'] = status_df['Status'].map(colors)

            fig = go.Figure(data=[go.Pie(
                labels=status_df['Status'],
                values=status_df['Count'],
                hole=0.5,
                marker=dict(colors=status_df['color'])
            )])

            fig.update_layout(
                showlegend=True,
                height=350,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data")

    with col2:
        # Email sequence completion funnel
        st.markdown("#### 📧 Email Sequence Funnel")

        email_1_sent = sum(1 for p in prospects if system.db.get_email_status(p['id'], 1))
        email_2_sent = sum(1 for p in prospects if system.db.get_email_status(p['id'], 2))
        email_3_sent = sum(1 for p in prospects if system.db.get_email_status(p['id'], 3))

        funnel_data = pd.DataFrame({
            'Stage': ['Email #1', 'Email #2', 'Email #3'],
            'Count': [email_1_sent, email_2_sent, email_3_sent]
        })

        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            textinfo="value+percent initial",
            marker=dict(color=["#6366F1", "#818CF8", "#A5B4FC"])
        ))

        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Category analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏷️ Category Performance")

    if prospects:
        # Calculate per-category stats
        category_stats = {}
        for prospect in prospects:
            cat = prospect.get('category', 'Unknown')
            if cat not in category_stats:
                category_stats[cat] = {
                    'prospects': 0,
                    'with_sequences': 0,
                    'emails_sent': 0
                }

            category_stats[cat]['prospects'] += 1

            if system.db.get_all_email_sequences(prospect['id']):
                category_stats[cat]['with_sequences'] += 1

            for i in range(1, 4):
                if system.db.get_email_status(prospect['id'], i):
                    category_stats[cat]['emails_sent'] += 1

        # Display as table
        cat_df = pd.DataFrame([
            {
                'Category': cat,
                'Prospects': stats['prospects'],
                'With Sequences': stats['with_sequences'],
                'Emails Sent': stats['emails_sent'],
                'Avg Emails/Prospect': round(stats['emails_sent'] / stats['prospects'], 2) if stats['prospects'] > 0 else 0
            }
            for cat, stats in category_stats.items()
        ])

        st.dataframe(cat_df, use_container_width=True, hide_index=True)

        # Category breakdown chart
        st.markdown("#### 📊 Prospects Distribution")
        fig = px.treemap(
            cat_df,
            path=['Category'],
            values='Prospects',
            color='Avg Emails/Prospect',
            color_continuous_scale='Blues',
            title=''
        )
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Email activity heatmap
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📅 Email Activity Heatmap (Last 30 Days)")

    # Get email activity for last 30 days
    today = datetime.now().date()
    activity_data = []

    for i in range(30):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')

        # Count emails sent on this date
        activities = system.db.get_recent_activities(limit=1000)
        count = sum(
            1 for a in activities
            if a['activity_type'] == 'email_sent'
            and a['created_at'].startswith(date_str)
        )

        activity_data.append({
            'date': date_str,
            'weekday': date.strftime('%A'),
            'emails': count
        })

    if activity_data:
        df = pd.DataFrame(activity_data)

        fig = px.bar(
            df.tail(30),
            x='date',
            y='emails',
            color='emails',
            color_continuous_scale='Blues',
            labels={'date': 'Date', 'emails': 'Emails Sent'}
        )

        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=50),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Emails Sent"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Key Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Most active category
        if prospects:
            cat_counts = {}
            for p in prospects:
                cat = p.get('category', 'Unknown')
                cat_counts[cat] = cat_counts.get(cat, 0) + 1

            most_active_cat = max(cat_counts.items(), key=lambda x: x[1])
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Most Active Category</div>
                    <div class="metric-value" style="font-size: 1.5rem;">{most_active_cat[0]}</div>
                    <div style="color: #6B7280; margin-top: 0.5rem;">{most_active_cat[1]} prospects</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        # Completion rate
        if metrics['total_prospects'] > 0:
            completion_rate = round((email_3_sent / metrics['total_prospects']) * 100, 1)
        else:
            completion_rate = 0

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Sequence Completion</div>
                <div class="metric-value" style="font-size: 1.5rem;">{completion_rate}%</div>
                <div style="color: #6B7280; margin-top: 0.5rem;">Prospects receiving all 3 emails</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        # Avg emails per day
        if metrics['emails_sent_week'] > 0:
            avg_per_day = round(metrics['emails_sent_week'] / 7, 1)
        else:
            avg_per_day = 0

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Daily Average (7d)</div>
                <div class="metric-value" style="font-size: 1.5rem;">{avg_per_day}</div>
                <div style="color: #6B7280; margin-top: 0.5rem;">Emails per day</div>
            </div>
        """, unsafe_allow_html=True)
