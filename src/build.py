# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0,'.')
import data_wh, data_cig as D, enrich as EN
B="12BLUERIVIERA"
CIG=[]
for line in D.NEW.split('\n'):
    k,desc,price,pn,sh,tot = line.split('|')
    acc = k in EN.ACC
    CIG.append([B+k, desc, float(price), EN.IMG.get(k,""), EN.NOTE.get(k,""), EN.TERM[k],
                EN.COUNTRY[k], EN.NEP.get(k) and [EN.NEP[k][0],EN.NEP[k][1]] or None,
                EN.SPEC.get(k), EN.LINKS.get(k), [int(pn),int(sh),int(tot)], acc])
WH=[[r[0],r[1],r[2],r[3],r[4],r[5],r[6],None,None,r[7],None,False] for r in data_wh.WH]
def js(rows):
    return ',\n'.join(json.dumps(r,ensure_ascii=False) for r in rows)
removed=[(B+k,D.OLD_DESC[k]) for k in ["43","44","55","70","83","86","95","96","97","98","115","118"]]
added=[r for r in CIG if r[0][len(B):] in ["05","28","32","35","37","39","40","41","50","58","62","66","67","76","84","103","121"]]
html=open('template.html',encoding='utf-8').read()
html=html.replace("/*CIGARS*/", js(CIG)).replace("/*WHISKIES*/", js(WH))
html=html.replace("/*NCIG*/",str(len(CIG))).replace("/*NWH*/",str(len(WH))).replace("/*NTOT*/",str(len(CIG)+len(WH)))
html=html.replace("/*REMOVED*/", ", ".join(f"{a} ({b})" for a,b in removed))
html=html.replace("/*ADDED*/", ", ".join(r[0] for r in added))
open('/home/claude/pricelist.html','w',encoding='utf-8').write(html)
print("cigares",len(CIG),"whiskies",len(WH))
