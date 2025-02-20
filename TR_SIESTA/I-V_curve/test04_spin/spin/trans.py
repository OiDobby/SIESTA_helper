import os
import math
import shutil
import glob

os.system("ls -l | awk '/^d/{print $NF}' > list")

print('This code made by JW.Chae at 22/05/26.')
print('Code is for calculated the I-V curve.')
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

#print(tmp_list3)
#print(tmp_list1)

f1.close()

num_point = x

base_path = os.getcwd()

#######################################################################non_spin
def non_spin():
    
    print('TS.Volatge','\t','Current')
    
    vol_list=[]
    cur_list=[]
    
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
    
    #    print("dE: %lf" %dE)
    
        for i in range (0,x):
            energy = TMP_list3[i][0]
            Dfd = (1/(1+math.exp((energy-VL)/(k*T))))-(1/(1+math.exp((energy-VR)/(k*T))))
            if Dfd < 1e-16:
                if Dfd > -1e-16:
                    Dfd = 0
            TMP_list3[i].append(Dfd)
        
        I = 0
        for i in range (0,x):
            I = I+(TMP_list3[i][1]*TMP_list3[i][2]*dE)
        
        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]
    
        I = I*38.7
    
        for i in range (0,x):
            TMP_list2 = list(map(str,TMP_list3[i]))
            TMP_list1.append(TMP_list2)
        
        V = str(f'{Voltage: .6f}')
        J = str(f'{I: .6f}')
    
        vol_list.append(V)
        cur_list.append(J)
    
        f1.close()
        
        os.system("rm ./siesta_trans")

        print('%lf' %zz,'\t','%lf' %I)
        
        os.chdir("%s" %base_path)

    #######################################################################print program state
    
    #os.system("find . -type f -name 'current' -exec cat {} + > V-I")
    print('##############################')
    print('post-progress done. write the V-I file')
    
    #######################################################################make plot file
    
    f3 = open("./V-I", "w")
    #f3.write('Voltage')
    #f3.write('\t')
    #f3.write('Current')
    #f3.write('\n')
    for i in range (0,num_point):
        f3.write(vol_list[i])
        f3.write('\t')
        f3.write(cur_list[i])
        f3.write('\n')
    f3.close()
#######################################################################non_spin-fin



#######################################################################spin
def spin():
    
    print('TS.Volatge','\t','Current_up','\t','Current_dn')
    
    vol_list=[]
    cur_list_up=[]
    cur_list_dn=[]
    
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
    
        for i in range (0,x):
            energy = TMP_list3[i][0]
            Dfd = (1/(1+math.exp((energy-VL)/(k*T))))-(1/(1+math.exp((energy-VR)/(k*T))))
            if Dfd < 1e-16:
                if Dfd > -1e-16:
                    Dfd = 0
            TMP_list3[i].append(Dfd)
        
        Ia = 0
        for i in range (0,x):
            Ia = Ia+(TMP_list3[i][1]*TMP_list3[i][2]*dE)
        
        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]
    
        Ia = Ia*38.7
    
        for i in range (0,x):
            TMP_list2 = list(map(str,TMP_list3[i]))
            TMP_list1.append(TMP_list2)
        
        V = str(f'{Voltage: .6f}')
        J = str(f'{Ia: .6f}')
    
        vol_list.append(V)
        cur_list_up.append(J)
    
    
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

        for i in range (0,x):
            energy = TMP_list3[i][0]
            Dfd = (1/(1+math.exp((energy-VL)/(k*T))))-(1/(1+math.exp((energy-VR)/(k*T))))
            if Dfd < 1e-16:
                if Dfd > -1e-16:
                    Dfd = 0
            TMP_list3[i].append(Dfd)

        Ib = 0
        for i in range (0,x):
            Ib = Ib+(TMP_list3[i][1]*TMP_list3[i][2]*dE)

        TMP_list1 = [0 for _ in range (-1)]
        TMP_list2 = [0 for _ in range (-1)]

        Ib = Ib*38.7

        for i in range (0,x):
            TMP_list2 = list(map(str,TMP_list3[i]))
            TMP_list1.append(TMP_list2)

        J = str(f'{Ib: .6f}')

        cur_list_dn.append(J)


        f1.close()

        os.system("rm ./siesta_trans-dn")


        print('%lf' %zz,'\t','%lf' %Ia,'\t','%lf' %Ib)
        
        os.chdir("%s" %base_path)

    #######################################################################print program state
    
    #os.system("find . -type f -name 'current' -exec cat {} + > V-I")
    print('##############################')
    print('post-progress done. write the V-I file')
    
    #######################################################################make plot file
    
    f3 = open("./V-I", "w")
    #f3.write('Voltage')
    #f3.write('\t')
    #f3.write('Current')
    #f3.write('\n')
    for i in range (0,num_point):
        f3.write(vol_list[i])
        f3.write('\t')
        f3.write(cur_list_up[i])
        f3.write('\t')
        f3.write(cur_list_dn[i])
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

print('Program done. Plz check the V-I file')
