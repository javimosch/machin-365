exec(open("harness.py").read())
X.XDefaultRootWindow.restype=L; X.XDefaultRootWindow.argtypes=[P]; X.XGetImage.restype=P; X.XGetImage.argtypes=[P,L,C.c_int,C.c_int,C.c_uint,C.c_uint,L,C.c_int]; X.XGetPixel.restype=L; X.XGetPixel.argtypes=[P,C.c_int,C.c_int]; X.XDestroyImage.argtypes=[P]
root=X.XDefaultRootWindow(d); import statistics as st
def grab():
    im=X.XGetImage(d,root,0,40,700,500,L(-1).value,2)
    v=tuple(X.XGetPixel(im,x,y) for x in range(0,700,5) for y in range(0,500,5)); X.XDestroyImage(im); return v
def latency(name, n=30):
    res=[]
    for i in range(n):
        time.sleep(0.25); before=grab()
        T.XTestFakeKeyEvent(d,kc(name),1,0); X.XFlush(d); t=time.time()
        while grab()==before and time.time()-t<3: time.sleep(0.002)
        res.append((time.time()-t)*1000); T.XTestFakeKeyEvent(d,kc(name),0,0); flush()
    print("  %-10s to changed screen: median %d ms, worst %d ms (%d presses; screen sampling adds a few ms)"%(name,st.median(res),max(res),n))
time.sleep(1.0); latency("Down"); latency("Next")
def save_time(label):
    if os.path.exists(OUT): os.remove(OUT)
    T.XTestFakeKeyEvent(d,kc("Control_L"),1,0); flush(0.02); t=time.time(); key("s",wait=0)
    T.XTestFakeKeyEvent(d,kc("Control_L"),0,0); X.XFlush(d)
    while not os.path.exists(OUT) and time.time()-t<30: time.sleep(0.01)
    print("  save %-28s file in place after %d ms (the window does not redraw meanwhile)"%(label,(time.time()-t)*1000))
for i in range(3): save_time("with no changes" if i==0 else "again")
enter_value("5"); save_time("with 1 change")
nav("Left",26)
for i in range(5): copy_paste(4,20,2)
time.sleep(1.5); save_time("with %d changed cells"%len(over))
