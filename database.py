"""SQLite ma'lumotlar bazasi bilan ishlash."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from typing import Iterable, Optional

from config import DB_PATH, TZ

SCHEMA = """
CREATE TABLE IF NOT EXISTS employees (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id       INTEGER NOT NULL UNIQUE,
    username    TEXT,
    tabel       TEXT NOT NULL DEFAULT '',
    full_name   TEXT NOT NULL,
    position    TEXT NOT NULL DEFAULT '',
    phone       TEXT NOT NULL DEFAULT '',
    is_active   INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    report_date TEXT NOT NULL,
    done        TEXT NOT NULL DEFAULT '',
    problems    TEXT NOT NULL DEFAULT '',
    plans       TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    UNIQUE (employee_id, report_date)
);

CREATE INDEX IF NOT EXISTS idx_reports_date ON reports(report_date);

CREATE TABLE IF NOT EXISTS user_settings (
    tg_id INTEGER PRIMARY KEY,
    lang  TEXT NOT NULL DEFAULT 'uz'
);
"""


def _now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        # eski bazalar uchun: yetishmayotgan ustunlarni qo'shish
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(employees)")}
        if "tabel" not in columns:
            conn.execute("ALTER TABLE employees ADD COLUMN tabel TEXT NOT NULL DEFAULT ''")


# ---------------------------------------------------------------- til sozlamasi

def get_lang(tg_id: int) -> str | None:
    with get_conn() as conn:
        row = conn.execute("SELECT lang FROM user_settings WHERE tg_id = ?", (tg_id,)).fetchone()
    return row["lang"] if row else None


def set_lang(tg_id: int, lang: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO user_settings (tg_id, lang) VALUES (?, ?)
               ON CONFLICT(tg_id) DO UPDATE SET lang = excluded.lang""",
            (tg_id, lang),
        )


# ---------------------------------------------------------------- hodimlar

def get_employee(tg_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM employees WHERE tg_id = ?", (tg_id,)).fetchone()


def get_employee_by_id(emp_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()


def add_employee(
    tg_id: int,
    full_name: str,
    position: str,
    phone: str,
    username: str = "",
    tabel: str = "",
) -> int:
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO employees (tg_id, username, tabel, full_name, position, phone, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(tg_id) DO UPDATE SET
                   username  = excluded.username,
                   tabel     = excluded.tabel,
                   full_name = excluded.full_name,
                   position  = excluded.position,
                   phone     = excluded.phone,
                   is_active = 1""",
            (tg_id, username, tabel, full_name, position, phone, _now()),
        )
        row = conn.execute("SELECT id FROM employees WHERE tg_id = ?", (tg_id,)).fetchone()
        return row["id"]


def employee_by_tabel(tabel: str) -> Optional[sqlite3.Row]:
    if not tabel:
        return None
    with get_conn() as conn:
        return conn.execute("SELECT * FROM employees WHERE tabel = ?", (tabel,)).fetchone()


def registered_tabels() -> set[str]:
    with get_conn() as conn:
        rows = conn.execute("SELECT tabel FROM employees WHERE tabel <> ''").fetchall()
    return {row["tabel"] for row in rows}


def list_employees(active_only: bool = True) -> list[sqlite3.Row]:
    sql = "SELECT * FROM employees"
    if active_only:
        sql += " WHERE is_active = 1"
    sql += " ORDER BY full_name COLLATE NOCASE"
    with get_conn() as conn:
        return conn.execute(sql).fetchall()


def set_employee_active(emp_id: int, active: bool) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE employees SET is_active = ? WHERE id = ?", (1 if active else 0, emp_id))


def delete_employee(emp_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM reports WHERE employee_id = ?", (emp_id,))
        conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))


# ---------------------------------------------------------------- hisobotlar

def upsert_report(employee_id: int, report_date: str, done: str, problems: str, plans: str) -> bool:
    """Hisobotni saqlaydi. Yangi qo'shilgan bo'lsa True, tahrirlangan bo'lsa False qaytaradi."""
    now = _now()
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM reports WHERE employee_id = ? AND report_date = ?",
            (employee_id, report_date),
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE reports SET done = ?, problems = ?, plans = ?, updated_at = ?
                   WHERE id = ?""",
                (done, problems, plans, now, existing["id"]),
            )
            return False
        conn.execute(
            """INSERT INTO reports (employee_id, report_date, done, problems, plans, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (employee_id, report_date, done, problems, plans, now, now),
        )
        return True


MERGED_LIMIT = 8000


def _merge_field(old: str, new: str, old_time: str, new_time: str) -> str:
    """Eski matnga yangisini vaqt belgisi bilan qo'shadi."""
    old = (old or "").strip()
    new = (new or "").strip()
    if not new:
        return old
    if not old:
        return f"[{new_time}]\n{new}"
    if not old.startswith("["):  # birinchi qo'shimcha — eski matnga ham vaqt qo'yamiz
        old = f"[{old_time}]\n{old}"
    return f"{old}\n\n[{new_time}]\n{new}"[:MERGED_LIMIT]


def append_report(employee_id: int, report_date: str, done: str, problems: str, plans: str) -> str:
    """Kun davomida hisobotga qo'shimcha yozuv. 'created' yoki 'appended' qaytaradi."""
    now = _now()
    new_time = now[11:16]
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM reports WHERE employee_id = ? AND report_date = ?",
            (employee_id, report_date),
        ).fetchone()

        if row is None:
            conn.execute(
                """INSERT INTO reports (employee_id, report_date, done, problems, plans,
                                        created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (employee_id, report_date, done, problems, plans, now, now),
            )
            return "created"

        old_time = (row["created_at"] or now)[11:16]
        conn.execute(
            """UPDATE reports SET done = ?, problems = ?, plans = ?, updated_at = ?
               WHERE id = ?""",
            (
                _merge_field(row["done"], done, old_time, new_time),
                _merge_field(row["problems"], problems, old_time, new_time),
                _merge_field(row["plans"], plans, old_time, new_time),
                now,
                row["id"],
            ),
        )
        return "appended"


def get_report(employee_id: int, report_date: str) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM reports WHERE employee_id = ? AND report_date = ?",
            (employee_id, report_date),
        ).fetchone()


def get_reports(date_from: str, date_to: str, employee_id: int | None = None) -> list[sqlite3.Row]:
    sql = """
        SELECT r.*, e.full_name, e.position, e.phone, e.tg_id, e.tabel
        FROM reports r
        JOIN employees e ON e.id = r.employee_id
        WHERE r.report_date BETWEEN ? AND ?
    """
    params: list = [date_from, date_to]
    if employee_id:
        sql += " AND r.employee_id = ?"
        params.append(employee_id)
    sql += " ORDER BY r.report_date, e.full_name COLLATE NOCASE"
    with get_conn() as conn:
        return conn.execute(sql, params).fetchall()


def last_reports_of_employee(employee_id: int, limit: int = 7) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """SELECT * FROM reports WHERE employee_id = ?
               ORDER BY report_date DESC LIMIT ?""",
            (employee_id, limit),
        ).fetchall()


def employees_without_report(day: str) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """SELECT e.* FROM employees e
               WHERE e.is_active = 1
                 AND NOT EXISTS (
                     SELECT 1 FROM reports r
                     WHERE r.employee_id = e.id AND r.report_date = ?
                 )
               ORDER BY e.full_name COLLATE NOCASE""",
            (day,),
        ).fetchall()


def stats_by_employee(date_from: str, date_to: str) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """SELECT e.full_name, e.position, e.tabel, COUNT(r.id) AS cnt,
                      MAX(r.report_date) AS last_date
               FROM employees e
               LEFT JOIN reports r
                      ON r.employee_id = e.id AND r.report_date BETWEEN ? AND ?
               WHERE e.is_active = 1
               GROUP BY e.id
               ORDER BY cnt DESC, e.full_name COLLATE NOCASE""",
            (date_from, date_to),
        ).fetchall()


def total_counts(date_from: str, date_to: str) -> tuple[int, int]:
    """(hisobotlar soni, hisobot topshirgan hodimlar soni)"""
    with get_conn() as conn:
        row = conn.execute(
            """SELECT COUNT(*) AS c, COUNT(DISTINCT employee_id) AS e
               FROM reports WHERE report_date BETWEEN ? AND ?""",
            (date_from, date_to),
        ).fetchone()
        return row["c"], row["e"]
