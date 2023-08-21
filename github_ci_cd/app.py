from dotenv import dotenv_values

config = dotenv_values(".env")
print(config)

DEBUG = config['DEBUG']
print('DEBUG', DEBUG)

print('Hello, world!')
print('Hi')

print(2 + 2)
print(2 - 2)
print(2 ** 2)
print(2 // 2)
