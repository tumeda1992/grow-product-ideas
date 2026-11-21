import json,sqlite3,tempfile
from pathlib import Path
schema=(Path(__file__).resolve().parent.parent/'data-model/schema.sql').read_text()
with tempfile.TemporaryDirectory() as d:
 c=sqlite3.connect(str(Path(d)/'read.db'),isolation_level=None);c.executescript(schema)
 c.execute('BEGIN');c.execute('INSERT INTO item VALUES("S1",1,0)')
 c.execute('INSERT INTO source VALUES("S1",1,"consent","2026-11-20T08:00:00+09:00","B1","blue bag","father","read original")')
 c.execute('INSERT INTO response_decision VALUES("S1",1,"participate","father","2026-11-16T19:30:00+09:00","family wishes and original checked")')
 c.execute('INSERT INTO action_need VALUES("S1",1,"prepare",15,"remaining preparation checked")');c.execute('COMMIT')
 query='SELECT d.choice,n.minutes FROM item i LEFT JOIN response_decision d ON d.item_id=i.id AND d.source_rev=i.current_rev LEFT JOIN action_need n ON n.item_id=i.id AND n.source_rev=i.current_rev WHERE i.id="S1"'
 first=c.execute(query).fetchall();assert first==[('participate',15)]
 c.execute('BEGIN');c.execute('INSERT INTO source SELECT item_id,2,title,"2026-11-19T08:00:00+09:00",body_key,location,"mother","changed deadline checked" FROM source WHERE item_id="S1" AND rev=1');c.execute('UPDATE item SET current_rev=2 WHERE id="S1"');c.execute('COMMIT')
 changed=c.execute(query).fetchall();assert changed==[(None,None)]
 c.execute('BEGIN');c.execute('INSERT INTO response_decision VALUES("S1",2,"needs_check","mother","2026-11-18T19:30:00+09:00","availability must be checked")');c.execute('INSERT INTO action_need VALUES("S1",2,"prepare",NULL,"remaining duration unknown")');c.execute('COMMIT')
 unknown=c.execute(query).fetchall();assert unknown==[('needs_check',None)]
 past=c.execute('SELECT choice,minutes FROM response_decision d JOIN action_need n USING(item_id,source_rev) WHERE source_rev=1').fetchall();assert past==[('participate',15)]
 print(json.dumps({'R1_before_booking':first,'R2_without_reconfirmation':changed,'R2_unknown_duration':unknown,'retained_R1':past,'observed':'all expected; source-specific selection and unknown duration preserved'},ensure_ascii=False,indent=2));c.close()
