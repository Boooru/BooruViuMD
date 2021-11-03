from time import time


class CallController:

    def __init__(self, max_call_interval):
        self._max_call_interval = max_call_interval
        self._last_call = time()

    def __call__(self, function):
        def wrapped(*args, **kwargs):
            now = time()

            if now - self._last_call > self._max_call_interval:
                self._last_call = now

                function(*args, **kwargs)

        return wrapped


class Wrap:
    __func: callable = None
    __a = None
    __b = None

    def __init__(self, func, a, b):
        self.__func = func
        self.__a = a
        self.__b = b

        print("Building wrap: " + str(func))

    def get(self):
        return self.__func(self.__a, self.__b)
