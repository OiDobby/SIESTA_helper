import os
import math
import shutil
import glob

os.system("ls -l | awk '/^d/{print $NF}' > list")

print('This code made by J.Chae at 22/09/19.')
print('Code is for calculated the conductance.')
print('Sub-directory name must be only constructed the number. Does not import unit!')
print('If you calculated the -x.xx eV bias, you must be sub-directory name about -x.xx eV to _x.xx')

f1 = open("./list","r")
tmp_list1=[]
tmp_list2=[]
tmp_list3=[]
tmp_list4=[]
x=0
while True:
 a = f1.readline().rstrip('\n')
 if not a: break
 x = x+1
 tmp_list1.append(a)

for i in tmp_list1:
    temp = i.replace('_','-')
    tmp_list4.append(temp)

for i in range (0,x):
 tmp_list2 = float(tmp_list4[i])
 tmp_list3.append(tmp_list2)

tmp_list1=[]
tmp_list2=[]

tmp_list3.sort()
tmp_list2 = list(map(str,tmp_list3))
for i in tmp_list2:
    temp = i.replace('-','_')
    tmp_list1.append(temp)

#print(tmp_list3)    #float_number (voltage)
#print(tmp_list1)    #string (voltage)

f1.close()

num_point = x

base_path = os.getcwd()

#######################################################################non_spin
def non_spin():
    
    print('TS.Volatge','\t','Conductance')
    
    vol_list=[]
    cond_list=[]
    
    for k in range (0,num_point): 
        yy=tmp_list1[k]
        zz=tmp_list3[k]
        dir_path = os.path.abspath("%s" %yy)
        os.chdir("%s" %dir_path)
        
        os.system("cp ./**.TRANS_Left-Right ./siesta_trans")
        #print("What is the TS.Volatge value in your calculation? Please enter that in only number.")
        Voltage = zz
        
        f1 = open("./siesta_trans", "r")
        
        for i in range(0,3):
            line = f1.readline()
        
        TMP_list1 = []
        TMP_list2 = []
        TMP_list3 = []
        x = 0
        
        while True:
            a = f1.readline().rstrip('\n')
            b = " ".join(a.split())
            c = b.split(' ')
            if not a: break
            x = x+1
            TMP_list1.append(c)
        
        for i in range (0,x):
            TMP_list2 = list(map(float,TMP_list1[i]))
            TMP_list3.append(TMP_list2)
        
        k = 8.617343e-5
        T = 300
        VL = Voltage/2
        VR = -1*Voltage/2
        dE = TMP_list3[1][0]-TMP_list3[0][0]
    
        #print("dE: %lf" %dE)
    
        cond=0

        for i in range (0,x):
            if TMP_list3[i][0] <= -0.5*dE:
                cond_v = TMP_list3[i][1]
            elif TMP_list3[i][0] == 0:
                cond = TMP_list3[i][1]
            elif TMP_list3[i][0] >= 0.5*dE:
                if TMP_list3[i][0] < 1.5*dE:
                    cond_c = TMP_list3[i][1]
        
        if cond == 0:
            cond = (cond_v + cond_c)/2

        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]
            
        cond = cond*1.602/4.135*100
    
        for i in range (0,x):
            TMP_list2 = list(map(str,TMP_list3[i]))
            TMP_list1.append(TMP_list2)
        
        V = str(f'{Voltage: .6f}')
        J = str(f'{cond: .6f}')
    
        vol_list.append(V)
        cond_list.append(J)
    
        f1.close()
        
        os.system("rm ./siesta_trans")

        print('%lf' %zz,'\t','%lf' %cond)
        
        os.chdir("%s" %base_path)

    #######################################################################print program state
    
    #os.system("find . -type f -name 'current' -exec cat {} + > V-I")
    print('##############################')
    print('post-progress done. write the Cond.dat file')
    
    #######################################################################make plot file
    
    f3 = open("./Cond.dat", "w")
    #f3.write('Voltage')
    #f3.write('\t')
    #f3.write('Current')
    #f3.write('\n')
    for i in range (0,num_point):
        f3.write(vol_list[i])
        f3.write('\t')
        f3.write(cond_list[i])
        f3.write('\n')
    f3.close()
#######################################################################non_spin-fin



#######################################################################spin
def spin():
    
    print('TS.Volatge','\t','Cond_up','\t','Cond_dn')
    
    vol_list=[]
    cond_list_up=[]
    cond_list_dn=[]
    
    for k in range (0,num_point): 
        yy=tmp_list1[k]
        zz=tmp_list3[k]
        dir_path = os.path.abspath("%s" %yy)
        os.chdir("%s" %dir_path)
        
        os.system("cp ./**UP.TRANS_Left-Right ./siesta_trans-up")
        #print("What is the TS.Volatge value in your calculation? Please enter that in only number.")
        Voltage = zz
        
        f1 = open("./siesta_trans-up", "r")
        
        for i in range(0,3):
            line = f1.readline()
        
        TMP_list1 = []
        TMP_list2 = []
        TMP_list3 = []
        x = 0
        
        while True:
            a = f1.readline().rstrip('\n')
            b = " ".join(a.split())
            c = b.split(' ')
            if not a: break
            x = x+1
            TMP_list1.append(c)
        
        for i in range (0,x):
            TMP_list2 = list(map(float,TMP_list1[i]))
            TMP_list3.append(TMP_list2)
        
        k = 8.617343e-5
        T = 300
        VL = Voltage/2
        VR = -1*Voltage/2
        dE = TMP_list3[1][0]-TMP_list3[0][0]
    
    #    print("dE: %lf" %dE)

        cond=0

        for i in range (0,x):
            if TMP_list3[i][0] <= -0.5*dE:
                cond_v = TMP_list3[i][1]
            elif TMP_list3[i][0] == 0:
                cond = TMP_list3[i][1]
            elif TMP_list3[i][0] >= 0.5*dE:
                if TMP_list3[i][0] < 1.5*dE:
                    cond_c = TMP_list3[i][1]

        if cond == 0:
            cond = (cond_v + cond_c)/2

        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]

        cond_up = cond*1.602/4.135*10e+2
    
        V = str(f'{Voltage: .6f}')
        J = str(f'{cond_up: .6f}')
    
        vol_list.append(V)
        cond_list_up.append(J)
    
    
        f1.close()
        
        os.system("rm ./siesta_trans-up")
   
        os.system("cp ./**DN.TRANS_Left-Right ./siesta_trans-dn")
        #print("What is the TS.Volatge value in your calculation? Please enter that in only number.")

        f1 = open("./siesta_trans-dn", "r")

        for i in range(0,3):
            line = f1.readline()

        TMP_list1 = []
        TMP_list2 = []
        TMP_list3 = []
        x = 0

        while True:
            a = f1.readline().rstrip('\n')
            b = " ".join(a.split())
            c = b.split(' ')
            if not a: break
            x = x+1
            TMP_list1.append(c)

        for i in range (0,x):
            TMP_list2 = list(map(float,TMP_list1[i]))
            TMP_list3.append(TMP_list2)

        k = 8.617343e-5
        T = 300
        VL = Voltage/2
        VR = -1*Voltage/2
        dE = TMP_list3[1][0]-TMP_list3[0][0]

    #    print("dE: %lf" %dE)

        cond=0

        for i in range (0,x):
            if TMP_list3[i][0] <= -0.5*dE:
                cond_v = TMP_list3[i][1]
            elif TMP_list3[i][0] == 0:
                cond = TMP_list3[i][1]
            elif TMP_list3[i][0] >= 0.5*dE:
                if TMP_list3[i][0] < 1.5*dE:
                    cond_c = TMP_list3[i][1]

        if cond == 0:
            cond = (cond_v + cond_c)/2

        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]
        
        cond_dn = cond*1.602/4.135*10e+2

        J = str(f'{cond_dn: .6f}')

        cond_list_dn.append(J)


        f1.close()

        os.system("rm ./siesta_trans-dn")


        print('%lf' %zz,'\t','%lf' %cond_up,'\t','%lf' %cond_dn)
        
        os.chdir("%s" %base_path)

    #######################################################################print program state
    
    #os.system("find . -type f -name 'current' -exec cat {} + > V-I")
    print('##############################')
    print('post-progress done. write the Cond.dat file')
    
    #######################################################################make plot file
    
    f3 = open("./Cond.dat", "w")
    #f3.write('Voltage')
    #f3.write('\t')
    #f3.write('Current')
    #f3.write('\n')
    for i in range (0,num_point):
        f3.write(vol_list[i])
        f3.write('\t')
        f3.write(cond_list_up[i])
        f3.write('\t')
        f3.write(cond_list_dn[i])
        f3.write('\n')
    f3.close()
#######################################################################non_spin-fin

yy=tmp_list1[0]
dir_path = os.path.abspath("%s" %yy)
os.chdir("%s" %dir_path)
if glob.glob('./**UP.TRANS_Left-Right') and glob.glob('./**.TBT_DN.TRANS_Left-Right'):
    print("spin")
    nspin=1
elif glob.glob('./**.TRANS_Left-Right'):
    print("non_spin")
    nspin=0
else:
    print("Some files missing")
    quit()

os.chdir("%s" %base_path)

print('##############################')
print("number of point: %d" %num_point)

if nspin==1:
    spin()
elif nspin==0:
    non_spin()
else:
    quit()

os.system("rm ./list")

print('Program done. Plz check the Cond.dat file')
