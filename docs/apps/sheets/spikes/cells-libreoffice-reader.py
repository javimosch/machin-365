# LibreOffice as the independent reader: open an xlsx, return {sheet: {ref: (type, value, formula, style, text)}}, merges
import subprocess, os, shutil, xml.etree.ElementTree as ET
NS={"table":"urn:oasis:names:tc:opendocument:xmlns:table:1.0","office":"urn:oasis:names:tc:opendocument:xmlns:office:1.0","text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
def q(p,n): return "{%s}%s"%(NS[p],n)
def col(n):
    s=""
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def alltext(e):
    out=e.text or ""
    for c in e:
        if c.tag==q("text","s"): out+=" "*int(c.get(q("text","c"),"1"))
        elif c.tag==q("text","tab"): out+="\t"
        elif c.tag==q("text","line-break"): out+="\n"
        else: out+=alltext(c)
        out+=c.tail or ""
    return out
def load(path, tag):
    d="fods/"+tag; shutil.rmtree(d,ignore_errors=True)
    subprocess.run(["soffice","--headless","-env:UserInstallation=file://"+os.environ["PROFILE"],"--convert-to","fods","--outdir",d,path],capture_output=True,timeout=200)
    root=ET.parse(d+"/"+os.path.basename(path).rsplit(".",1)[0]+".fods").getroot()
    sheets={}; merges=[]
    for t in root.iter(q("table","table")):
        name=t.get(q("table","name")); cells={}; r=0
        for row in t.iter(q("table","table-row")):
            for _ in range(min(int(row.get(q("table","number-rows-repeated"),"1")),1000)):
                r+=1; c=0
                for cell in row:
                    n=int(cell.get(q("table","number-columns-repeated"),"1"))
                    for _ in range(min(n,100)):
                        c+=1
                        typ=cell.get(q("office","value-type")); f=cell.get(q("table","formula"),"")
                        if cell.get(q("table","number-columns-spanned")): merges.append((name,col(c)+str(r),cell.get(q("table","number-columns-spanned"))))
                        if typ is None and not f: continue
                        val=cell.get(q("office","value")) or cell.get(q("office","date-value")) or cell.get(q("office","boolean-value"))
                        text="\n".join(alltext(p) for p in cell.findall(q("text","p")))
                        cells[col(c)+str(r)]=(typ,val if val is not None else text,f,cell.get(q("table","style-name")),text)
        sheets[name]=cells
    return sheets, merges
