import zipfile, subprocess, sys, os, shutil
for f in sorted(os.listdir("xl")):
    if not f.endswith(".xlsx"): continue
    d="out/"+f; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    r=subprocess.run(["/usr/bin/time","-f","MEM %M","./zipx"],env={"IN":"xl/"+f,"OUT":d},capture_output=True,text=True)
    L=r.stdout.split("\n"); names=[l.split(" ",2)[2] for l in L if l.startswith("ENTRY ")]
    z=zipfile.ZipFile("xl/"+f); same=names==z.namelist() and all(open(d+"/"+str(i),"rb").read()==z.read(n) for i,n in enumerate(names))
    summ=[l for l in L if l.startswith("SUMMARY")]
    print("  %-24s %s identical-to-python=%s peak=%s KB"%(f, summ[0][8:] if summ else "FAILED "+r.stdout[-200:], same, r.stderr.split()[-1]))
