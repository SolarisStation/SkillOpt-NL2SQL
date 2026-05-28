import re

def normalize_sql(sql: str) -> str:
    """Normalize SQL for comparison: lowercase, strip, remove semicolons and markdown."""
    # Remove markdown code blocks
    sql = re.sub(r'```sql\s*(.*?)\s*```', r'\1', sql, flags=re.DOTALL | re.IGNORECASE)
    sql = re.sub(r'```\s*(.*?)\s*```', r'\1', sql, flags=re.DOTALL)
    # Extract from <answer> tags if present
    match = re.search(r'<answer>(.*?)</answer>', sql, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1)
    
    sql = sql.lower().strip()
    sql = sql.replace(';', '')
    sql = re.sub(r'\s+', ' ', sql)
    return sql

def evaluate(prediction: str, gold_answers: list[str]) -> dict:
    """Evaluate SQL prediction against gold answers."""
    pred_norm = normalize_sql(prediction)
    em = 0.0
    for gold in gold_answers:
        if pred_norm == normalize_sql(gold):
            em = 1.0
            break
            
    return {
        "em": em,
        "f1": em,  # SQL is binary
        "sub_em": em,
        "predicted_answer": pred_norm
    }
