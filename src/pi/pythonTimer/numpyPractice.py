import numpy as np

a = np.array([(2,3,4),(1,7,9)])
print(a)

b = np.array(['time','distance','ax','ay','az','gx','gy','gz'])
print(b)

c = np.array([10,20,30])
print(c)

a = np.vstack((a,c))
print(a)
