import os
import time
time_start = time.time()
print('start time',time_start)
os.system('python DataHandle_main.py')
os.system('python BuildOutputHandle_main.py')
os.system('python APICheck_main.py')
os.system('python Find_Availability_main.py')
time_end = time.time()
print('end time',time_end)
print('time cost',time_end - time_start,'m')