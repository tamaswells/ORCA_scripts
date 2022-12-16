import sys
import os
if len(sys.argv) ==1:
    raise SystemError("write usage: python orca5_to_orca4.py your_orca_log")
if not os.path.exists(sys.argv[1]):
    raise SystemError("Your orca log does not exist")
with open(sys.argv[1]) as reader:
    all = reader.readlines()
    find_start = False
    for index,line in enumerate(all):
        if " Mode   freq       eps      Int      T**2         TX        TY        TZ" in line:
            start = index
            find_start = True
        if (line == "\n" or line == "\r\n") and find_start == True:
            end = index
            break
    sets  = []
    for i in range(start + 3,end):
        tmp = all[i].strip("\r\n").strip("\n").strip(")").split()
        if len(tmp) == 8:
            sets.append("%s %s %s ( %f %f %f )\n" %(tmp[0],tmp[1],tmp[3],float(tmp[5].lstrip("("))*42.2561,float(tmp[6])*42.2561,float(tmp[7])*42.2561))
        elif len(tmp) == 9:
            sets.append("%s %s %s ( %f %f %f )\n" %(tmp[0],tmp[1],tmp[3],float(tmp[6].lstrip("("))*42.2561,float(tmp[7])*42.2561,float(tmp[8])*42.2561))        
    all[start] = " Mode    freq (cm**-1)   T**2         TX         TY         TZ\n"
    all.pop(start+1)
    ii = 0
    for i in range(start + 2,end-1):
        all[i] = sets[ii]
        ii+=1
with open("new"+sys.argv[1],'w') as writer:
    writer.writelines(all)