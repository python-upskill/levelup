# generate random integer values
from random import seed
from random import randint


def random_int(v_from, v_to):
    # seed(10)
    return randint(v_from, v_to)


# seed random number generator
# seed(10)
# generate some integers
min = 100
max = 0
for _ in range(1000):
    #     value=randint(0,10)
    #     if(max>min):
    #         print('a')

    value = randint(0, 10)
    if (value > max):
        max = value
    if (value < min):
        min = value
    print(value)
        # if (value>max):
        #     pass
        # if value<min:
        #     min=value
print('min=' + str(min) + ' max=' + str(max))
