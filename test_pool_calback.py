import multiprocessing
import time

def callback(x):
    print('callback {}'.format(x))

def func(x):
    print('func {}'.format(x))
    return x

pool = multiprocessing.Pool()

args = range(20)

for a in args:
    pool.apply_async(func, (a,), callback=callback)

print('sleep')

t0 = time.time()
while time.time() - t0 < 60:
    pass

print('Finished with the script')