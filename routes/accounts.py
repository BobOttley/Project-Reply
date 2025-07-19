from flask import Blueprint, request, jsonify
import psycopg2
import os

accounts_bp = Blueprint('accounts', __name__)

def get_db_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])

# === SEARCH (Parents/Children) ===
@accounts_bp.route('/api/accounts/search', methods=['GET'])
def search_accounts():
    q = request.args.get('q', '').strip()
    results = []
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            sql = """
                SELECT p.id, p.name, p.email, p.phone, c.id AS child_id, c.name AS child_name,
                       c.year_group, c.interests, e.id AS enquiry_id, e.enquiry_date, e.source
                FROM parents p
                LEFT JOIN children c ON c.parent_id = p.id
                LEFT JOIN enquiries e ON e.parent_id = p.id
            """
            params = []
            filters = []
            if q:
                filters.append("(p.name ILIKE %s OR p.email ILIKE %s OR c.name ILIKE %s)")
                params += [f'%{q}%', f'%{q}%', f'%{q}%']
            if filters:
                sql += " WHERE " + " AND ".join(filters)
            sql += " ORDER BY e.enquiry_date DESC NULLS LAST, p.name ASC LIMIT 50"
            cur.execute(sql, params)
            for row in cur.fetchall():
                results.append(dict(zip(
                    ['id', 'name', 'email', 'phone', 'child_id', 'child_name', 'year_group',
                     'interests', 'enquiry_id', 'enquiry_date', 'source'],
                    row
                )))
    return jsonify(results)

# === ADD NEW PARENT (with optional child and enquiry) ===
@accounts_bp.route('/api/accounts/add', methods=['POST'])
def add_account():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"success": False, "error": "Missing parent name or email"}), 400
    parent_id = None
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            # Insert parent
            cur.execute("""
                INSERT INTO parents (name, email, phone, customer_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                data['name'], data['email'], data.get('phone', None), data.get('customer_id', "LOCAL-TEST")
            ))
            parent_id = cur.fetchone()[0]
            # Insert child if provided
            child_id = None
            if data.get('child_name'):
                cur.execute("""
                    INSERT INTO children (parent_id, name, year_group, interests, customer_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    parent_id, data['child_name'], data.get('year_group', None),
                    data.get('interests', None), data.get('customer_id', "LOCAL-TEST")
                ))
                child_id = cur.fetchone()[0]
            # Insert enquiry if provided
            if data.get('enquiry_date'):
                cur.execute("""
                    INSERT INTO enquiries (parent_id, child_id, enquiry_date, source, raw_text, customer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    parent_id, child_id,
                    data['enquiry_date'], data.get('source', "manual"),
                    data.get('raw_text', None), data.get('customer_id', "LOCAL-TEST")
                ))
        conn.commit()
    return jsonify({"success": True, "parent_id": parent_id})

# === GET FULL ACCOUNT DETAIL ===
@accounts_bp.route('/api/accounts/<int:parent_id>', methods=['GET'])
def get_account(parent_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, p.name, p.email, p.phone, p.customer_id,
                       c.id AS child_id, c.name AS child_name, c.year_group, c.interests,
                       e.id AS enquiry_id, e.enquiry_date, e.source, e.raw_text
                FROM parents p
                LEFT JOIN children c ON c.parent_id = p.id
                LEFT JOIN enquiries e ON e.parent_id = p.id
                WHERE p.id = %s
                ORDER BY e.enquiry_date DESC NULLS LAST
            """, (parent_id,))
            results = [dict(zip(
                ['id', 'name', 'email', 'phone', 'customer_id',
                 'child_id', 'child_name', 'year_group', 'interests',
                 'enquiry_id', 'enquiry_date', 'source', 'raw_text'],
                row
            )) for row in cur.fetchall()]
    return jsonify(results)

# === UPDATE PARENT DETAILS ===
@accounts_bp.route('/api/accounts/<int:parent_id>/update', methods=['POST'])
def update_account(parent_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No update data supplied"}), 400
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE parents SET name=%s, email=%s, phone=%s
                WHERE id=%s
            """, (data.get('name'), data.get('email'), data.get('phone'), parent_id))
        conn.commit()
    return jsonify({"success": True, "parent_id": parent_id})

# === DELETE PARENT (SOFT DELETE BY FLAG OR REALLY REMOVE) ===
@accounts_bp.route('/api/accounts/<int:parent_id>/delete', methods=['POST'])
def delete_account(parent_id):
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM parents WHERE id=%s", (parent_id,))
        conn.commit()
    return jsonify({"success": True})

# === ADD/UPDATE/DELETE ENDPOINTS FOR CHILD AND ENQUIRY (OPTIONAL) ===
# Add if you need child-specific editing, otherwise do via parent.

# === Error Handling Example ===
@accounts_bp.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"success": False, "error": str(e)}), 500
