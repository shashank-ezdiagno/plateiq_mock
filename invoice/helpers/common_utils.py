import random

class CommonUtils:
    @staticmethod
    def generate_random_id():
        return ''.join(random.choice('0123456789ABCDEF') for i in range(6))

    @staticmethod
    def generate_random_int(a,b):
        return random.randint(a,b)


    @staticmethod
    def generate_random_float(a,b):
        return random.random()


