exec(open("harness.py").read())
PID=sys.argv[4]; random.seed(11); samples=[]; stop=False
def mem():
    s=open("/proc/%s/status"%PID).read()
    return int(re.search(r"VmRSS:\s+(\d+)",s).group(1))//1024, int(re.search(r"VmHWM:\s+(\d+)",s).group(1))//1024
def sampler():
    while not stop:
        try: samples.append((time.time(),)+mem())
        except Exception: return
        time.sleep(0.2)
threading.Thread(target=sampler,daemon=True).start()
time.sleep(1.0); opened=mem()
t0=time.time(); last_save=t0; saves=0; minute=1; marks=[]
def count(n): ops[n]=ops.get(n,0)+1
while time.time()-t0 < float(os.environ.get("SECONDS_",300)):
    r=random.random()
    if time.time()-last_save>25:
        save(2.0); last_save=time.time(); saves+=1; count("save"); check("after save %d"%saves)
    elif r<0.34: enter_value(random.choice([str(random.randint(1,99999)),"abc %d"%random.randint(1,999),"%d.%d"%(random.randint(1,999),random.randint(1,99))])); count("type"); check("type")
    elif r<0.44:
        if cur[1]>1: nav("Left",cur[1]-1)
        n=copy_paste(4,20,random.randint(1,3)); count("paste of %d cells"%n); check("paste",1.5)
    elif r<0.50: extend("Right",random.randint(1,3)); extend("Down",random.randint(1,5)); delete_block(); count("delete block"); check("delete",0.6)
    elif r<0.64: do_undo(); key("Control_L","z",wait=0.8); count("undo"); check("undo",0.5)
    elif r<0.70: do_redo(); key("Control_L","y",wait=0.8); count("redo"); check("redo",0.5)
    elif r<0.86: nav(random.choice(["Next","Next","Next","Prior"]),random.randint(2,12)); count("page"); check("page")
    elif r<0.93:
        T.XTestFakeMotionEvent(d,-1,600,400,0); flush()
        b=random.choice([4,5,5])
        for _ in range(random.randint(10,40)): T.XTestFakeButtonEvent(d,b,1,0); T.XTestFakeButtonEvent(d,b,0,0); flush(0.02)
        count("wheel scroll")
    else: nav(random.choice(["Right","Down","Left"]),random.randint(1,5)); count("arrows"); check("arrows")
    if time.time()-t0>minute*60: marks.append((minute,mem()[0])); minute+=1
save(2.5); saves+=1; check("final",1.0)
k,b=verify_saved("final save"); stop=True
rss=[x[1] for x in samples]
print("ran %.0f s | %s"%(time.time()-t0, ", ".join("%s: %d"%kv for kv in sorted(ops.items()))))
print("changed cells at the end: %d | undo steps: %d"%(len(over),len(undo)))
print("memory MB — after open: %d | at each minute: %s | at the end: %d"%(opened[0], " ".join(str(m) for _,m in marks), mem()[0]))
print("memory MB — highest sample %d | highest the kernel saw (VmHWM) %d | median sample %d"%(max(rss), mem()[1], sorted(rss)[len(rss)//2]))
print("final saved file: %d cells compared, %d wrong | failed checks: %d"%(k,b,len(fails))); print("\n".join(f[:220] for f in fails[:8]))
