"""Cross-material Q17 walkthrough against the proposed schema."""
from pathlib import Path
import sqlite3,json,tempfile,hashlib,html
ROOT=Path(__file__).resolve().parent
BODY='折り目は何度使った跡だろう'
def view(c,day,now):
 if not 36000<=now<41100:return []
 return c.execute('''SELECT p.id,p.number,c.title,e.location,p.source,p.body,p.rev,r.epoch
 FROM current_display d JOIN prompt p ON d.prompt_id=p.id AND d.number=p.number
 JOIN catalog c ON c.number=p.number JOIN exhibition e ON e.number=p.number JOIN runtime r
 WHERE r.id=1 AND r.mode='open' AND r.active_day=? AND p.state='active' AND p.body IS NOT NULL''',(day,)).fetchall()
def main():
 obs=[]
 with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
  path=Path(tmp)/'model.sqlite';c=sqlite3.connect(path);c.executescript((ROOT.parent/'data-model/schema.sql').read_text())
  catalog=json.loads((ROOT/'existing-site/catalog.json').read_text())
  c.executemany('INSERT INTO catalog VALUES(?,?,?)',[(r['number'],r['title'],r['shelf']) for r in catalog]);c.executemany('INSERT INTO exhibition VALUES(?,?)',[(17,'左室'),(18,'右室'),(19,'入口壁面')]);c.executemany('INSERT INTO days VALUES(?)',[(d,) for d in ['2026-11-28','2026-11-29']])
  c.execute("INSERT INTO runtime VALUES(1,'2026-11-28','covered',1)")
  c.executemany('INSERT INTO slot(day,number,at) VALUES(?,?,?)',[(d,n,t) for d in ['2026-11-28','2026-11-29'] for n in [17,18,19] for t in [37200,38400,39600,40500]])
  c.execute('INSERT INTO prompt(id,receipt,day,number,body,payload_digest,source,scope,state,rev) VALUES(?,?,?,?,?,?,?,?,?,?)',('Q17','receipt-one','2026-11-28',17,BODY,hashlib.sha256(BODY.encode()).hexdigest(),'visitor','weekend','accepted',1))
  c.execute("UPDATE slot SET prompt_id='Q17' WHERE day='2026-11-28' AND number=17 AND at=37200");c.commit()
  assert c.execute('SELECT day,number,at FROM slot WHERE prompt_id=?',('Q17',)).fetchall()==[('2026-11-28',17,37200)]
  try:
   c.execute("UPDATE slot SET prompt_id='Q17' WHERE day='2026-11-28' AND number=18 AND at=38400");c.commit();raise AssertionError('mismatch accepted')
  except sqlite3.IntegrityError:c.rollback()
  # Use a distinct prompt to isolate composite FK rejection from prompt_id UNIQUE.
  c.execute('INSERT INTO prompt(id,receipt,day,number,body,payload_digest,source,scope,state,rev) VALUES(?,?,?,?,?,?,?,?,?,?)',('Q18','receipt-two','2026-11-28',18,'合成の別の問い','digest','visitor','weekend','accepted',1));c.commit()
  try:
   c.execute("UPDATE slot SET prompt_id='Q18' WHERE day='2026-11-28' AND number=17 AND at=38400");c.commit();raise AssertionError('wrong target accepted')
  except sqlite3.IntegrityError as e: error=str(e);c.rollback()
  assert 'FOREIGN KEY' in error
  obs.append({'claim':'target_and_slot','Q17_reserved':['2026-11-28',17,37200],'Q18_to_17_rejected':error})
  c.execute("INSERT INTO current_display VALUES(17,'Q17')");c.execute("INSERT INTO paper_copy VALUES('Q17-P1','Q17','prepared',NULL,NULL)");c.commit()
  assert view(c,'2026-11-28',37380)==[]
  obs.append({'claim':'before_physical_confirmation','runtime':'covered','new_view':[],'paper':'prepared'})
  # These are synthetic operator confirmations; no physical paper was moved.
  c.execute("UPDATE prompt SET state='active',rev=2 WHERE id='Q17' AND rev=1")
  c.execute("UPDATE paper_copy SET state='placed',operator='B',confirmed_at=37380 WHERE id='Q17-P1'")
  c.execute("UPDATE runtime SET mode='open',epoch=2");c.commit()
  rows=view(c,'2026-11-28',37380);assert rows==[('Q17',17,'袋','左室','visitor',BODY,2,2)]
  render='<article data-question="Q17"><h2>17 袋</h2><p>左室</p><p>来館者の言葉（事実未確認）</p><p>'+html.escape(rows[0][5])+'</p></article>'
  assert 'A1' not in render and '左室' in render
  (ROOT/'synthetic-view-fragment.html').write_text(render)
  stale=c.execute("UPDATE prompt SET state='withdrawn',rev=rev+1 WHERE id='Q17' AND rev=1").rowcount;c.commit();assert stale==0
  obs.append({'claim':'confirmed_view_and_stale_update','payload':rows,'render_location':'左室; shelf A1 not used for display','stale_rows':stale})
  assert view(c,'2026-11-28',41100)==[] and view(c,'2026-11-29',37380)==[]
  c.execute("UPDATE runtime SET mode='covered',epoch=3");c.commit();assert view(c,'2026-11-28',37800)==[]
  assert c.execute("SELECT state FROM paper_copy WHERE id='Q17-P1'").fetchone()==('placed',)
  obs.append({'claim':'withdrawal_before_recovery','new_view':[],'paper_status':'placed; recovery not inferred'})
  c.execute("UPDATE paper_copy SET state='recovered',operator='B',confirmed_at=37800 WHERE id='Q17-P1'")
  c.execute("UPDATE prompt SET state='withdrawn',rev=3,body=NULL WHERE id='Q17' AND rev=2")
  c.execute('UPDATE current_display SET prompt_id=NULL');c.commit();assert view(c,'2026-11-28',37800)==[]
  before=c.execute('SELECT number,title,shelf FROM catalog ORDER BY number').fetchall();assert before==[(17,'袋','A1'),(18,'道具','B2'),(19,'写真','C1')]
  # Complete F0: keep aggregate counts, remove all per-word and receipt records.
  c.execute("INSERT INTO aggregate VALUES('2026-11-28','all','day','accepted_words',2)")
  c.execute('DELETE FROM paper_copy');c.execute('DELETE FROM current_display');c.execute('UPDATE slot SET prompt_id=NULL');c.execute('DELETE FROM prompt');c.execute("UPDATE runtime SET mode='ended',epoch=4");c.commit();c.execute('VACUUM');c.close()
  data=path.read_bytes();assert BODY.encode() not in data
  c=sqlite3.connect(path);counts={t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['prompt','paper_copy','current_display','aggregate']};assert counts=={'prompt':0,'paper_copy':0,'current_display':0,'aggregate':1}
  assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert c.execute('PRAGMA foreign_key_check').fetchall()==[]
  c.close();obs.append({'claim':'F0_final_state','row_counts':counts,'body_bytes_absent_in_this_file':True,'catalog_before_and_after':before,'integrity':'ok','foreign_key_issues':[]})
 out={'observations':obs,'limits':['operator confirmations were synthetic; physical covering/recovery was not performed','proposed SQL and generated HTML fragment; not facility runtime or full browser application','body byte check covers this SQLite file, not external backups or printer storage']}
 (ROOT/'model-observations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
