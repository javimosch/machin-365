import subprocess, os, random, time, re, sys
out=sys.argv[1]; bad=0; gens=set()
for i in range(200):
    p=subprocess.Popen(["./save"], env={"OUT":out})
    time.sleep(random.uniform(0.03,0.25)); p.kill(); p.wait()
    if os.path.exists(out):
        L=open(out).read().split("\n")
        ok = L[0].startswith("begin ") and L[-2]=="end "+L[0][6:] and set(L[1:-2])=={L[0][6:]}
        bad += not ok; gens.add(L[0])
    else: bad += i>0
print("200 forced kills: damaged or missing file %d times; distinct saved generations seen %d" % (bad,len(gens)))
