exec(open("harness.py").read())
time.sleep(0.5)
enter_value("1234.5"); check("type a number")
over[(2,1)]=("number","1234.6")          # the script now expects something that was never typed
check("control: wrong value expected"); save(); verify_saved("control: saved file")
over[(2,1)]=("number","1234.5"); enter_value("8"); do_undo(); check("control: an undo the app never got")
print("controls that were caught:",len(fails),"(3 expected)"); print("\n".join(f[:150] for f in fails))
