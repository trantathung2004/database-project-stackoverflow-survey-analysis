from app.database import SessionLocal
from sqlalchemy import text
from decimal import Decimal

def get_chart_data(topic: str) -> dict:
    """
    Get chart data for a specific topic (group question)
    Returns a dictionary where:
    - key: question name
    - value: list of tuples (answer, percentage)
    """
    db = SessionLocal()
    try:
        # Get all questions and their answer counts for the given topic using the view
        query = text("""
            WITH question_totals AS (
                SELECT q.QID, SUM(v.num_responses) as total_responses
                FROM v_question_summary v
                JOIN questions q ON v.QID = q.QID
                JOIN groupquestions g ON q.GID = g.GID
                WHERE g.GroupQuestion = :topic
                GROUP BY q.QID
            )
            SELECT 
                q.qname,
                v.Answer,
                ROUND((v.num_responses * 100.0 / qt.total_responses), 2) as percentage
            FROM v_question_summary v
            JOIN questions q ON v.QID = q.QID
            JOIN groupquestions g ON q.GID = g.GID
            JOIN question_totals qt ON q.QID = qt.QID
            WHERE g.GroupQuestion = :topic
            ORDER BY q.qname, percentage DESC
        """)
        
        results = db.execute(query, {"topic": topic}).fetchall()
        
        # Group the results by question
        chart_data = {}
        for row in results:
            if row.qname not in chart_data:
                chart_data[row.qname] = []
            # Convert Decimal to float
            percentage = float(row.percentage) if isinstance(row.percentage, Decimal) else row.percentage
            chart_data[row.qname].append((row.Answer, percentage))
        
        return chart_data
    finally:
        db.close()
