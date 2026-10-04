"""Turn MySQL's sample 'world' database dump (world.sql) into an SQLite file (world.db).

Source: https://downloads.mysql.com/docs/world-db.zip (the same 'world' data loaded into MySQL in the Video).
Only MySQL-specific bits are stripped; the tables and rows are unchanged.
"""
import re
import sqlite3
from pathlib import Path

here = Path(__file__).parent
sql = (here / "world.sql").read_text(encoding="utf-8")

statements = []
for block in re.findall(r"CREATE TABLE .*?\) ENGINE=[^;]*;", sql, flags=re.S):
    lines = [l for l in block.splitlines() if not re.match(r"\s*(KEY|CONSTRAINT)\b", l)]
    block = "\n".join(lines)
    block = re.sub(r"enum\([^)]*\)", "TEXT", block)        # SQLite has no enum type
    block = block.replace(" AUTO_INCREMENT", "")
    block = re.sub(r",?\s*\n\) ENGINE=[^;]*;", "\n);", block)  # drop the MySQL table options
    statements.append(block)
statements += [l.replace("\\'", "''") for l in sql.splitlines() if l.startswith("INSERT INTO")]

db = here / "world.db"
db.unlink(missing_ok=True)
with sqlite3.connect(db) as conn:
    conn.executescript("\n".join(statements))
    for t in ("city", "country", "countrylanguage"):
        print(t, conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
