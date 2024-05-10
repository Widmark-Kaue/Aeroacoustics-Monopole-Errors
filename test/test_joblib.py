#%% libs
import time 
from joblib import Parallel,delayed 
import math 
  
#%% test
  
# Normal 
t1 = time.time() 
r = [math.factorial(int(math.sqrt(i**3))) for i in range(100,1000)]   
t2 = time.time() 
print(f'Time normal = {t2-t1} s') 

# 2 Core 
t1 = time.time()
r1 = Parallel(n_jobs=2)(delayed(math.factorial) (int(math.sqrt(i**3))) for i in range(100,1000)) 
t2 = time.time() 
print(f'Time 2 Core = {t2-t1} s')

# 4 Core 
t1 = time.time()
r2 = Parallel(n_jobs=4)(delayed(math.factorial) (int(math.sqrt(i**3))) for i in range(100,1000)) 
t2 = time.time() 
print(f'Time 4 Core = {t2-t1} s')

# All Core 
t1 = time.time()
r3 = Parallel(n_jobs=-1)(delayed(math.factorial) (int(math.sqrt(i**3))) for i in range(100,1000)) 
t2 = time.time() 
print(f'Time All Core = {t2-t1} s')

# %%
def square(x):
    return x**2


t1 = time.time()
sqrt = Parallel(n_jobs=2)(delayed(square) (i) for i in range(100, 1000) )
t2 = time.time() 
print(f'Time All Core = {t2-t1} s')


#%%

#%%

#%%

#%%