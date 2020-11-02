import random, string

poolOfChars  = string.ascii_letters + string.digits
random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])
print (random_codes(poolOfChars, 15))
