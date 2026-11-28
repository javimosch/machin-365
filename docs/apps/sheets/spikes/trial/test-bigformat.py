exec(open("harness.py").read())
PID=sys.argv[4]
def mem():
    s=open("/proc/%s/status"%PID).read(); return int(re.search(r"VmRSS:\s+(\d+)",s).group(1))//1024, int(re.search(r"VmHWM:\s+(\d+)",s).group(1))//1024
time.sleep(1); print("  after open: resident %d MB"%mem()[0])
extend("Right",19); extend("Next",39)
t=time.time(); key("Control_L","b",wait=0.1)
while int(read_dump()[-2].split()[1])<10000 and time.time()-t<40: time.sleep(0.05)
print("  bold on %s cells applied after %.1f s | resident %d MB"%(read_dump()[-2].split()[1], time.time()-t, mem()[0]))
for i in range(3):
    if os.path.exists(OUT): os.remove(OUT)
    t=time.time(); key("Control_L","s",wait=0.1)
    while not os.path.exists(OUT) and time.time()-t<60: time.sleep(0.02)
    time.sleep(1.0); print("  save %d: %.1f s | resident after %d MB | highest so far %d MB"%(i+1,time.time()-t-1.0,*mem()))
