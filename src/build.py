# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0,'.')
import data_wh, data_cig as D, enrich as EN, data_cat as C
# Ligne : 0 réf, 1 désignation, 2 prix, 3 image, 4 note, 5 nom développé, 6 pays/origine, 7 Neptune, 8 specs,
# 9 liens de notation, 10 stock, 11 accessoire, 12 longueur CA, 13 page du catalogue festif (badge), 14 type (filtre),
# 15 prix de la liste précédente, 16 ligne de détail du catalogue
B="12BLUERIVIERA"
CIG=[]
for line in D.NEW.split('\n'):
    k,desc,price,pn,sh,tot = line.split('|')
    acc = k in EN.ACC
    CIG.append([B+k, desc, float(price), EN.IMG.get(k,""), EN.NOTE.get(k,""), EN.TERM[k],
                EN.COUNTRY[k], EN.NEP.get(k) and [EN.NEP[k][0],EN.NEP[k][1]] or None,
                EN.SPEC.get(k), EN.LINKS.get(k), [int(pn),int(sh),int(tot)], acc,
                EN.LEN.get(k) and list(EN.LEN[k]), None, None, None, None])
WH=[[r[0],r[1],r[2],r[3],r[4],r[5],r[6],None,None,r[7],None,False,None,None,None,None,None] for r in data_wh.WH]

# Catalogue festif 2026/2027
NONE_ORIG="Non indiquée au catalogue"
SEC={"vin":[],"bulles":[],"gin":[],"sansalcool":[],"rhum":[],"liqueur":[]}
WH_NEW=[]; WH_UPD=[]
def info(orig,vint,vol,typ):
    return " · ".join(x for x in [orig,vint,vol,typ] if x)
for line in C.CAT.split('\n'):
    p,i,sec,typ,name,orig,vint,vol,price = line.split('|')
    key=p+"|"+i; page=int(p); price=float(price)
    det=info(orig,vint,vol,typ)
    img="img/cat/p%02d-%02d.jpg"%(page,int(i))
    if sec=="whisky":
        refs=C.WH_MATCH.get(key)
        if refs:
            for r in WH:
                if r[0] in refs:
                    r[15]=r[2]; r[2]=price; r[13]=page; r[16]="Catalogue p. %d : %s"%(page,det)
                    WH_UPD.append(r[0])
            continue
        WH_NEW.append(["Cat. p. %d / %s"%(page,i), name, price, img, C.NOTE.get(key,""), name, orig or NONE_ORIG,
                       None,None,None,None,False,None,page,typ or None,None,det])
        continue
    if sec=="bulles":
        ftype="Champagne" if typ.startswith("Champagne") else "Prosecco" if key in C.PROSECCO else \
              "Apéritif" if typ=="Apéritif" else "Vin effervescent"
    else:
        ftype=typ
    SEC[sec].append(["Cat. p. %d / %s"%(page,i), name, price, img, C.NOTE.get(key,""), name, orig or NONE_ORIG,
                     None,None,None,None,False,None,page,ftype,None,det])
WH+=WH_NEW

def js(rows):
    return ',\n'.join(json.dumps(r,ensure_ascii=False) for r in rows)
removed=[(B+k,D.OLD_DESC[k]) for k in ["43","44","55","70","83","86","95","96","97","98","115","118"]]
added=[r for r in CIG if r[0][len(B):] in ["05","28","32","35","37","39","40","41","50","58","62","66","67","76","84","103","121"]]
NCAT=sum(len(v) for v in SEC.values())
html=open('template.html',encoding='utf-8').read()
html=html.replace("/*CIGARS*/", js(CIG)).replace("/*WHISKIES*/", js(WH))
for k,v in SEC.items(): html=html.replace("/*CAT_%s*/"%k, js(v))
html=html.replace("/*NCIG*/",str(len(CIG))).replace("/*NWH*/",str(len(WH))).replace("/*NCAT*/",str(NCAT))
html=html.replace("/*NTOT*/",str(len(CIG)+len(WH)+NCAT))
html=html.replace("/*REMOVED*/", ", ".join(f"{a} ({b})" for a,b in removed))
html=html.replace("/*ADDED*/", ", ".join(r[0] for r in added))
html=html.replace("/*WH_UPD*/", ", ".join(WH_UPD)).replace("/*NWH_UPD*/", str(len(WH_UPD)))
html=html.replace("/*WH_NEW*/", ", ".join(r[1]+" ("+r[16]+")" for r in WH_NEW))
open('../index.html','w',encoding='utf-8',newline='\n').write(html)
print("cigares",len(CIG),"whiskies",len(WH),"(maj",len(WH_UPD),"+",len(WH_NEW),")",{k:len(v) for k,v in SEC.items()})
