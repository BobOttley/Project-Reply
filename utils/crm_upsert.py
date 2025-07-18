# utils/crm_upsert.py

from sqlalchemy.orm import Session
from models import Parent, Child
from utils.account_utils import generate_account_number
import datetime

def upsert_parent(session: Session, customer_id: str, parent_data: dict):
    """
    Find or create a Parent by email or name+phone.
    Updates name and phone if changed.
    Returns (parent, is_new)
    """
    email = parent_data.get("parent_email") or parent_data.get("email")
    name = parent_data.get("parent_name") or parent_data.get("name")
    phone = parent_data.get("phone")

    parent = None
    is_new = False

    if email:
        parent = session.query(Parent).filter_by(customer_id=customer_id, email=email).first()

    if not parent and name and phone:
        parent = (
            session.query(Parent)
            .filter_by(customer_id=customer_id, name=name, phone=phone)
            .first()
        )

    if not parent:
        parent = Parent(
            customer_id=customer_id,
            name=name,
            email=email,
            phone=phone,
            account_number=None,
        )
        session.add(parent)
        session.flush()
        parent.account_number = generate_account_number(session, Parent, "P")
        session.commit()
        is_new = True
        print(f"[CRM] New parent added: {name} <{email}>")
    else:
        updated = False
        if name and parent.name != name:
            parent.name = name
            updated = True
        if phone and parent.phone != phone:
            parent.phone = phone
            updated = True
        if updated:
            session.add(parent)
            session.commit()
            print(f"[CRM] Updated parent info: {name} <{email}>")

    return parent, is_new

def upsert_child(session: Session, customer_id: str, parent_id: int, child_data: dict):
    """
    Find or create a Child by parent_id + name + dob.
    Updates year_group and interests if changed.
    Returns (child, is_new)
    """
    name = child_data.get("child_name") or child_data.get("name")
    dob_raw = child_data.get("dob")
    dob = None
    if dob_raw:
        try:
            if isinstance(dob_raw, str):
                dob = datetime.datetime.fromisoformat(dob_raw)
            elif isinstance(dob_raw, datetime.datetime):
                dob = dob_raw
        except Exception:
            dob = None

    year_group = child_data.get("child_year_group") or child_data.get("year_group")
    interests = child_data.get("interests")

    query = session.query(Child).filter_by(parent_id=parent_id, name=name)
    if dob:
        query = query.filter(Child.dob == dob)
    child = query.first()
    is_new = False

    if not child:
        child = Child(
            parent_id=parent_id,
            name=name,
            dob=dob,
            year_group=year_group,
            interests=interests,
            account_number=None
        )
        session.add(child)
        session.flush()
        child.account_number = generate_account_number(session, Child, "C")
        session.commit()
        is_new = True
        print(f"[CRM] New child added: {name} (Parent ID {parent_id})")
    else:
        updated = False
        if year_group and child.year_group != year_group:
            child.year_group = year_group
            updated = True
        if interests and child.interests != interests:
            child.interests = interests
            updated = True
        if updated:
            session.add(child)
            session.commit()
            print(f"[CRM] Updated child info: {name} (Parent ID {parent_id})")

    return child, is_new
