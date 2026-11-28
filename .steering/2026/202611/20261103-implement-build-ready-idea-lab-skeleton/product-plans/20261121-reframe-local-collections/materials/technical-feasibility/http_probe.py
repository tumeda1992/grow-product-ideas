"""Finite local HTTP/SQLite experiment. Not the product application."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
import sqlite3, json, threading, urllib.request, urllib.error, tempfile
ROOT=Path(__file__).resolve().parent

def connect(db):
 c=sqlite3.connect(db,timeout=5);c.execute('PRAGMA secure_delete=ON');return c

def handler(db,viewer):
 class H(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def send_json(self,code,value):
   data=json.dumps(value,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  def do_GET(self):
   with connect(db) as c:
    if self.path=='/view':
     rows=c.execute("SELECT id,number,body,state,rev FROM prompt WHERE state='active' AND expires>100 AND (SELECT closed FROM event)=0").fetchall();self.send_json(200,rows)
    elif not viewer and self.path=='/item':self.send_json(200,c.execute('SELECT id,body,state,rev FROM prompt').fetchall())
    else:self.send_json(404,{})
  def do_POST(self):
   if viewer:self.send_json(405,{'error':'read_only'});return
   x=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
   c=connect(db)
   try:
    c.execute('BEGIN IMMEDIATE')
    if c.execute('SELECT closed FROM event').fetchone()[0]:c.rollback();self.send_json(410,{'error':'period_closed'});return
    if self.path=='/receive':
     payload=json.dumps(x,sort_keys=True,ensure_ascii=False)
     row=c.execute('SELECT id,payload FROM prompt WHERE receipt=?',(x['receipt'],)).fetchone()
     if row:
      c.commit();self.send_json(200 if row[1]==payload else 409,{'id':row[0],'result':'same_receipt' if row[1]==payload else 'receipt_conflict'});return
     c.execute('INSERT INTO prompt VALUES(?,?,?,?,?,?,?,?,?)',('Q17',x['receipt'],17,x['body'],payload,'pending',1,200,'visitor_question'));c.commit();self.send_json(201,{'id':'Q17'});return
    if self.path=='/change':
     n=c.execute('UPDATE prompt SET state=?,rev=rev+1 WHERE id=? AND rev=?',(x['state'],x['id'],x['rev'])).rowcount;c.commit();self.send_json(200 if n==1 else 409,{'changed':n});return
    c.rollback();self.send_json(404,{})
   finally:c.close()
 return H

def request(base,path,payload=None):
 req=urllib.request.Request(base+path,data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req) as r:return r.status,json.load(r),r.headers.get('Cache-Control')
 except urllib.error.HTTPError as e:return e.code,json.load(e),e.headers.get('Cache-Control')

def main():
 obs=[]
 with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
  db=Path(tmp)/'test.sqlite';c=connect(db)
  c.executescript('PRAGMA journal_mode=DELETE; CREATE TABLE event(closed INTEGER);INSERT INTO event VALUES(0); CREATE TABLE prompt(id TEXT PRIMARY KEY,receipt TEXT UNIQUE,number INTEGER,body TEXT,payload TEXT,state TEXT,rev INTEGER,expires INTEGER,source TEXT);');c.commit();c.close()
  servers=[ThreadingHTTPServer(('127.0.0.1',0),handler(db,v)) for v in [False,True]]
  threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in servers]
  for t in threads:t.start()
  admin,viewer=['http://127.0.0.1:'+str(s.server_port) for s in servers]
  body='合成の問い：折り目は何度使った跡だろう';payload={'receipt':'synthetic-receipt-one','body':body}
  with ThreadPoolExecutor(max_workers=2) as pool: received=list(pool.map(lambda _:request(admin,'/receive',payload),range(2)))
  c=connect(db);rows=c.execute('SELECT COUNT(*),MIN(rev),MAX(rev) FROM prompt').fetchone();c.close()
  assert sorted(r[0] for r in received)==[200,201] and rows==(1,1,1)
  changed=request(admin,'/receive',dict(payload,body='different'));assert changed[0]==409
  obs.append({'claim':'simultaneous_receipt','responses':received,'db_count_and_revisions':rows,'different_body_response':changed[0]})
  before=[request(admin,'/item')[1] for _ in range(2)];assert before[0][0][-1]==before[1][0][-1]==1
  with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(lambda state:request(admin,'/change',{'id':'Q17','rev':1,'state':state}),['active','withdrawn']))
  c=connect(db);state,rev=c.execute('SELECT state,rev FROM prompt').fetchone();c.close()
  assert sorted(r[0] for r in results)==[200,409] and rev==2
  obs.append({'claim':'simultaneous_stale_updates','starting_revisions':[1,1],'responses':results,'db_state_and_revision':[state,rev]})
  request(admin,'/change',{'id':'Q17','rev':2,'state':'active'})
  active=request(viewer,'/view');assert active[0]==200 and len(active[1])==1 and active[2]=='no-store'
  forbidden=request(viewer,'/receive',payload);assert forbidden[0]==405
  request(admin,'/change',{'id':'Q17','rev':3,'state':'withdrawn'})
  withdrawn=request(viewer,'/view');assert withdrawn[1]==[]
  c=connect(db);c.execute("UPDATE prompt SET state='active',expires=100");c.commit();c.close();expired=request(viewer,'/view');assert expired[1]==[]
  obs.append({'claim':'viewer_boundary','active_rows':len(active[1]),'cache_control':active[2],'post_status':forbidden[0],'withdrawn_rows':withdrawn[1],'expired_rows':expired[1]})
  c=connect(db);c.execute('UPDATE event SET closed=1');c.execute("UPDATE prompt SET body=NULL,payload=NULL,state='expired',rev=rev+1");c.commit();c.execute('VACUUM');c.close()
  after=request(admin,'/item');closed=request(admin,'/receive',payload)
  assert after[1][0][1] is None and closed[0]==410
  data=db.read_bytes();assert body.encode() not in data and b'different' not in data
  obs.append({'claim':'purge_after_close','logical_rows':after[1],'replay_status':closed[0],'synthetic_body_bytes_absent':True,'metadata_row_retained':True,'boundary':'this closed SQLite file only; no OS backup or printed copy guarantee'})
  for s in servers:s.shutdown();s.server_close()
 result={'observations':obs,'limits':['localhost HTTP only; no facility LAN or real browser test','physical covering and paper recovery not automated or observed','finite SQL/HTTP protocol experiment; not product implementation']}
 (ROOT/'http-observations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
