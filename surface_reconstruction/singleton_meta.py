from threading import Lock


class SingletonMeta(type):
    _instances = {}

    _lock = Lock()

    def __call__(cls, *args, **kwargs):

        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = {}

            instance: type = super().__call__(cls, *args, **kwargs)

            if instance not in cls._instances[cls]:
                if 'method_type' in kwargs:
                    del kwargs['method_type']

                cls._instances[cls][instance] = instance(**kwargs)

            return cls._instances[cls][instance]
