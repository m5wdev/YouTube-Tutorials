'''
X
X=F[-X][+X]

1
F[-X][+X]

2
F[-F[-X][+X]][+F[-X][+X]]

3
F[-F[-F[-X][+X]][+F[-X][+X]]][+F[-F[-X][+X]][+F[-X][+X]]]

4
F[-F[-F[-F[-X][+X]][+F[-X][+X]]][+F[-F[-X][+X]][+F[-X][+X]]]][+F[-F[-F[-X][+X]][+F[-X][+X]]][+F[-F[-X][+X]][+F[-X][+X]]]]
'''

def generate_l_system(axiom: str, rules: dict, iterations: int):
    l_system = axiom
    for _ in range(iterations):
        new_rules = ''
        for char in l_system:
            new_rules += rules.get(char, char)
        l_system = new_rules
    return l_system


# ls = {
#     # 'axiom': 'X',
#     # 'rules': {'X': 'F[-X][+X]'},
#     'axiom': 'X',
#     'rules': {'F': 'FF', 'X': 'F-[[X]+X]+F[+FX]-X'},
# }

# print(generate_l_system(ls['axiom'], ls['rules'], 5))
