"""Local model checks for the data handoff; no external API is contacted."""
import json
import sqlite3
import tempfile
from pathlib import Path


def run():
    checks = []

    def observe(name, value, expected):
        assert value == expected, (name, value, expected)
        checks.append({"claim": name, "observed": value, "expected": expected})

    with tempfile.TemporaryDirectory(prefix="structure90-") as tmp:
        path = Path(tmp) / "model.sqlite"
        with sqlite3.connect(path) as first, sqlite3.connect(path) as second:
            first.executescript("""
                CREATE TABLE sources (id TEXT PRIMARY KEY, revision INTEGER NOT NULL);
                CREATE TABLE jobs (
                    id TEXT PRIMARY KEY, source_id TEXT NOT NULL,
                    target_revision INTEGER NOT NULL, status TEXT NOT NULL,
                    owner TEXT, external_id TEXT
                );
                INSERT INTO sources VALUES ('S1', 1);
                INSERT INTO jobs VALUES ('J1','S1',1,'pending',NULL,NULL);
                INSERT INTO jobs VALUES ('J2','S1',1,'pending',NULL,NULL);
            """)
            first.commit()
            both = [db.execute("SELECT status FROM jobs WHERE id='J1'").fetchone()[0]
                    for db in (first, second)]
            observe("two readers see the same pending request", both, ["pending", "pending"])
            claim = """
                UPDATE jobs SET status='processing', owner=?
                WHERE id=? AND status='pending'
                  AND target_revision=(SELECT revision FROM sources WHERE id=jobs.source_id)
            """
            acquired = []
            for db, owner in ((first, "worker-a"), (second, "worker-b")):
                acquired.append(db.execute(claim, (owner, "J1")).rowcount)
                db.commit()
            observe("conditional claim with first writer committed", acquired, [1, 0])

            # Negative control: identical prior reads do not make an unconditional write safe.
            unsafe = []
            for db, owner in ((first, "worker-a"), (second, "worker-b")):
                unsafe.append(db.execute("UPDATE jobs SET owner=? WHERE id='J2'", (owner,)).rowcount)
                db.commit()
            observe("unconditional claim accepts both writers", unsafe, [1, 1])

            first.execute("UPDATE jobs SET status='unknown' WHERE id='J1'")
            first.commit()
            row = second.execute("SELECT status, external_id FROM jobs WHERE id='J1'").fetchone()
            observe("missing external id does not change unknown into pending", list(row), ["unknown", None])

            first.execute("UPDATE sources SET revision=2 WHERE id='S1'")
            first.execute("UPDATE jobs SET status='confirmed', external_id='E1' WHERE id='J1'")
            first.commit()
            history = second.execute("SELECT target_revision, external_id FROM jobs WHERE id='J1'").fetchall()
            observe("confirmed old result is retained as revision-1 history", [list(x) for x in history], [[1, "E1"]])
            current = second.execute("""
                SELECT j.external_id FROM jobs j JOIN sources s ON s.id=j.source_id
                WHERE j.id='J1' AND j.status='confirmed' AND j.target_revision=s.revision
            """).fetchall()
            observe("revision-2 current view excludes revision-1 success", current, [])
            unsafe_current = second.execute("SELECT external_id FROM jobs WHERE id='J1' AND status='confirmed'").fetchall()
            observe("reader without revision condition leaks old success", [list(x) for x in unsafe_current], [["E1"]])

    return {
        "scope": "controlled SQLite model interleaving, not a production runtime or external API",
        "sqlite_version": sqlite3.sqlite_version,
        "transaction_condition": "both readers read outside an explicit transaction; first update commits before second update",
        "checks": checks,
        "unverified": ["external idempotency and reconciliation", "old worker effects after claim expiry", "other transaction schedules", "actual host and running cost"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
