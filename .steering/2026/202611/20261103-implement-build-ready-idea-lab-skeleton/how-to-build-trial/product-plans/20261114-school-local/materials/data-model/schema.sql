PRAGMA foreign_keys = ON;
CREATE TABLE item (
 id TEXT PRIMARY KEY,
 current_rev INTEGER NOT NULL,
 token INTEGER NOT NULL CHECK(token >= 0),
 FOREIGN KEY(id,current_rev) REFERENCES source(item_id,rev) DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE source (
 item_id TEXT NOT NULL REFERENCES item(id) DEFERRABLE INITIALLY DEFERRED,
 rev INTEGER NOT NULL CHECK(rev > 0),
 title TEXT NOT NULL,
 due TEXT NOT NULL,
 body_key TEXT NOT NULL,
 location TEXT NOT NULL CHECK(length(trim(location)) > 0),
 checked_by TEXT NOT NULL CHECK(checked_by IN ('father','mother')),
 basis TEXT NOT NULL CHECK(length(trim(basis)) > 0),
 PRIMARY KEY(item_id,rev)
);
CREATE TABLE response_decision (
 item_id TEXT NOT NULL,
 source_rev INTEGER NOT NULL,
 choice TEXT NOT NULL CHECK(choice IN ('participate','decline','needs_check')),
 actor TEXT NOT NULL CHECK(actor IN ('father','mother')),
 decided_at TEXT NOT NULL,
 basis TEXT NOT NULL CHECK(length(trim(basis)) > 0),
 PRIMARY KEY(item_id,source_rev),
 FOREIGN KEY(item_id,source_rev) REFERENCES source(item_id,rev)
);
CREATE TABLE action_need (
 item_id TEXT NOT NULL,
 source_rev INTEGER NOT NULL,
 action TEXT NOT NULL CHECK(action IN ('prepare','submit')),
 minutes INTEGER CHECK(minutes IS NULL OR minutes > 0),
 basis TEXT NOT NULL CHECK(length(trim(basis)) > 0),
 PRIMARY KEY(item_id,source_rev,action),
 FOREIGN KEY(item_id,source_rev) REFERENCES source(item_id,rev)
);
CREATE TABLE evidence (
 id TEXT PRIMARY KEY,
 item_id TEXT NOT NULL,
 source_rev INTEGER NOT NULL,
 kind TEXT NOT NULL CHECK(kind IN ('signed','carried','submitted','correction')),
 actor TEXT NOT NULL CHECK(actor IN ('father','mother')),
 occurred_at TEXT NOT NULL,
 basis TEXT NOT NULL CHECK(length(trim(basis)) > 0),
 corrects TEXT REFERENCES evidence(id),
 FOREIGN KEY(item_id,source_rev) REFERENCES source(item_id,rev)
);
CREATE TABLE acceptance (
 item_id TEXT NOT NULL,
 action TEXT NOT NULL CHECK(action IN ('prepare','submit')),
 source_rev INTEGER NOT NULL,
 person TEXT NOT NULL CHECK(person IN ('father','mother')),
 accepted_at TEXT NOT NULL,
 PRIMARY KEY(item_id,action),
 UNIQUE(item_id,action,source_rev,person),
 FOREIGN KEY(item_id,source_rev) REFERENCES source(item_id,rev)
);
CREATE TABLE booking (
 item_id TEXT NOT NULL,
 action TEXT NOT NULL,
 source_rev INTEGER NOT NULL,
 person TEXT NOT NULL,
 start TEXT NOT NULL,
 end TEXT NOT NULL CHECK(end > start),
 PRIMARY KEY(item_id,action),
 FOREIGN KEY(item_id,action,source_rev,person) REFERENCES acceptance(item_id,action,source_rev,person)
);
CREATE TRIGGER booking_current BEFORE INSERT ON booking
WHEN NEW.source_rev != (SELECT current_rev FROM item WHERE id=NEW.item_id)
BEGIN SELECT RAISE(ABORT,'stale_source'); END;
CREATE TRIGGER booking_nonoverlap BEFORE INSERT ON booking
WHEN EXISTS(SELECT 1 FROM booking b WHERE b.person=NEW.person AND b.start < NEW.end AND b.end > NEW.start)
BEGIN SELECT RAISE(ABORT,'overlap'); END;
CREATE TRIGGER booking_no_update BEFORE UPDATE ON booking
BEGIN SELECT RAISE(ABORT,'replace_booking_in_transaction'); END;
CREATE TABLE calendar_ref (
 item_id TEXT NOT NULL REFERENCES item(id),
 action TEXT NOT NULL CHECK(action IN ('prepare','submit')),
 marker TEXT NOT NULL UNIQUE,
 target_payload TEXT NOT NULL,
 outcome TEXT NOT NULL CHECK(outcome IN ('in_progress','confirmed','unknown')),
 basis TEXT,
 CHECK(outcome != 'confirmed' OR length(trim(coalesce(basis,''))) > 0),
 PRIMARY KEY(item_id,action)
);
CREATE TABLE command (
 id TEXT PRIMARY KEY,
 item_id TEXT NOT NULL REFERENCES item(id),
 payload TEXT NOT NULL,
 result_token INTEGER NOT NULL
);
