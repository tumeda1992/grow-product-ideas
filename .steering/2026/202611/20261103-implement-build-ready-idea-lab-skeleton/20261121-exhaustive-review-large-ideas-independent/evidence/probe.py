"""Review probes for constructed opportunity sets and a local SQLite update."""
import itertools
import json
import platform
import sqlite3


def invitations(disjoint_days):
    slots = {"prior": list("abcde"), "late": list("fghi")}
    results = []
    for wed, fri in itertools.product(slots, repeat=2):
        groups = [set(slots[wed]), set(slots[fri])]
        if disjoint_days:
            groups[1] = {x.upper() for x in groups[1]}
        results.append({
            "days": [wed, fri],
            "opportunities": sum(map(len, groups)),
            "distinct": len(groups[0] | groups[1]),
        })
    return results


def conditional_update():
    address = "file:studio_probe?mode=memory&cache=shared"
    first = sqlite3.connect(address, uri=True, isolation_level=None)
    second = sqlite3.connect(address, uri=True, isolation_level=None)
    try:
        first.execute("CREATE TABLE slot(id TEXT PRIMARY KEY, rev INTEGER, claimed_by TEXT)")
        first.execute("INSERT INTO slot VALUES ('R7',1,NULL)")
        query = "SELECT id, rev, claimed_by FROM slot WHERE id='R7'"
        reads = [connection.execute(query).fetchone() for connection in (first, second)]
        claim = """UPDATE slot SET rev=rev+1, claimed_by=?
                   WHERE id='R7' AND rev=? AND claimed_by IS NULL"""
        rows = [
            first.execute(claim, ("p1", reads[0][1])).rowcount,
            second.execute(claim, ("p2", reads[1][1])).rowcount,
        ]
        after = first.execute(query).fetchone()
        first.execute("UPDATE slot SET rev=rev+1, claimed_by=NULL WHERE id='R7' AND rev=2")
        stale = second.execute(claim, ("p2", 2)).rowcount
        fresh = second.execute(claim, ("p2", 3)).rowcount
        final = first.execute(query).fetchone()
        assert rows == [1, 0] and after == ("R7", 2, "p1")
        assert stale == 0 and fresh == 1 and final == ("R7", 4, "p2")
        return dict(reads=reads, rows=rows, after=after, stale=stale, fresh=fresh, final=final)
    finally:
        second.close()
        first.close()


if __name__ == "__main__":
    repeated, separate = invitations(False), invitations(True)
    assert [case["distinct"] for case in repeated] == [5, 9, 9, 4]
    assert [case["distinct"] for case in separate] == [10, 9, 9, 8]
    print(json.dumps(dict(python=platform.python_version(), sqlite=sqlite3.sqlite_version,
                          same_groups=repeated, disjoint_days=separate,
                          update=conditional_update()), ensure_ascii=False, indent=2))
