import sys, pickle, os, zipfile, xml.etree.ElementTree as ET
exec(open(sys.argv[1]).read())            # lo.py
orig,_=load(sys.argv[2],"fb-orig"); new,_=load(sys.argv[3],"fb-new")
A=list(orig.values())[0]; B=list(new.values())[0]
ST="urn:oasis:names:tc:opendocument:xmlns:style:1.0"; FO="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
def styles(tag):
    root=ET.parse("fods/%s/%s"%(tag, os.listdir("fods/"+tag)[0])).getroot(); out={}
    data={e.get("{%s}name"%ST): e.tag.split("}")[1] for e in root.iter() if e.tag.startswith("{urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0}") and e.get("{%s}name"%ST)}
    for s in root.iter("{%s}style"%ST):
        bold=any(t.get("{%s}font-weight"%FO)=="bold" for t in s.iter("{%s}text-properties"%ST))
        out[s.get("{%s}name"%ST)]=(bold, data.get(s.get("{%s}data-style-name"%ST),""))
    return out
sa,sb=styles("fb-orig"),styles("fb-new")
expected=pickle.load(open("expected.pkl","rb")); bad=[]; n=0
def look(cells,st,ref):
    g=cells.get(ref); return st.get(g[3],(False,"")) if g else (False,"")
for (r,c,is_style),v in expected.items():
    ref=chr(64+c)+str(r); g=B.get(ref); n+=1
    if is_style:
        bold_want,fmt=v.split(":"); bold,_=look(B,sb,ref); text=g[4] if g else ""
        if bold_want!="x" and bold!=(bold_want=="1"): bad.append((ref,"bold",bold_want,bold))
        if fmt=="eur" and not text.endswith("€"): bad.append((ref,"euro shows",text))
        if fmt=="num" and not (len(text.split(".")[-1])==2 or len(text.split(",")[-1])==2): bad.append((ref,"number shows",text))
        if fmt=="date" and not (g and g[0]=="date"): bad.append((ref,"date",g))
    else:
        kind,body=v.split(":",1)
        if kind=="c": ok = g is None or g[4]==""
        elif kind=="n": ok = g is not None and (g[0]=="date" or abs(float(g[1])-float(body))<1e-6)
        elif kind=="f": ok = g is not None and g[2].replace("[.","").replace("]","").replace("of:=","")==body
        else: ok = g is not None and g[4]==body
        if not ok: bad.append((ref,v,g))
print("  changed cells and formats, as LibreOffice reads the saved file: %d checked, %d wrong"%(n,len(bad)))
for x in bad[:8]: print("    ",x)
changed={chr(64+c)+str(r) for (r,c,_) in expected}
diff=[]; m=0
for ref,g in A.items():
    if ref in changed: continue
    row=int(ref.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    if row>400: continue
    m+=1; h=B.get(ref)
    if h is None or (g[0],g[1],g[4])!=(h[0],h[1],h[4]) or look(A,sa,ref)!=look(B,sb,ref): diff.append((ref,g,h))
print("  untouched cells in the first 400 rows: %d compared (value, shown text, bold, format kind), %d differ"%(m,len(diff)), diff[:3])
for ref in ("G2","G4","G6","G7","G8","A17","C21"):
    g=B.get(ref); print("    %-4s shows %-22r bold=%-5s %s"%(ref, g[4] if g else None, look(B,sb,ref)[0], g[2] if g else ""))
