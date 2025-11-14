#!/usr/bin/env python3
"""
Database Module - SQLite database for prospects and email tracking
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


class Database:
    """Manages all database operations for the outreach system"""
    
    def __init__(self, db_path="chronos_outreach.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prospects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prospects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                email TEXT NOT NULL,
                website TEXT,
                sector TEXT,
                category TEXT,
                products TEXT,
                description TEXT,
                status TEXT DEFAULT 'prospect',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email sequences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prospect_id INTEGER NOT NULL,
                email_number INTEGER NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                html_body TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prospect_id) REFERENCES prospects(id),
                UNIQUE(prospect_id, email_number)
            )
        ''')
        
        # Email sends table (tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_sends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prospect_id INTEGER NOT NULL,
                email_number INTEGER NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'sent',
                FOREIGN KEY (prospect_id) REFERENCES prospects(id)
            )
        ''')
        
        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prospect_id INTEGER NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prospect_id) REFERENCES prospects(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_prospect(self, prospect_data, category):
        """Add a new prospect to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert products list to JSON string
        products_json = json.dumps(prospect_data.get('products', []))
        
        cursor.execute('''
            INSERT INTO prospects 
            (name, company, email, website, sector, category, products, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            prospect_data.get('name', prospect_data.get('company')),
            prospect_data.get('company'),
            prospect_data.get('email'),
            prospect_data.get('website'),
            prospect_data.get('sector', 'Unknown'),
            category,
            products_json,
            prospect_data.get('description', ''),
            'prospect'
        ))
        
        prospect_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prospect_id
    
    def get_prospect(self, prospect_id):
        """Get a single prospect by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM prospects WHERE id = ?', (prospect_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            prospect = dict(row)
            # Parse products JSON
            prospect['products'] = json.loads(prospect['products']) if prospect['products'] else []
            return prospect
        return None
    
    def get_all_prospects(self):
        """Get all prospects"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM prospects ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        prospects = []
        for row in rows:
            prospect = dict(row)
            prospect['products'] = json.loads(prospect['products']) if prospect['products'] else []
            prospects.append(prospect)
        
        return prospects
    
    def get_prospects_by_category(self, category):
        """Get all prospects in a specific category"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM prospects WHERE category = ? ORDER BY created_at DESC', 
                      (category,))
        rows = cursor.fetchall()
        conn.close()
        
        prospects = []
        for row in rows:
            prospect = dict(row)
            prospect['products'] = json.loads(prospect['products']) if prospect['products'] else []
            prospects.append(prospect)
        
        return prospects
    
    def get_prospects_without_emails(self):
        """Get prospects that don't have email sequences yet"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.* FROM prospects p
            LEFT JOIN email_sequences e ON p.id = e.prospect_id
            WHERE e.id IS NULL
            ORDER BY p.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        prospects = []
        for row in rows:
            prospect = dict(row)
            prospect['products'] = json.loads(prospect['products']) if prospect['products'] else []
            prospects.append(prospect)
        
        return prospects
    
    def add_email_sequence(self, prospect_id, email_sequence):
        """Add complete email sequence for a prospect"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add each email in the sequence
        for email_num in [1, 2, 3]:
            email_key = f'email_{email_num}'
            email_data = email_sequence.get(email_key, {})
            
            cursor.execute('''
                INSERT OR REPLACE INTO email_sequences 
                (prospect_id, email_number, subject, body, html_body)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                prospect_id,
                email_num,
                email_data.get('subject', ''),
                email_data.get('body', ''),
                email_data.get('html_body', '')
            ))
        
        conn.commit()
        conn.close()
    
    def get_email_sequence(self, prospect_id, email_number):
        """Get a specific email from a prospect's sequence"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM email_sequences 
            WHERE prospect_id = ? AND email_number = ?
        ''', (prospect_id, email_number))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_all_email_sequences(self, prospect_id):
        """Get all emails for a prospect"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM email_sequences 
            WHERE prospect_id = ?
            ORDER BY email_number
        ''', (prospect_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def mark_email_sent(self, prospect_id, email_number):
        """Mark an email as sent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_sends (prospect_id, email_number, status)
            VALUES (?, ?, 'sent')
        ''', (prospect_id, email_number))
        
        conn.commit()
        conn.close()
    
    def get_email_status(self, prospect_id, email_number):
        """Check if an email has been sent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM email_sends 
            WHERE prospect_id = ? AND email_number = ?
        ''', (prospect_id, email_number))
        
        row = cursor.fetchone()
        conn.close()
        
        return row is not None
    
    def add_note(self, prospect_id, note):
        """Add a note to a prospect"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notes (prospect_id, note)
            VALUES (?, ?)
        ''', (prospect_id, note))
        
        conn.commit()
        conn.close()
    
    def get_notes(self, prospect_id):
        """Get all notes for a prospect"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notes 
            WHERE prospect_id = ?
            ORDER BY created_at DESC
        ''', (prospect_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_prospect_status(self, prospect_id, status):
        """Update prospect status (prospect, contacted, lead, client)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE prospects 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, prospect_id))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Get system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total prospects
        cursor.execute('SELECT COUNT(*) FROM prospects')
        total_prospects = cursor.fetchone()[0]
        
        # Prospects with email sequences
        cursor.execute('''
            SELECT COUNT(DISTINCT prospect_id) FROM email_sequences
        ''')
        with_sequences = cursor.fetchone()[0]
        
        # Total emails sent
        cursor.execute('SELECT COUNT(*) FROM email_sends')
        emails_sent = cursor.fetchone()[0]
        
        # Categories
        cursor.execute('SELECT DISTINCT category FROM prospects WHERE category IS NOT NULL')
        categories = [row[0] for row in cursor.fetchall()]
        
        # Prospects by status
        cursor.execute('SELECT status, COUNT(*) FROM prospects GROUP BY status')
        status_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_prospects': total_prospects,
            'with_sequences': with_sequences,
            'emails_sent': emails_sent,
            'categories': categories,
            'status_counts': status_counts
        }
