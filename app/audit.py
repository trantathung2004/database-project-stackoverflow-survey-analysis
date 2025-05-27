from sqlalchemy import text
from database import SessionLocal
from typing import List, Dict
from models import AuditLogResponse
from datetime import datetime

def get_audit_logs() -> List[Dict]:
    db = SessionLocal()
    try:
        # Query to get audit logs with username and question name
        query = text("""
            SELECT 
                al.log_id,
                al.response_id,
                al.user_id,
                al.action_type,
                al.action_timestamp,
                al.old_value,
                al.new_value,
                al.question_id,
                u.username,
                q.qname as question_name
            FROM response_audit_log al
            LEFT JOIN Users u ON al.user_id = u.ID
            LEFT JOIN Questions q ON al.question_id = q.QID
            ORDER BY al.action_timestamp DESC
        """)
        
        results = db.execute(query).mappings().all()
        # Convert datetime to string format
        logs = []
        for row in results:
            log_dict = dict(row)
            if isinstance(log_dict['action_timestamp'], datetime):
                log_dict['action_timestamp'] = log_dict['action_timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            logs.append(log_dict)
        return logs
    finally:
        db.close()
