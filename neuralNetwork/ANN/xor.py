import math
import random
array = [[0,1,1],[1,1,0],[1,0,1],[0,0,0]]

w13=0.5
w14=0.9
w23=0.4
w24=1.0
w35=-1.2
w45=1.1
t3=0.8
t4=-0.1
t5=0.3
alpha=0.5
errors = 0
error = 0
print (error,">>",errors)
count=0
for j in range(10000):
    print(">>>>>>>>>>>>>>>>>>>>>>",errors)
    errors=0
    for i in range(4):
         y3=1/(1+math.exp(-((array[i][0]*w13)+(array[i][1]*w23))))
         y4=1/(1+math.exp(-(array[i][0]*w14+array[i][1]*w24)))
         y5=1/(1+math.exp(-(y3*w35+y4*w45)))
         error=array[i][2]-y5
         del5=y5*(1-y5)*error
         dw35=alpha*y3*del5
         dw45=alpha*y4*del5
         dt5=alpha*(-1)*del5

         del3=y3*(1-y3)*del5*w35
         del4=y4*(1-y4)*del5*w45

        #changes
         dw13=alpha*array[i][0]*del3
         dw23=alpha*array[i][1]*del3
         dt3=alpha*(-1)*del3
         dw14=alpha*array[i][0]*del4
         dw24=alpha*array[i][1]*del4
         dt4=alpha*(-1)*del4
         print (">>>>>>>>>>>>>>",del4,del3,del5)
         #corrections
         w13=w13+dw13
         w14=w14+dw14
         w23=w23+dw23
         w24=w24+dw24
         w35=w35+dw35
         w45=w45+dw45
         t3=t3+dt3
         t4=t4+dt4
         t5=t5+dt5
         if y5<0.5:
             temporary=0
         else:
             temporary=1

         print (">>",array[i][0],array[i][1],">>",temporary," actual ",array[i][2])
         #print (">>>>>",error*error)
         errors=errors+(error*error)
         if errors<0.001:
             break


