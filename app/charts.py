from database import SessionLocal
from sqlalchemy import text
from decimal import Decimal
from typing import Dict, List, Tuple, Any

def get_chart_data(topic: str) -> dict:
    """
    Get chart data for a specific topic (group question)
    Returns a dictionary where:
    - key: question name
    - value: list of tuples (answer, percentage)
    """
    db = SessionLocal()
    try:
        # Use the stored procedure instead of raw SQL
        query = text("CALL GetGroupQuestionDetails(:topic)")
        results = db.execute(query, {"topic": topic}).fetchall()
        
        # Group the results by question
        chart_data = {}
        for row in results:
            if row.question_name not in chart_data:
                chart_data[row.question_name] = []
            # Convert Decimal to float
            percentage = float(row.percentage) if isinstance(row.percentage, Decimal) else row.percentage
            chart_data[row.question_name].append((row.Answer, percentage))
        
        return chart_data
    finally:
        db.close()