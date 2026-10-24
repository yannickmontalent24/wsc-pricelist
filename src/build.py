# -*- coding: utf-8 -*-
# Génère le site : une page par catégorie (index.html = cigares), même gabarit, barre de navigation commune.
import json, re, sys
sys.path.insert(0,'.')
import data_wh, data_cig as D, enrich as EN, data_cat as C
try:
    import vivino as V
except ImportError:
    V = None
# Ligne : 0 réf, 1 désignation, 2 prix, 3 image, 4 note, 5 nom développé, 6 pays/origine, 7 Neptune, 8 specs,
# 9 liens de notation, 10 stock, 11 accessoire, 12 longueur CA, 13 page du catalogue festif (badge), 14 type (filtre),
# 15 prix de la liste précédente, 16 ligne de détail du catalogue, 17 libellé du message de commande, 18 unité
B="12BLUERIVIERA"
CIG=[]
for line in D.NEW.split('\n'):
    k,desc,price,pn,sh,tot = line.split('|')
    acc = k in EN.ACC
    CIG.append([B+k, desc, float(price), EN.IMG.get(k,""), EN.NOTE.get(k,""), EN.TERM[k],
                EN.COUNTRY[k], EN.NEP.get(k) and [EN.NEP[k][0],EN.NEP[k][1]] or None,
                EN.SPEC.get(k), EN.LINKS.get(k), [int(pn),int(sh),int(tot)], acc,
                EN.LEN.get(k) and list(EN.LEN[k]), None, None, None, None,
                re.sub(r'\s*/\d+/\s*$','',desc).strip(), "Accessoire" if acc else "Cigare"])
WH=[[r[0],r[1],r[2],r[3],r[4],r[5],r[6],None,None,r[7],None,False,None,None,None,None,None,r[1],"bouteille"] for r in data_wh.WH]

# Catalogue festif 2026/2027
NONE_ORIG="Non indiquée au catalogue"
STD_VOL={"75 cl","70 cl"}
SEC={"vin":[],"bulles":[],"gin":[],"sansalcool":[],"rhum":[],"liqueur":[]}
WH_NEW=[]; WH_UPD=[]
def info(*xs):
    return " · ".join(x for x in xs if x)
def label(name,vint,vol):
    return " ".join(x for x in [name, vint, "" if vol in STD_VOL else vol] if x)
for line in C.CAT.split('\n'):
    p,i,sec,typ,name,orig,vint,vol,price = line.split('|')
    key=p+"|"+i; page=int(p); price=float(price)
    det=info(orig,vint,vol,typ)
    img="img/cat/p%02d-%02d.jpg"%(page,int(i))
    vi=V and V.VIVINO.get(key)
    links=[["VI",vi[0],vi[1]]] if vi else None
    if sec=="whisky":
        refs=C.WH_MATCH.get(key)
        if refs:
            for r in WH:
                if r[0] in refs:
                    r[15]=r[2]; r[2]=price; r[13]=page; r[16]="Catalogue p. %d : %s"%(page,det)
                    WH_UPD.append(r[0])
            continue
        WH_NEW.append(["Cat. p. %d / %s"%(page,i), name, price, img, C.NOTE.get(key,""), name, orig or NONE_ORIG,
                       None,None,None,None,False,None,page,typ or None,None,det,label(name,vint,vol),"bouteille"])
        continue
    if sec=="bulles":
        ftype="Champagne" if typ.startswith("Champagne") else "Prosecco" if key in C.PROSECCO else \
              "Apéritif" if typ=="Apéritif" else "Vin effervescent"
    else:
        ftype=typ
    SEC[sec].append(["Cat. p. %d / %s"%(page,i), name, price, img, C.NOTE.get(key,""), name, orig or NONE_ORIG,
                     None,None,links,None,False,None,page,ftype,None,det,label(name,vint,vol),"bouteille"])
WH+=WH_NEW

CAT_SUB="%d références &middot; catalogue « Le Bottle Shop — Sélection festive 2026 / 2027 » &middot; prix en Rs TTC valables du 27 octobre 2026 au 10 janvier 2027, dans la limite des stocks disponibles"
def links(*groups):
    out=[]
    for g,items in groups:
        out.append('<span class="grp">%s</span>'%g)
        out+=['<a href="%s" target="_blank" rel="noopener">%s</a>'%(u,n) for n,u in items]
    return '<div class="links">'+"\n    ".join(out)+'</div>'
L_CIG=links(("Notation cigares :",[("Cigar Aficionado","https://www.cigaraficionado.com/"),("halfwheel","https://halfwheel.com/")]))
L_WH=links(("Notation whiskies :",[("Whiskybase","https://www.whiskybase.com/"),("Whisky Advocate","https://www.whiskyadvocate.com/"),("Distiller","https://distiller.com/")]))
L_WINE=links(("Notation vins :",[("Vivino","https://www.vivino.com/en/"),("Wine Spectator","https://www.winespectator.com/"),("Wine Enthusiast","https://www.wineenthusiast.com/ratings/")]))
PAGES=[
 ("index.html","Cigares","%d références &middot; liste « CIGARS OCTOBER 2026 » &middot; stock au 13.10.2026, sous réserve de disponibilité"%len(CIG),L_CIG,
  [dict(id="cig",title="Cigares",ph="Rechercher un cigare (référence ou désignation)…",data=CIG,missing=True,stock=True)]),
 ("whiskies.html","Whiskies","%d références &middot; badge FÊTES 2026/2027 : prix du catalogue festif (Rs TTC, du 27 octobre 2026 au 10 janvier 2027)"%len(WH),L_WH,
  [dict(id="wh",title="Whiskies",ph="Rechercher un whisky (référence ou désignation)…",data=WH,missing=True)]),
 ("vins.html","Vins",CAT_SUB%len(SEC["vin"]),L_WINE,
  [dict(id="vin",title="Vins",ph="Rechercher un vin…",data=SEC["vin"],cat=True,reviews=True,types=["Blanc","Rosé","Rouge"],typeAll="Toutes les couleurs")]),
 ("bulles.html","Champagnes et autres bulles",CAT_SUB%len(SEC["bulles"]),L_WINE,
  [dict(id="bulles",title="Champagnes et autres bulles",ph="Rechercher un champagne, un prosecco…",data=SEC["bulles"],cat=True,reviews=True,
        types=["Prosecco","Vin effervescent","Champagne","Apéritif"],typeAll="Tous les types")]),
 ("gins.html","Gins",CAT_SUB%len(SEC["gin"]),"",[dict(id="gin",title="Gins",ph="Rechercher un gin…",data=SEC["gin"],cat=True)]),
 ("sans-alcool.html","Sans alcool",CAT_SUB%len(SEC["sansalcool"]),"",[dict(id="sa",title="Sans alcool",ph="Rechercher une boisson sans alcool…",data=SEC["sansalcool"],cat=True)]),
 ("rhums.html","Rhums",CAT_SUB%len(SEC["rhum"]),"",[dict(id="rhum",title="Rhums",ph="Rechercher un rhum…",data=SEC["rhum"],cat=True)]),
 ("liqueurs.html","Liqueurs",CAT_SUB%len(SEC["liqueur"]),"",[dict(id="liq",title="Liqueurs",ph="Rechercher une liqueur…",data=SEC["liqueur"],cat=True)]),
]
NAVNAME={"Champagnes et autres bulles":"Bulles"}
tpl=open('template.html',encoding='utf-8').read()
for fn,title,sub,lk,secs in PAGES:
    nav="".join('<a href="%s"%s>%s</a>'%(f,' class="on" aria-current="page"' if f==fn else '',NAVNAME.get(t,t)) for f,t,*_ in PAGES)
    data=json.dumps(secs,ensure_ascii=False).replace('</','<\\/')
    html=tpl.replace("/*PAGE_TITLE*/",title).replace("/*PAGE_SUB*/",sub).replace("/*PAGE_LINKS*/",lk).replace("/*NAV*/",nav).replace("/*SECTIONS*/",data)
    open('../'+fn,'w',encoding='utf-8',newline='\n').write(html)
nvi=sum(1 for s in ("vin","bulles") for r in SEC[s] if r[9])
print("pages",len(PAGES),"| cigares",len(CIG),"whiskies",len(WH),"(maj",len(WH_UPD),"+",len(WH_NEW),")",
      {k:len(v) for k,v in SEC.items()},"| liens Vivino",nvi,"/",len(SEC["vin"])+len(SEC["bulles"]))
