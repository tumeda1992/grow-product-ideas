import csv,sys
from pathlib import Path
rows=list(csv.DictReader((Path(__file__).parent/'items.csv').open()))
item=next(x for x in rows if x['case_id']==sys.argv[1])
print(f"{item['case_id']} / {item['item_label']} / {item['shelf']} / {item['status']}")
