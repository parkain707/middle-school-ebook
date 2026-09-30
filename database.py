import sqlite3
import os
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ebook_system.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS book_meta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price INTEGER NOT NULL,
        price_unit TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        total_pages INTEGER NOT NULL,
        publisher TEXT NOT NULL,
        description TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_num INTEGER,
        subject TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT,
        content TEXT NOT NULL,
        page_start INTEGER
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        buyer_name TEXT NOT NULL,
        buyer_email TEXT NOT NULL,
        buyer_phone TEXT,
        price INTEGER NOT NULL,
        price_unit TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL,
        access_token TEXT UNIQUE,
        created_at TEXT NOT NULL,
        approved_at TEXT,
        download_count INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    
    # 메타데이터 주입
    cur.execute("DELETE FROM book_meta")
    cur.execute("""
    INSERT INTO book_meta (title, author, price, price_unit, payment_method, total_pages, publisher, description, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "꿈을 여는 공부의 새벽: 중학교 첫 시험 전교 1등 시크릿",
        "6학년 3반 담임 선생님",
        70000,
        "미소",
        "경제앱으로 박희망에게 입금",
        44,
        "6학년 3반 교실 연구소",
        "초등 6학년부터 시작하는 10대 전 과목 자기주도 학습 및 중등 성적 역전 전자책",
        datetime.now().isoformat()
    ))
    
    # 원고 파싱 및 적재
    manuscript_path = os.path.join(BASE_DIR, "ebook_manuscript.md")
    if os.path.exists(manuscript_path):
        cur.execute("DELETE FROM chapters")
        with open(manuscript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        cur_subject = "도입부"
        cur_title = "표지 및 프롤로그"
        cur_content = []
        chap_num = 1
        
        for line in lines:
            if line.startswith("## Part") or line.startswith("### "):
                if cur_content:
                    cur.execute("""
                    INSERT INTO chapters (chapter_num, subject, title, content)
                    VALUES (?, ?, ?, ?)
                    """, (chap_num, cur_subject, cur_title, "".join(cur_content)))
                    chap_num += 1
                    cur_content = []
                cur_title = line.strip("# \n")
                if "국어" in cur_title: cur_subject = "국어"
                elif "영어" in cur_title: cur_subject = "영어"
                elif "수학" in cur_title: cur_subject = "수학"
                elif "과학" in cur_title: cur_subject = "과학"
                elif "사회" in cur_title or "역사" in cur_title: cur_subject = "사회/역사"
                elif "도덕" in cur_title: cur_subject = "도덕"
                elif "기술" in cur_title or "가정" in cur_title: cur_subject = "기술가정"
                elif "정보" in cur_title: cur_subject = "정보"
                elif "한문" in cur_title: cur_subject = "한문"
                elif "음악" in cur_title or "미술" in cur_title or "체육" in cur_title: cur_subject = "음미체"
            cur_content.append(line)
            
        if cur_content:
            cur.execute("""
            INSERT INTO chapters (chapter_num, subject, title, content)
            VALUES (?, ?, ?, ?)
            """, (chap_num, cur_subject, cur_title, "".join(cur_content)))
            
    conn.commit()
    conn.close()

def create_order(buyer_name, buyer_email, buyer_phone=""):
    conn = get_connection()
    cur = conn.cursor()
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    token = f"tok_{uuid.uuid4().hex}"
    
    cur.execute("""
    INSERT INTO orders (order_id, buyer_name, buyer_email, buyer_phone, price, price_unit, payment_method, status, access_token, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
    """, (order_id, buyer_name, buyer_email, buyer_phone, 70000, "미소", "경제앱으로 박희망에게 입금", token, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    return order_id, token

def approve_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    now_str = datetime.now().isoformat()
    cur.execute("""
    UPDATE orders 
    SET status = 'APPROVED', approved_at = ?
    WHERE order_id = ?
    """, (now_str, order_id))
    
    cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return dict(row) if row else None

def get_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def verify_token(token):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE access_token = ? AND status = 'APPROVED'", (token,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE orders SET download_count = download_count + 1 WHERE access_token = ?", (token,))
        conn.commit()
        cur.execute("SELECT * FROM orders WHERE access_token = ?", (token,))
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == "__main__":
    init_db()
    print("DATABASE_INITIALIZED_WITH_FULL_CHAPTERS")
