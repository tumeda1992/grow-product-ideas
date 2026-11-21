import os,sys,json,tempfile,subprocess,fcntl,platform
from pathlib import Path
OLD={"rev":0,"node":"root"};NEW={"rev":1,"node":"a3"}
if len(sys.argv)>1:
    mode,loc=sys.argv[1:];p=Path(loc)
    if mode=="lock":
        with (p/"record.lock").open("a+") as f:
            try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError: sys.exit(23)
        sys.exit(0)
    if mode=="direct":
        with (p/"record.json").open("w") as f:
            f.write('{"rev":');f.flush();os.fsync(f.fileno());os._exit(7)
    with (p/"record.lock").open("a+") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        with (p/"next.tmp").open("w") as f:
            json.dump(NEW,f);f.flush();os.fsync(f.fileno())
        if mode=="before":os._exit(7)
        os.replace(p/"next.tmp",p/"record.json")
        if mode=="after":os._exit(7)
    sys.exit(0)
rows=[]
with tempfile.TemporaryDirectory(prefix="c1-boundary-") as loc:
    p=Path(loc)
    for mode in ["normal","before","after","direct"]:
        (p/"record.json").write_text(json.dumps(OLD))
        r=subprocess.run([sys.executable,__file__,mode,loc],check=False)
        try: observed=json.loads((p/"record.json").read_text())
        except json.JSONDecodeError:observed="invalid-json"
        expected={"normal":NEW,"before":OLD,"after":NEW,"direct":"invalid-json"}[mode]
        rows.append({"case":mode,"returncode":r.returncode,"observed":observed,"expected":expected,"pass":observed==expected})
    with (p/"record.lock").open("a+") as f:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        r=subprocess.run([sys.executable,__file__,"lock",loc],check=False)
        rows.append({"case":"concurrent-rejected","observed":r.returncode,"expected":23,"pass":r.returncode==23})
    r=subprocess.run([sys.executable,__file__,"lock",loc],check=False)
    rows.append({"case":"released-accepted","observed":r.returncode,"expected":0,"pass":r.returncode==0})
print(json.dumps({"runtime":sys.version,"platform":platform.platform(),"observations":rows},ensure_ascii=False,indent=2))
assert all(x["pass"] for x in rows)
