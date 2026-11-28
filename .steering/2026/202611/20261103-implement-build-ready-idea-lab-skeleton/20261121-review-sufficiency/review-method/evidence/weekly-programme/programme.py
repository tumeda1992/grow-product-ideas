from datetime import timedelta, timezone


def publish(ledger, course, start, week):
    occurrence = (course, week)
    if occurrence not in ledger:
        instant = start.astimezone(timezone.utc) + timedelta(weeks=week)
        ledger[occurrence] = instant.astimezone(start.tzinfo)
    return ledger[occurrence]
