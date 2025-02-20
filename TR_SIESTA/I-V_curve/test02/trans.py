import os
import math
import shutil

os.system("ls -l | awk '/^d/{print $NF}' > list")

print('This code made by JW.Chae at 22/03/01.')
print('Code is for calculated the I-V curve.')
print('Sub-directory name must be only constructed the number. Does not import unit!')
print('##############################')

f1 = open("./list","r")
tmp_list1=[]
tmp_list2=[]
tmp_list3=[]
x=0
while True:
 a = f1.readline().rstrip('\n')
 if not a: break
 x = x+1
 tmp_list1.append(a)

for i in range (0,x):
 tmp_list2 = float(tmp_list1[i])
 tmp_list3.append(tmp_list2)

f1.close()

num_point = x

print("number of point: %d" %num_point)

#######################################################################

print('TS.Volatge','\t','Current')

base_path = os.getcwd()

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
    
    V = str(Voltage)
    J = str(I)

    vol_list.append(V)
    cur_list.append(J)

    f1.close()
    
    os.system("rm ./siesta_trans")

    print('%lf' %zz,'\t','%lf' %I)
    
    os.chdir("%s" %base_path)

#os.system("find . -type f -name 'current' -exec cat {} + > V-I")
print('##############################')
print('post-progress done. write the V-I file')

#print(vol_list)
#print(cur_list)

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

#os.system("rm ./list")

print('Program done. Plz check the V-I file')
