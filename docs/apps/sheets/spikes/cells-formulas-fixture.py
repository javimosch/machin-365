# Hand-made (not Excel): 20,000 x 26 with 6 formula columns, half of them shared, all with stored results.
import zipfile, random
random.seed(9)
exec(open("excel_style.py").read().split("with zipfile.ZipFile")[0])
L=lambda c: chr(65+c)
rows=[]
for r in range(1,20001):
    cs=[]
    for c in range(26):
        if c<20: cs.append('<c r="%s%d"><v>%d</v></c>'%(L(c),r,random.randint(1,10**6)))
        elif c<23: cs.append('<c r="%s%d"><f>A%d+B%d*%d</f><v>0</v></c>'%(L(c),r,r,r,c))
        else:
            src=L(c-23)
            if r==1: cs.append('<c r="%s1"><f t="shared" ref="%s1:%s20000" si="%d">%s1*2</f><v>0</v></c>'%(L(c),L(c),L(c),c-23,src))
            else: cs.append('<c r="%s%d"><f t="shared" si="%d"/><v>0</v></c>'%(L(c),r,c-23))
    rows.append('<row r="%d">%s</row>'%(r,"".join(cs)))
files={k:v for k,v in files.items()}
files["xl/worksheets/sheet1.xml"]='<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+"".join(rows)+'</sheetData></worksheet>'
files["xl/sharedStrings.xml"]='<?xml version="1.0"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"/>'
with zipfile.ZipFile("xl/formulas.xlsx","w",zipfile.ZIP_DEFLATED) as z:
    for n,s in files.items(): z.writestr(n,s.encode())
