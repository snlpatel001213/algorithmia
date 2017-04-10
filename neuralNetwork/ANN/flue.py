__author__ = 'Decepticonn'
import random
import math
import numpy


w1=[  #0 w1 00            01                 02             3               4                 5               6         7
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#0
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#1
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#2
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#3
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#4
    [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()],#5
  ]
theta1=[random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random() ]
deltatheta1=[0,0,0,0,0,0,0,0]
w2=[     #0              1               2               3
    [random.random(),random.random(),random.random(),random.random()],#0
    [random.random(),random.random(),random.random(),random.random()],#1
    [random.random(),random.random(),random.random(),random.random()],#2
    [random.random(),random.random(),random.random(),random.random()],#3
    [random.random(),random.random(),random.random(),random.random()],#4
    [random.random(),random.random(),random.random(),random.random()],#5
    [random.random(),random.random(),random.random(),random.random()],#6
    [random.random(),random.random(),random.random(),random.random()],#7

  ]
theta2=[random.random(),random.random(),random.random(),random.random()]
deltatheta2=[0,0,0,0]
w3=[    #0next layey
     [random.random()],#0 previous layer
     [random.random()],#1
     [random.random()],#2
     [random.random()] #3
   ]
theta3=[random.random()]
deltatheta3=0
y1=[0,0,0,0,0,0,0,0]
y2=[0,0,0,0]
y3=[0]
errorgrad2=[0,0,0,0]
errorgrad1=[0,0,0,0,0,0,0,0]
errorgrad0=[0,0,0,0,0,0]
dw01=[
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]
      ]
dw12=[
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]

      ]
dw23=[
          [0],[0],[0],[0]
     ]
print(y1)
alpha=0.9
PP=0
QQ=0
RR=0

with open('data.txt','r') as f:

    for line in f:
        errorsq=0
       # line = file.read()
        #print (line)
        line=line.strip()
        digit= line.split(" ")
        #print (digit)
        for i in range(8):#second layer
            for j in range(6):#first layer
                PP+=w1[j][i]*int(digit[j])
        P=numpy.exp(-(PP - deltatheta1[i]))
        y1[i]+=1/(1+(P))
                #print ("output one and two",i,y1[i],w1[j][i],int(digit[j]))
                #print(y1)
        for i in range(4):#third layer
            for j in range(8):#second layer
                QQ += w2[j][i]*y1[j]
        Q=numpy.exp(-(QQ-deltatheta2[i]))
        y2[i]+=1/(1+(Q))
                #print ("output two and three",i,y2[i],w2[j][i],y1[j])
                #print(y2)
        for i in range(1):#forth layer
            for j in range(4):#third layer
                RR += w3[j][i]*y2[j]
        R=numpy.exp(-(RR-deltatheta3))
        y3[i]+=1/(1+R)
                #print ("output two and three",i,y3[i],w3[j][i],y2[j])
                #print(y3)

        #finding gradient

        error=int(digit[6])-y3[0]
        errorgrad3=y3[0]*(1-y3[0])*error
        for i in range(4):#third and forth layer
                #print ("w3[i][0]",w3[i][0])
                errorgrad2[i]=y2[i]*(1-y2[i])*errorgrad3*w3[i][0]
        #print("W#",w3)
        #print ("error gradient2",errorgrad2)

        for i in range(8):#second and third layer
            for j in range(4):#third layer
                errorgrad1[i]+=y1[i]*(1-y1[i])*errorgrad2[j]*w2[i][j]
        #print("W#",w2)
        #print ("error gradient1",errorgrad1)

        #for i in range(6):#first and second layer
           # for j in range(8):
              #  errorgrad0[i]+=(int(digit[i]))*(1-(int(digit[i])))*errorgrad1[j]*w1[i][j]
              #  print(i,(int(digit[i])),(1-(int(digit[i]))),errorgrad1[j],w1[i][j])
       # print("W#",w1)
        #print("digit",digit)
       # print ("error gradient0",errorgrad0)

        #weight deviation
        #print("digit",digit)
        for i in range(8):#01 layer
            for j in range(6):
                dw01[j][i]=0.95*alpha*(int(digit[j]))*errorgrad1[i]
        #print("weight deviation 01 ",dw01)
        for i in range(4):##12 layer
            for j in range(8):
                dw12[j][i]=0.95*alpha*y1[j]*errorgrad2[i]
        #print("weight deviation 12 ",dw12)
        for i in range(1):##23 layer
            for j in range(4):
                dw23[j][i]=0.95*alpha*y2[j]*errorgrad3
        #print("weight deviation 23 ",dw23)

        #weight correction
        for i in range(8):#01 layer
            for j in range(6):
                w1[j][i]=w1[j][i]+dw01[j][i]
        for i in range(4):#01 layer
            for j in range(8):
                w2[j][i]=w2[j][i]+dw12[j][i]
        for i in range(1):#01 layer
            for j in range(4):
                w3[j][i]=w3[j][i]+dw23[j][i]

        #theta calculation
        for i in range(8):#01 layer
            deltatheta1[i]=alpha*(-1)*errorgrad1[i]
        for i in range(4):#01 layer
            deltatheta2[i]=alpha*(-1)*errorgrad2[i]
            errorsq+=error*error
        deltatheta3=alpha*(-1)*errorgrad3
        print("################################",errorsq,error)
        print ("output",y3,"desired",digit[6])
        if errorsq<0.001:
             break







