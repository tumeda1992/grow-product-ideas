"""保存とlockだけのprobe。ゲーム本体は含めない。"""
from pathlib import Path
import json,os,sys,subprocess,tempfile,fcntl,platform

def save_child(target,stop):
 p=Path(target);t=p.with_suffix('.pending')
 with t.open('w',encoding='utf-8') as f:
  json.dump({'version':1,'reason':'比較のために別の文を置く'},f,ensure_ascii=False);f.flush();os.fsync(f.fileno())
 if stop=='before':os._exit(17)
 os.replace(t,p)
 os._exit(18)

def lock_child(path):
 with open(path,'a') as f:
  try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:print('blocked');return
  print('acquired')

if len(sys.argv)>1:
 if sys.argv[1]=='save':save_child(*sys.argv[2:])
 elif sys.argv[1]=='lock':lock_child(sys.argv[2])
else:
 here=Path(__file__).resolve().parent
 results={'environment':{'python':platform.python_version(),'system':platform.system()},'observations':[]}
 with tempfile.TemporaryDirectory(dir=here,prefix='probe-') as td:
  p=Path(td)/'data.json';s='検査用の理由：Aではなく別の文'
  p.write_text(json.dumps({'reason':s},ensure_ascii=False),encoding='utf-8');got=json.loads(p.read_text(encoding='utf-8'))
  assert got=={'reason':s};results['observations'].append({'id':'T1','unicode_equal':True})
  for phase,expect in [('before',0),('after',1)]:
   p.write_text(json.dumps({'version':0}),encoding='utf-8')
   r=subprocess.run([sys.executable,__file__,'save',str(p),phase],capture_output=True,text=True)
   got=json.loads(p.read_text(encoding='utf-8'));assert got['version']==expect
   results['observations'].append({'id':'T2' if phase=='before' else 'T3','stop':phase,'exit_code':r.returncode,'read_version':got['version'],'stdout':r.stdout})
  lp=Path(td)/'writer.lock'
  with lp.open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   r=subprocess.run([sys.executable,__file__,'lock',str(lp)],capture_output=True,text=True,check=True)
   assert r.stdout.strip()=='blocked';results['observations'].append({'id':'T4-live','result':r.stdout.strip()})
  r=subprocess.run([sys.executable,__file__,'lock',str(lp)],capture_output=True,text=True,check=True)
  assert r.stdout.strip()=='acquired';results['observations'].append({'id':'T4-released','result':r.stdout.strip()})
 (here/'observations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(results,ensure_ascii=False,indent=2))
