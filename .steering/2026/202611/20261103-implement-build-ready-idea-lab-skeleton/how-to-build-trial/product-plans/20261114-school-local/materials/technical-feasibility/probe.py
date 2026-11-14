"""Design probe only: SQLite operations, not the household application."""
import json,platform,sqlite3,tempfile,hashlib
from pathlib import Path
SCHEMA=(Path(__file__).resolve().parent.parent/'data-model/schema.sql').read_text()
results=[]
def open_db(path):
 c=sqlite3.connect(path,isolation_level=None,timeout=0)
 c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA busy_timeout=0')
 return c
def setup(path):
 c=open_db(path);c.execute('PRAGMA journal_mode=WAL');c.executescript(SCHEMA)
 for key in ['S1','S2']:
  c.execute('BEGIN IMMEDIATE')
  c.execute('INSERT INTO item VALUES(?,1,0)',(key,))
  c.execute('INSERT INTO source VALUES(?,1,?,?,?,?,?,?)',(key,'consent','2026-11-20T08:00:00+09:00','B1','blue bag','father','paper inspected'))
  c.execute('COMMIT')
 return c
def command(c,key,expected,request,payload,changes):
 c.execute('BEGIN IMMEDIATE')
 try:
  previous=c.execute('SELECT payload,result_token FROM command WHERE id=?',(request,)).fetchone()
  if previous:
   if previous[0]!=payload:raise ValueError('command_id_reused')
   c.execute('ROLLBACK');return {'outcome':'repeat','saved_token':previous[1]}
  n=c.execute('UPDATE item SET token=token+1 WHERE id=? AND token=?',(key,expected)).rowcount
  if not n:c.execute('ROLLBACK');return {'outcome':'stale','rows':0}
  changes(c)
  token=c.execute('SELECT token FROM item WHERE id=?',(key,)).fetchone()[0]
  c.execute('INSERT INTO command VALUES(?,?,?,?)',(request,key,payload,token))
  c.execute('COMMIT');return {'outcome':'saved','saved_token':token}
 except BaseException:
  if c.in_transaction:c.execute('ROLLBACK')
  raise

def evidence(c,id='E1',kind='signed',key='S1',rev=1,basis='original observed'):
 c.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,NULL)',(id,key,rev,kind,'father','2026-11-16T19:45:00+09:00',basis))
def revise(c,body='B1'):
 c.execute('INSERT INTO source VALUES(?,2,?,?,?,?,?,?)',('S1','consent','2026-11-19T08:00:00+09:00',body,'blue bag','mother','school change inspected'))
 c.execute('DELETE FROM booking WHERE item_id=?',('S1',));c.execute('UPDATE item SET current_rev=2 WHERE id=?',('S1',))
def accept(c,key='S1',rev=1):
 c.execute('INSERT INTO acceptance VALUES(?,?,?,?,?)',(key,'prepare',rev,'mother','2026-11-18T19:45:00+09:00'))
def book(c,key,start='19:45',end='20:00',rev=1):
 c.execute('INSERT INTO booking VALUES(?,?,?,?,?,?)',(key,'prepare',rev,'mother',f'2026-11-18T{start}:00+09:00',f'2026-11-18T{end}:00+09:00'))
def tokens(c):return c.execute('SELECT id,token FROM item ORDER BY id').fetchall()
def add(name,observed,expected):
 assert observed==expected,(name,observed,expected)
 results.append({'case':name,'expected':expected,'observed':observed,'matched':True})

with tempfile.TemporaryDirectory(prefix='school-design-probe-') as directory:
 root=Path(directory)
 c=setup(root/'current.db')
 command(c,'S1',0,'sign','sign R1',lambda c:evidence(c))
 command(c,'S1',1,'change','deadline R2',revise)
 observed={'current':c.execute('SELECT s.rev,s.due,s.body_key FROM item i JOIN source s ON s.item_id=i.id AND s.rev=i.current_rev WHERE i.id="S1"').fetchone(),'evidence':c.execute('SELECT source_rev,kind FROM evidence').fetchall(),'submitted':c.execute('SELECT count(*) FROM evidence WHERE kind="submitted"').fetchone()[0]}
 add('current R2 keeps R1 signature, not submission',observed,{'current':(2,'2026-11-19T08:00:00+09:00','B1'),'evidence':[(1,'signed')],'submitted':0})
 valid_sql='SELECT count(*) FROM evidence e JOIN source old ON old.item_id=e.item_id AND old.rev=e.source_rev JOIN item i ON i.id=e.item_id JOIN source now ON now.item_id=i.id AND now.rev=i.current_rev WHERE e.kind="signed" AND old.body_key=now.body_key'
 add('same body supports old signature',c.execute(valid_sql).fetchone()[0],1)
 c.execute('BEGIN IMMEDIATE');c.execute('UPDATE source SET body_key="B2" WHERE item_id="S1" AND rev=2');c.execute('COMMIT')
 add('changed body does not support old signature',c.execute(valid_sql).fetchone()[0],0)
 # This direct change is a probe setup, not an allowed application write to an immutable source revision.
 c.close()
 c=setup(root/'stale.db');command(c,'S1',0,'r2','rev2',revise);b=open_db(root/'stale.db')
 initial_a=c.execute('SELECT token FROM item WHERE id="S1"').fetchone()[0];initial_b=b.execute('SELECT token FROM item WHERE id="S1"').fetchone()[0]
 first=command(c,'S1',initial_a,'acceptA','mother accepted',lambda c:accept(c,rev=2))
 second=command(b,'S1',initial_b,'acceptB','stale evidence',lambda c:evidence(c))
 add('same R2 stale token rejects second write',{'first':first,'second':second,'tokens':tokens(c),'accepted':c.execute('SELECT person FROM acceptance').fetchall()},{'first':{'outcome':'saved','saved_token':2},'second':{'outcome':'stale','rows':0},'tokens':[('S1',2),('S2',0)],'accepted':[('mother',)]})
 c.close();b.close()
 c=setup(root/'repeat.db');first=command(c,'S1',0,'lost-response','sign R1',lambda c:evidence(c));second=command(c,'S1',0,'lost-response','sign R1',lambda c:evidence(c,'E2'))
 add('lost successful response does not repeat changes',{'retry':second,'tokens':tokens(c),'evidence':c.execute('SELECT count(*) FROM evidence').fetchone()[0]},{'retry':{'outcome':'repeat','saved_token':1},'tokens':[('S1',1),('S2',0)],'evidence':1})
 try:command(c,'S1',0,'lost-response','different',lambda c:None)
 except ValueError as e:add('same command different payload',str(e),'command_id_reused')
 else:raise AssertionError('payload reuse was accepted')
 c.close()
 c=setup(root/'rollback.db')
 def fail(c):
  evidence(c);evidence(c,'E2',rev=999)
 try:command(c,'S1',0,'partial','two evidence',fail)
 except sqlite3.IntegrityError:
  add('partial transaction rolls back all',{'tokens':tokens(c),'evidence':c.execute('SELECT count(*) FROM evidence').fetchone()[0],'commands':c.execute('SELECT count(*) FROM command').fetchone()[0]},{'tokens':[('S1',0),('S2',0)],'evidence':0,'commands':0})
 else:raise AssertionError('invalid reference was accepted')
 c.close()
 c=setup(root/'booking.db');b=open_db(root/'booking.db')
 def reserve(c,key,start='19:45',end='20:00'):
  accept(c,key);book(c,key,start,end)
 command(c,'S1',0,'book1','S1 1945',lambda c:reserve(c,'S1'))
 try:command(b,'S2',0,'book2','S2 1945',lambda c:reserve(c,'S2'))
 except sqlite3.IntegrityError as e:
  add('different items compete for same person',{'error':str(e),'tokens':tokens(c),'booking':c.execute('SELECT item_id FROM booking').fetchall()},{'error':'overlap','tokens':[('S1',1),('S2',0)],'booking':[('S1',)]})
 else:raise AssertionError('overlap was accepted')
 try:c.execute('UPDATE booking SET start="2026-11-18T19:30:00+09:00"')
 except sqlite3.IntegrityError as e:add('booking UPDATE cannot bypass insertion checks',str(e),'replace_booking_in_transaction')
 else:raise AssertionError('update was accepted')
 c.close();b.close()
 c=setup(root/'adjacent.db');command(c,'S1',0,'a','S1 1930',lambda c:reserve(c,'S1','19:30','19:45'));command(c,'S2',0,'b','S2 1945',lambda c:reserve(c,'S2'))
 add('adjacent slots can both be reserved',c.execute('SELECT count(*) FROM booking').fetchone()[0],2)
 command(c,'S1',1,'change','R2 invalidates old booking',revise)
 add('source change removes only affected booking',{'slots':c.execute('SELECT item_id FROM booking').fetchall(),'source':c.execute('SELECT current_rev FROM item WHERE id="S1"').fetchone()[0]},{'slots':[('S2',)],'source':2})
 c.close()
 c=setup(root/'busy.db');b=open_db(root/'busy.db');c.execute('BEGIN IMMEDIATE')
 try:command(b,'S1',0,'busy-retry','sign R1',lambda c:evidence(c))
 except sqlite3.OperationalError as e:
  add('writer lock is BUSY, not stale rows',{'name':e.sqlite_errorname,'code':e.sqlite_errorcode,'commands':b.execute('SELECT count(*) FROM command').fetchone()[0]},{'name':'SQLITE_BUSY','code':5,'commands':0})
 else:raise AssertionError('second writer acquired lock')
 c.execute('ROLLBACK');add('explicit retry after lock release',command(b,'S1',0,'busy-retry','sign R1',lambda c:evidence(c)),{'outcome':'saved','saved_token':1});c.close();b.close()
 c=setup(root/'constraints.db');command(c,'S1',0,'change','rev2',revise)
 try:command(c,'S2',0,'bad-current','S2 uses other item revision',lambda c:c.execute('UPDATE item SET current_rev=2 WHERE id="S2"'))
 except sqlite3.IntegrityError:add('current revision cannot use another item source',c.execute('SELECT current_rev,token FROM item WHERE id="S2"').fetchone(),(1,0))
 else:raise AssertionError('cross item revision accepted')
 try:command(c,'S1',1,'empty','empty evidence',lambda c:evidence(c,basis=' '))
 except sqlite3.IntegrityError:add('empty evidence basis rejected',c.execute('SELECT count(*) FROM evidence').fetchone()[0],0)
 else:raise AssertionError('empty evidence was accepted')
 c.close()
 c=setup(root/'backup.db');reader=open_db(root/'backup.db');c.execute('BEGIN IMMEDIATE');c.execute('UPDATE item SET token=1 WHERE id="S1"');evidence(c)
 dst=open_db(root/'before.db');reader.backup(dst);dst.close();restored=open_db(root/'before.db')
 add('backup while writing contains committed state only',{'tokens':tokens(restored),'evidence':restored.execute('SELECT count(*) FROM evidence').fetchone()[0],'fk':restored.execute('PRAGMA foreign_key_check').fetchall()},{'tokens':[('S1',0),('S2',0)],'evidence':0,'fk':[]});restored.close()
 c.execute('COMMIT');dst=open_db(root/'after.db');reader.backup(dst);dst.close();restored=open_db(root/'after.db')
 add('backup after commit restores whole state',{'tokens':tokens(restored),'evidence':restored.execute('SELECT count(*) FROM evidence').fetchone()[0],'fk':restored.execute('PRAGMA foreign_key_check').fetchall()},{'tokens':[('S1',1),('S2',0)],'evidence':1,'fk':[]});restored.close();reader.close();c.close()
print(json.dumps({'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'os':platform.system(),'journal_mode':'WAL','busy_timeout_ms':0,'transaction':'BEGIN IMMEDIATE'},'schema_sha256':hashlib.sha256(SCHEMA.encode()).hexdigest(),'method':'sequential interleaving of independent connections; not a load test','cases':results},ensure_ascii=False,indent=2))
