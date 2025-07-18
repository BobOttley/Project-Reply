import datetime
from sqlalchemy.orm import Session

def generate_account_number(session: Session, model, prefix: str) -> str:
    """
    Generate a unique account number with format PREFIX-YYYYMMDD-XXX
    where XXX is a zero-padded sequence number for that day.
    """
    today_str = datetime.datetime.utcnow().strftime("%Y%m%d")
    like_pattern = f"{prefix}-{today_str}-%"

    # Query max existing account_number for today
    last = (
        session.query(model)
        .filter(model.account_number.like(like_pattern))
        .order_by(model.account_number.desc())
        .first()
    )

    if last and last.account_number:
        try:
            last_seq = int(last.account_number.split("-")[-1])
        except Exception:
            last_seq = 0
    else:
        last_seq = 0

    next_seq = last_seq + 1
    return f"{prefix}-{today_str}-{next_seq:03d}"
