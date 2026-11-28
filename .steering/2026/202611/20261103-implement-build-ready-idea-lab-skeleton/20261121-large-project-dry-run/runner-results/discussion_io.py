from pathlib import Path
import json, subprocess, hashlib, difflib, datetime
W=Path('/workspace/grow-product-ideas/.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton')
PLAN=W/'product-plans/20261121-reframe-local-collections'
RUN=W/'20261121-large-project-dry-run/runner-results'
HELPER='/workspace/.cache/grow-product-ideas/plugin-sources-9.1.1/tumeda-dev/plugins/tumeda-dev/skills/facilitate-discussion/scripts/inspect-discussion.mjs'
def call(action,directory,extra=(),data=None):
 r=subprocess.run(['node',HELPER,action,'--directory',str(directory),'--name','discussion.md',*extra],input=data,capture_output=True,text=True)
 result=json.loads(r.stdout)
 with (RUN/'discussion-tools.jsonl').open('a') as f: f.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'action':action,'code':r.returncode,'result':result},ensure_ascii=False)+'\n')
 if r.returncode: raise RuntimeError(result)
 return result

def read(layer,topic):
 d=PLAN/layer; baseline=call('snapshot',d)
 call('check',d)
 for extra in [('--view','current'),('--topic',str(topic))]:
  offset=0
  while True:
   r=call('read',d,(*extra,'--offset',str(offset),'--limit','100'))
   if extra[0]=='--topic':
    for c in r['chunks']: print(c['text'],end='')
   if r['next_offset'] is None: break
   offset=r['next_offset']
 call('compare',d,data=json.dumps(baseline))
 (RUN/(layer.replace('/','__')+'-baseline.json')).write_text(json.dumps(baseline))

def save(layer,new):
 d=PLAN/layer;p=d/'discussion.md'; old=p.read_text()
 call('compare',d,data=(RUN/(layer.replace('/','__')+'-baseline.json')).read_text())
 p.write_text(new)
 print(''.join(difflib.unified_diff(old.splitlines(True),p.read_text().splitlines(True),fromfile='before',tofile='after')))
 s=call('snapshot',d)
 (RUN/(layer.replace('/','__')+'-baseline.json')).write_text(json.dumps(s))
 call('check',d)
 print('saved sha256',hashlib.sha256(p.read_bytes()).hexdigest())
