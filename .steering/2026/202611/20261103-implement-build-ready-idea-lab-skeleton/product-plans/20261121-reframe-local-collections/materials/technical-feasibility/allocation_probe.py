"""Candidate s1 allocation, finite SQLite experiment; not a production app."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sqlite3, tempfile, json
ROOT=Path(__file__).resolve().parent
TIMES=[37200,38400,39600,40500]
def setup(path,one=False):
 c=sqlite3.connect(path);c.executescript('CREATE TABLE slot(number INTEGER,t INTEGER,receipt TEXT UNIQUE,PRIMARY KEY(number,t));')
 c.executemany('INSERT INTO slot(number,t) VALUES(?,?)',[(17,40500)] if one else [(n,t) for n in [17,18,19] for t in TIMES]);c.commit();c.close()
def reserve(path,receipt,number,now):
 c=sqlite3.connect(path,timeout=5)
 try:
  c.execute('BEGIN IMMEDIATE')
  old=c.execute('SELECT number,t FROM slot WHERE receipt=?',(receipt,)).fetchone()
  if old:c.commit();return {'result':'same_receipt','number':old[0],'slot':old[1]}
  if not 36000<=now<=40200:c.rollback();return {'result':'closed'}
  row=c.execute('SELECT t FROM slot WHERE number=? AND receipt IS NULL AND t>=? ORDER BY t LIMIT 1',(number,now+300)).fetchone()
  if not row:c.rollback();return {'result':'no_target_slot'}
  n=c.execute('UPDATE slot SET receipt=? WHERE number=? AND t=? AND receipt IS NULL',(receipt,number,row[0])).rowcount
  assert n==1;c.commit();return {'result':'accepted','number':number,'slot':row[0]}
 finally:c.close()
def main():
 observations=[]
 with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
  scenarios=[('all17',[(17,36300)]*12,4),('balanced',[(n,36300) for n in [17,18,19] for _ in range(4)],12),('late17',[(17,40140)]*3,1),('exact_cutoff',[(18,40200)],1),('after_cutoff',[(18,40201)],0)]
  for name,inputs,count in scenarios:
   path=Path(tmp)/(name+'.sqlite');setup(path)
   results=[reserve(path,name+str(i),n,t) for i,(n,t) in enumerate(inputs)]
   accepted=sum(r['result']=='accepted' for r in results)
   c=sqlite3.connect(path);occupied=c.execute('SELECT number,t,receipt FROM slot WHERE receipt IS NOT NULL ORDER BY number,t').fetchall();c.close()
   assert accepted==count==len(occupied)
   observations.append({'case':name,'inputs':inputs,'results':results,'occupied':occupied,'accepted':accepted})
  path=Path(tmp)/'race.sqlite';setup(path,True)
  with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(lambda receipt:reserve(path,receipt,17,40140),['raceA','raceB']))
  assert sum(r['result']=='accepted' for r in results)==1
  winner=['raceA','raceB'][next(i for i,r in enumerate(results) if r['result']=='accepted')]
  replay=reserve(path,winner,17,40140);assert replay['result']=='same_receipt'
  observations.append({'case':'two_connections_final_slot','results':results,'replay':replay})
 result={'rule':'s1; confirm-completed time, >= 300 seconds preparation, cutoff inclusive 40200','observations':observations,'limits':['SQLite allocation only; receipt payload equality verified separately by HTTP experiment','reserved slot is not physical display completion or real visitor impact']}
 (ROOT/'allocation-observations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'accepted':{r['case']:r.get('accepted',r.get('results')) for r in observations},'limits':result['limits']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
