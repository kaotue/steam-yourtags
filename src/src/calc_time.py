import time

def calc_time(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        stop = time.time()
        print(f'[{fn.__name__}] elapsed time: {round(stop - start, 8)}')
        return ret
    return wrapper