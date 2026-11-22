"""Synthetic evidence probe; not production application code."""
from pathlib import Path
import sqlite3, tempfile, subprocess, sys, json, hashlib, html, importlib.util
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent

def open_db(path):
 c=sqlite3.connect(path,timeout=1); c.execute('PRAGMA foreign_keys=ON'); return c

def schema(c):
 c.executescript('''CREATE TABLE prompt(id TEXT PRIMARY KEY,receipt TEXT UNIQUE NOT NULL,number INTEGER NOT NULL,body TEXT NOT NULL,source TEXT NOT NULL,scope TEXT NOT NULL,state TEXT NOT NULL,rev INTEGER NOT NULL,expires INTEGER NOT NULL);''');c.commit()

def receive(c, receipt, body):
 row=c.execute('SELECT id,body FROM prompt WHERE receipt=?',(receipt,)).fetchone()
 if row:
  if row[1]!=body: return {'result':'receipt_conflict'}
  return {'result':'same_receipt','id':row[0]}
 c.execute('INSERT INTO prompt VALUES(?,?,?,?,?,?,?,?,?)',('Q17',receipt,17,body,'visitor_question','weekend_only','pending',1,200));c.commit()
 return {'result':'received','id':'Q17'}

def visible(c,now):
 return c.execute("SELECT id,number,body,source,rev FROM prompt WHERE state='active' AND expires>? ORDER BY id",(now,)).fetchall()

def main():
 records=[]
 with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
  db=Path(tmp)/'synthetic.sqlite'; a=open_db(db);schema(a)
  spec=importlib.util.spec_from_file_location('packing',ROOT/'existing-site/scripts/packing_list.py');packing=importlib.util.module_from_spec(spec);spec.loader.exec_module(packing)
  before=packing.packing_list(ROOT/'existing-site'); cataloghash=hashlib.sha256((ROOT/'existing-site/catalog.json').read_bytes()).hexdigest()
  body='折り目は何度使った跡だろう'; received=receive(a,'receipt-one',body)
  assert before==[(17,'A1'),(18,'B2'),(19,'C1')]
  assert all(type(n) is int for n,s in before)
  b=open_db(db); ar=a.execute("SELECT rev FROM prompt WHERE id='Q17'").fetchone()[0];br=b.execute("SELECT rev FROM prompt WHERE id='Q17'").fetchone()[0]
  na=a.execute("UPDATE prompt SET state='active',rev=rev+1 WHERE id='Q17' AND rev=?",(ar,)).rowcount;a.commit()
  nb=b.execute("UPDATE prompt SET state='withdrawn',rev=rev+1 WHERE id='Q17' AND rev=?",(br,)).rowcount;b.commit()
  current=b.execute("SELECT state,rev FROM prompt WHERE id='Q17'").fetchone()
  assert (na,nb,current)==(1,0,('active',2))
  records.append({'claim':'two_connections_old_revision','read_revisions':[ar,br],'first_rows':na,'stale_rows':nb,'current':current})
  assert visible(b,100)==[('Q17',17,body,'visitor_question',2)]
  n=b.execute("UPDATE prompt SET state='withdrawn',rev=rev+1 WHERE id='Q17' AND rev=2").rowcount;b.commit();assert n==1 and visible(a,100)==[]
  records.append({'claim':'withdrawal_new_reads','state':a.execute("SELECT state,rev FROM prompt").fetchall(),'new_read':visible(a,100)})
  replay=receive(b,'receipt-one',body);conflict=receive(b,'receipt-one','別の内容');assert replay=={'result':'same_receipt','id':'Q17'} and conflict=={'result':'receipt_conflict'}
  assert a.execute('SELECT COUNT(*) FROM prompt').fetchone()[0]==1
  records.append({'claim':'response_lost_then_replay','replay':replay,'changed_payload':conflict,'row_count':1})
  # Child process exits without connection cleanup, first before, then after commit.
  for commit in [False,True]:
   code="import sqlite3,os; c=sqlite3.connect("+repr(str(db))+"); c.execute(\"UPDATE prompt SET state='active',rev=rev+1 WHERE id='Q17'\"); "+('c.commit(); ' if commit else '')+'os._exit(0)'
   subprocess.run([sys.executable,'-c',code],check=True)
   value=a.execute("SELECT state,rev FROM prompt WHERE id='Q17'").fetchone()
   assert value==(('active',4) if commit else ('withdrawn',3))
   records.append({'claim':'process_exit_after_commit' if commit else 'process_exit_before_commit','observed':value})
  assert visible(a,199) and visible(a,200)==[]
  a.execute("UPDATE prompt SET state='pending',rev=rev+1 WHERE id='Q17'");a.commit();assert visible(b,100)==[]
  records.append({'claim':'expiry_and_pending','active_before_200':True,'active_at_200':False,'pending_new_read':[]})
  injected='<script>alert("synthetic")</script>\n袋 & "問い"'; escaped=html.escape(injected,quote=True)
  class Parser(HTMLParser):
   def __init__(self):super().__init__();self.tags=[];self.text=[]
   def handle_starttag(self,tag,attrs): self.tags.append(tag)
   def handle_data(self,data):self.text.append(data)
  parser=Parser();parser.feed('<p>'+escaped+'</p>');assert parser.tags==['p'] and ''.join(parser.text)==injected
  records.append({'claim':'html_escape','tags':parser.tags,'roundtrip_text_matches':True,'escaped':escaped})
  after=packing.packing_list(ROOT/'existing-site');assert before==after
  records.append({'claim':'existing_packing_contract','before':before,'after':after,'catalog_sha256':cataloghash})
  a.close();b.close()
 out={'environment':{'python':sys.version.split()[0],'sqlite':sqlite3.sqlite_version},'observations':records,'limits':['synthetic SQLite and generated HTML only','not a browser, physical display or paper recall test','no facility or production network connections','not production implementation']}
 (ROOT/'observations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
