# Drives the trial with real X input and keeps its own model of what the file should hold.
import ctypes as C, time, os, sys, subprocess, threading, random, zipfile, re, xml.etree.ElementTree as ET
X=C.CDLL('libX11.so.6'); T=C.CDLL('libXtst.so.6'); P=C.c_void_p; L=C.c_ulong
X.XOpenDisplay.restype=P; X.XOpenDisplay.argtypes=[C.c_char_p]; X.XFlush.argtypes=[P]
X.XStringToKeysym.restype=L; X.XStringToKeysym.argtypes=[C.c_char_p]; X.XKeysymToKeycode.restype=C.c_ubyte; X.XKeysymToKeycode.argtypes=[P,L]
for f,a in (("XTestFakeKeyEvent",[P,C.c_uint,C.c_int,L]),("XTestFakeButtonEvent",[P,C.c_uint,C.c_int,L]),("XTestFakeMotionEvent",[P,C.c_int,C.c_int,C.c_int,L])): getattr(T,f).argtypes=a
SRC, OUT, DUMP, DELAY = sys.argv[1], sys.argv[2], sys.argv[3], 0.05
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
def read_xlsx(path):
    """independent reader: zipfile + ElementTree. {(row,col): (kind, text)}"""
    z=zipfile.ZipFile(path); assert z.testzip() is None
    sst=[]
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS+"si"): sst.append("".join(t.text or "" for t in si.iter(NS+"t")))
    names=[n for n in z.namelist() if re.match(r"xl/worksheets/sheet1\.xml$",n)]
    out={}
    for c in ET.fromstring(z.read(names[0])).iter(NS+"c"):
        m=re.match(r"([A-Z]+)(\d+)",c.get("r")); col=0
        for ch in m.group(1): col=col*26+ord(ch)-64
        key=(int(m.group(2)),col); t=c.get("t"); f=c.find(NS+"f"); v=c.find(NS+"v")
        if f is not None: out[key]=("formula",f.text or "")
        elif t=="s": out[key]=("text",sst[int(v.text)])
        elif t=="inlineStr": out[key]=("text","".join(x.text or "" for x in c.iter(NS+"t")))
        elif v is not None: out[key]=("number",v.text)
    return out
base=read_xlsx(SRC)
over={}; undo=[]; redo=[]; cur=[2,1]; anchor=[2,1]; fails=[]; ops={}
def isnum(s): return bool(re.fullmatch(r"-?(\d+(\.\d*)?|\.\d+)",s)) and len(s)<=15 and not (len(s)>1 and s[0]=="0" and s[1]!=".")
def enc(s): return None if False else (("clear","") if s=="" else ("formula",s[1:]) if s.startswith("=") else ("number",s) if isnum(s) else ("text",s))
def text_of(k):
    v=over.get(k) or base.get(k)
    if v is None or v[0]=="clear": return ""
    return ("="+v[1]) if v[0]=="formula" else v[1]
def step(changes):
    if not changes: return
    st=[(k,over.get(k),n) for k,n in changes]
    for k,_,n in st: over[k]=n
    undo.append(st); redo.clear()
def do_undo():
    if undo:
        st=undo.pop()
        for k,b,_ in reversed(st):
            if b is None: over.pop(k,None)
            else: over[k]=b
        redo.append(st)
def do_redo():
    if redo:
        st=redo.pop()
        for k,_,n in st: over[k]=n
        undo.append(st)
d=X.XOpenDisplay(os.environ["DISPLAY"].encode())
def flush(t=DELAY): X.XFlush(d); time.sleep(t)
def kc(n): return X.XKeysymToKeycode(d,X.XStringToKeysym(n.encode()))
def key(*names, wait=DELAY):
    for n in names: T.XTestFakeKeyEvent(d,kc(n),1,0); flush(0.015)
    for n in reversed(names): T.XTestFakeKeyEvent(d,kc(n),0,0); flush(0.015)
    flush(wait)
def shift(n,times):
    T.XTestFakeKeyEvent(d,kc("Shift_L"),1,0); flush()
    for _ in range(times): key(n)
    T.XTestFakeKeyEvent(d,kc("Shift_L"),0,0); flush()
def nav(n,times=1):
    for _ in range(times):
        key(n)
        dr,dc={"Down":(1,0),"Up":(-1,0),"Right":(0,1),"Left":(0,-1),"Next":(25,0),"Prior":(-25,0)}[n]
        cur[0]=max(1,min(20001,cur[0]+dr)); cur[1]=max(1,min(26,cur[1]+dc)); anchor[:]=cur
def extend(n,times):
    shift(n,times)
    for _ in range(times):
        dr,dc={"Down":(1,0),"Right":(0,1),"Next":(25,0)}[n]; cur[0]=min(20001,cur[0]+dr); cur[1]=min(26,cur[1]+dc)
def block(): return range(min(cur[0],anchor[0]),max(cur[0],anchor[0])+1), range(min(cur[1],anchor[1]),max(cur[1],anchor[1])+1)
def read_dump():
    for _ in range(20):
        L_=open(DUMP).read().split("\n")
        if len(L_)>1 and L_[-2].startswith("changes "): return L_
        time.sleep(0.05)
    return L_
def col(c): return chr(64+c)
def check(label, settle=0.25):
    time.sleep(settle)
    L_=read_dump(); head=L_[0].split()
    want_cursor=col(cur[1])+str(cur[0]); n=int(L_[-2].split()[1]); problems=[]
    if head[1]!=want_cursor: problems.append("cursor app=%s script=%s"%(head[1],want_cursor))
    if head[5]!="%d/%d"%(len(undo),len(undo)+len(redo)): problems.append("undo app=%s script=%d/%d"%(head[5],len(undo),len(undo)+len(redo)))
    if n!=len(over): problems.append("changed cells app=%d script=%d"%(n,len(over)))
    if len(over)<=60:
        app={l.split("=",1)[0]:l.split("=",1)[1] for l in L_[1:-2]}
        tag={"number":"n:","text":"t:","formula":"f:","clear":"c:"}
        mine={col(c)+str(r):tag[v[0]]+v[1] for (r,c),v in over.items()}
        if app!=mine: problems.append("values differ: only-app %s only-script %s"%(sorted(set(app.items())-set(mine.items()))[:4], sorted(set(mine.items())-set(app.items()))[:4]))
    if problems: fails.append(label+": "+"; ".join(problems))
    return not problems
def type_value(s):
    for ch in s:
        name={"-":"minus",".":"period"," ":"space","=":"equal"}.get(ch,ch)
        if ch.isupper(): T.XTestFakeKeyEvent(d,kc("Shift_L"),1,0); flush(0.02); key(ch.lower(),wait=0.02); T.XTestFakeKeyEvent(d,kc("Shift_L"),0,0); flush(0.02)
        else: key(name,wait=0.02)
    time.sleep(0.2)
def enter_value(s):
    k=(cur[0],cur[1]); type_value(s); key("Return",wait=0.25); step([(k,enc(s))]); cur[0]=min(20001,cur[0]+1); anchor[:]=cur
def copy_paste(rows_pages, cols, down_pages):
    extend("Right",cols-1)
    if rows_pages: extend("Next",rows_pages)
    rs,cs=block(); data=[[text_of((r,c)) for c in cs] for r in rs]
    key("Control_L","c",wait=0.4)
    nav("Next",down_pages)      # moving without shift collapses the selection onto the cursor
    r0,c0=cur
    key("Control_L","v",wait=1.0)
    step([((r0+i,c0+j),enc(v)) for i,row in enumerate(data) for j,v in enumerate(row) if r0+i<=20001 and c0+j<=26])
    return len(data)*len(data[0])
def delete_block(): 
    rs,cs=block(); key("Delete",wait=0.4); step([((r,c),("clear","")) for r in rs for c in cs])
def save(wait=1.6): key("Control_L","s",wait=wait)
def verify_saved(label):
    got=read_xlsx(OUT); bad=[]
    keys=set(over)|set(random.sample(list(base),3000))
    for k in keys:
        v=over.get(k); g=got.get(k)
        if v is None:
            b=base.get(k)
            ok = g==b or (b is not None and g is not None and b[0]=="formula" and g[0]=="formula")
        elif v[0]=="clear": ok = g is None
        elif v[0]=="number": ok = g is not None and g[0]=="number" and float(g[1])==float(v[1])
        else: ok = g==v
        if not ok: bad.append((col(k[1])+str(k[0]), v, g))
    if bad: fails.append("%s: saved file wrong in %d of %d cells, e.g. %s"%(label,len(bad),len(keys),bad[:3]))
    return len(keys), len(bad)
