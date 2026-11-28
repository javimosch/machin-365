exec(open("harness.py").read())
import subprocess
passed=0
def clickxy(x,y,b=1,wait=0.6):
    T.XTestFakeMotionEvent(d,-1,x,y,0); flush(0.2)
    for v in (1,0): T.XTestFakeButtonEvent(d,b,v,0); flush(0.12)
    time.sleep(wait)
BTN=dict(Save=36,Undo=94,Redo=153,Cut=211,Copy=263,Paste=322,Clear=382,Bold=444,Number=509,Euro=581,Date=643,Sum=704,Find=757)
def button(n): clickxy(BTN[n],21)
def cell_xy(r,c): return 70+(c-1)*112+50, 122+(r-1)*26     # rows 1.. while the grid is at the top
def click_cell(r,c): clickxy(*cell_xy(r,c)); cur[:]=[r,c]; anchor[:]=[r,c]
def right(r,c): x,y=cell_xy(r,c); clickxy(x,y,3); return x,y
MENU=dict(Cut=20,Copy=49,Paste=78,Clear=107,Bold=137,Sum=166)
def pick(at,n): clickxy(at[0]+40,at[1]+MENU[n])
def state():
    time.sleep(0.3); L_=read_dump(); out={}
    for l in L_[1:-2]:
        k,v=l.split("=",1); m=re.match(r"([A-Z])(\d+)",k); r=int(m.group(2)); c=ord(m.group(1))-64
        out[(r%10000000, c, r>=10000000)]=v
    return L_[0].split(), out
def val(r,c): return state()[1].get((r,c,False))
def sty(r,c): return state()[1].get((r,c,True))
def expect(what, cond, detail=""):
    global passed
    if cond: passed+=1; print("  ok   "+what)
    else: fails.append(what); print("  FAIL "+what+"  "+str(detail)[:220])
def undo_key(): key("Control_L","z",wait=0.6)
b=lambda r,c: base[(r,c)][1]
time.sleep(1)
# ---- cut ----
click_cell(2,3); extend("Down",2); key("Control_L","x",wait=0.8)
expect("Ctrl+X clears the cut cells", all(val(r,3)=="c:" for r in (2,3,4)), state())
click_cell(2,12) if False else None
click_cell(8,4); key("Control_L","v",wait=0.8)
expect("what was cut pastes elsewhere", [val(8,4),val(9,4),val(10,4)]==["n:"+b(2,3),"n:"+b(3,3),"n:"+b(4,3)], state())
undo_key(); undo_key()
expect("two undos put everything back (cut is one step)", state()[1]=={}, state())
click_cell(2,2); extend("Right",1); button("Cut")
expect("toolbar Cut", val(2,2)=="c:" and val(2,3)=="c:", state())
click_cell(12,2); button("Paste")
expect("toolbar Paste", val(12,2)=="t:"+b(2,2) and val(12,3)=="n:"+b(2,3), state())
undo_key(); undo_key()
# ---- right-click menu ----
click_cell(3,2); at=right(3,2); subprocess.run(["import","-display",":95","-window","root","menu-test.png"]); pick(at,"Cut")
expect("menu Cut", val(3,2)=="c:", state())
at=right(5,5); pick(at,"Paste"); cur[:]=[5,5]; anchor[:]=[5,5]
expect("right-click moves to the cell, menu Paste writes there", val(5,5)=="t:"+b(3,2), state())
click_cell(6,3); extend("Down",1); at=right(7,3); pick(at,"Clear")
expect("right-click inside a selection keeps it; menu Clear", val(6,3)=="c:" and val(7,3)=="c:", state())
n_before=state()[1]; at=right(9,2); key("Escape",wait=0.6)
expect("Escape closes the menu and changes nothing", state()[1]==n_before, state())
at=right(9,2); clickxy(1000,600)
head,after=state()
expect("a click outside closes it without acting or moving", after==n_before and head[1]=="B9", head)
at=right(10,6); pick(at,"Copy"); at=right(14,6); pick(at,"Paste"); cur[:]=[14,6]; anchor[:]=[14,6]
expect("menu Copy then Paste", val(14,6)=="t:"+b(10,6), state())
click_cell(15,6); at=right(15,6); key("Down",wait=0.4)
expect("keys do not move the grid while the menu is open", state()[0][1]=="F15", state()[0])
key("Escape",wait=0.5); button("Clear")
expect("toolbar Clear", val(15,6)=="c:", state())
# ---- formats ----
click_cell(2,7); extend("Right",1); extend("Down",1); button("Bold")
expect("Bold on a 2x2 selection", all(sty(r,c)=="1:x" for r in (2,3) for c in (7,8)), state())
click_cell(2,7); key("Control_L","b",wait=0.6)
expect("Ctrl+B on a bold cell turns it off", sty(2,7)=="0:x" and sty(2,8)=="1:x", state())
undo_key()
expect("undo restores bold", sty(2,7)=="1:x", state())
click_cell(4,7); extend("Down",1); button("Euro")
expect("Euro format", sty(4,7)=="x:eur" and sty(5,7)=="x:eur", state())
click_cell(6,7); button("Number")
expect("Number format", sty(6,7)=="x:num", state())
click_cell(7,7); enter_value("46354"); click_cell(7,7); button("Date")
expect("Date format", sty(7,7)=="x:date" and val(7,7)=="n:46354", state())
click_cell(8,7); enter_value("12.5"); click_cell(8,7); button("Euro"); at=right(8,7); pick(at,"Bold")
expect("value, euro and bold together on one cell", val(8,7)=="n:12.5" and sty(8,7)=="1:eur", state())
click_cell(25-8,1); at=right(17,1); pick(at,"Bold")
expect("bold on a cell whose value is unchanged", sty(17,1)=="1:x" and val(17,1) is None, state())
subprocess.run(["import","-display",":95","-window","root","formats.png"])
# ---- sum ----
click_cell(18,3); extend("Down",2); button("Sum"); cur[:]=[21,3]; anchor[:]=[21,3]
expect("Sum puts a total under the selection", val(21,3)=="f:SUM(C18:C20)" and state()[0][1]=="C21", state())
# ---- find ----
button("Find"); type_value("150-8"); key("Return",wait=1.5)
expect("Find goes to the match", state()[0][1]=="I151", state()[0])
key("Escape",wait=0.6)
time.sleep(0.3); button("Save"); time.sleep(2.5)
json_={"values":{}, }
import pickle; pickle.dump({k:v for k,v in state()[1].items()}, open("expected.pkl","wb"))
print("on screen: %d passed, %d failed"%(passed,len(fails)))
