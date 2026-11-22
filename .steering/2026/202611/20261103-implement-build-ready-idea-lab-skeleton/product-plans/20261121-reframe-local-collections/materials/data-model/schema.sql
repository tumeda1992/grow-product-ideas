PRAGMA foreign_keys=ON;
PRAGMA journal_mode=DELETE;
PRAGMA secure_delete=ON;
CREATE TABLE catalog(number INTEGER PRIMARY KEY, title TEXT NOT NULL, shelf TEXT NOT NULL);
CREATE TABLE exhibition(number INTEGER PRIMARY KEY REFERENCES catalog(number), location TEXT NOT NULL);
CREATE TABLE days(day TEXT PRIMARY KEY);
CREATE TABLE runtime(id INTEGER PRIMARY KEY CHECK(id=1), active_day TEXT REFERENCES days(day), mode TEXT NOT NULL CHECK(mode IN('covered','open','ended')), epoch INTEGER NOT NULL);
CREATE TABLE prompt(
 id TEXT PRIMARY KEY, receipt TEXT UNIQUE NOT NULL, day TEXT NOT NULL REFERENCES days(day),
 number INTEGER NOT NULL REFERENCES catalog(number), body TEXT, payload_digest TEXT,
 source TEXT NOT NULL CHECK(source IN('visitor','operator')), scope TEXT NOT NULL CHECK(scope='weekend'),
 state TEXT NOT NULL CHECK(state IN('accepted','active','retired','withdrawn','unprovided')),
 rev INTEGER NOT NULL CHECK(rev>=1),
 CHECK(state NOT IN('accepted','active') OR body IS NOT NULL), UNIQUE(id,day,number)
);
CREATE TABLE slot(
 day TEXT NOT NULL REFERENCES days(day), number INTEGER NOT NULL REFERENCES catalog(number),
 at INTEGER NOT NULL CHECK(at IN(37200,38400,39600,40500)), prompt_id TEXT UNIQUE,
 PRIMARY KEY(day,number,at),
 FOREIGN KEY(prompt_id,day,number) REFERENCES prompt(id,day,number)
);
CREATE TABLE current_display(number INTEGER PRIMARY KEY REFERENCES catalog(number), prompt_id TEXT UNIQUE REFERENCES prompt(id));
CREATE TABLE paper_copy(id TEXT PRIMARY KEY,prompt_id TEXT NOT NULL REFERENCES prompt(id),state TEXT NOT NULL CHECK(state IN('prepared','placed','recovered')),operator TEXT CHECK(operator IN('A','B')),confirmed_at INTEGER);
CREATE TABLE aggregate(day TEXT NOT NULL,room TEXT NOT NULL,window TEXT NOT NULL,metric TEXT NOT NULL,n INTEGER NOT NULL CHECK(n>=0),PRIMARY KEY(day,room,window,metric));
