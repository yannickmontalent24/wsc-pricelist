# -*- coding: utf-8 -*-
# Outil ponctuel : découpe les bouteilles du catalogue PDF (cadres BOX de data_cat.py) vers ../img/cat/.
# Usage : python crop_catalogue.py "CATALOGUE LE BOTTLE SHOP 2026.pdf"   (nécessite PyMuPDF : pip install pymupdf)
# Les images produites sont versionnées ; le PDF ne l'est pas. build.py n'a pas besoin de ce script.
import sys, os
sys.path.insert(0, '.')
import pymupdf
import data_cat as C
DPI, BASE, PAD = 160, 110, 0.04
pdf = pymupdf.open(sys.argv[1])
os.makedirs('../img/cat', exist_ok=True)
pages = {}
for key, (x0, y0, x1, y1) in C.BOX.items():
    p, i = map(int, key.split('|'))
    if p not in pages:
        pages[p] = pdf[p - 1].get_pixmap(dpi=DPI)
    pix = pages[p]
    s = DPI / BASE
    w, h = (x1 - x0) * s, (y1 - y0) * s
    r = pymupdf.IRect(max(0, int(x0 * s - w * PAD)), max(0, int(y0 * s - h * PAD)),
                      min(pix.width, int(x1 * s + w * PAD)), min(pix.height, int(y1 * s + h * PAD)))
    out = pymupdf.Pixmap(pix, 0) if pix.alpha else pix
    crop = pymupdf.Pixmap(out.colorspace, r, False)
    crop.copy(out, r)
    crop.save('../img/cat/p%02d-%02d.jpg' % (p, i), jpg_quality=82)
print(len(C.BOX), 'images')
