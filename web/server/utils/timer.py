import time, functools

def timing(func):
    '''this function is a wrapper to measure time execution.
    '''
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        ret = func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('############function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
        return ret
    return newfunc