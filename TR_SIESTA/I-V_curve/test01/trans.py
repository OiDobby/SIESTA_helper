import os
import math

os.system("cp **.TRANS_Left-Right ./siesta_trans")
print("What is the TS.Volatge value in your calculation? Please enter that in only number.")
Voltage = float(input("TS.Voltage::"))

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

for i in range (0,x):
    TMP_list2 = list(map(str,TMP_list3[i]))
    TMP_list1.append(TMP_list2)

f2 = open("./siesta_trans.TMP", "w")

J = str(I)
f2.write("I=")
f2.write(J)
f2.write("\n")

for i in range (0,x):
    for j in range (0,3):
        f2.write(TMP_list1[i][j])
        f2.write("  ")
    f2.write("\n")

f2.close()
f1.close()

f3 = open("./current", "w")
J = str(I)
V = str(Voltage)
f3.write(V)
f3.write("\t")
f3.write(J)
f3.close()

os.system("rm ./siesta_trans.TMP")

print("program done. Current is: %lf" %I)
