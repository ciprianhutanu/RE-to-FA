def initVariables(node, var):
    t = ({node: {var: [node + 1]}}, node, [node + 1])
    return t


def star(node, var):
    global d
    oldtrans = d[var][0].copy()
    for n in d[var][2]:
        if n in oldtrans:
            if 'lambda' in oldtrans[n]:
                oldtrans[n]['lambda'].extend([node])
            else:
                oldtrans[n]['lambda'] = [node]
        else:
            oldtrans[n] = {'lambda': [node]}
    oldtrans[node] = {'lambda': [d[var][1]]}
    d[var + '*'] = (oldtrans, node, d[var][2] + [node])


def add(node, expr1, expr2):
    global d
    oldtrans = d[expr1][0].copy()
    for n in d[expr2][0]:
        for k in d[expr2][0][n]:
            if n in oldtrans:
                if k in oldtrans:
                    oldtrans[n][k].extend(d[expr2][0][n][k])
                else:
                    oldtrans[n][k] = d[expr2][0][n][k]
            else:
                oldtrans[n] = {k: d[expr2][0][n][k]}
    oldtrans[node] = {'lambda': [d[expr1][1], d[expr2][1]]}
    d[expr1 + '+' + expr2] = (oldtrans, node, d[expr1][2] + d[expr2][2])


def concat(expr1, expr2):
    global d
    oldtrans = d[expr1][0].copy()
    for n in d[expr2][0]:
        for k in d[expr2][0][n]:
            if n in oldtrans:
                if k in oldtrans:
                    oldtrans[n][k].extend(d[expr2][0][n][k])
                else:
                    oldtrans[n][k] = d[expr2][0][n][k]
            else:
                oldtrans[n] = {k: d[expr2][0][n][k]}
    for n in d[expr1][2]:
        if n in oldtrans:
            if 'lambda' in oldtrans[n]:
                oldtrans[n]['lambda'].extend([d[expr2][1]])
            else:
                oldtrans[n]['lambda'] = [d[expr2][1]]
        else:
            oldtrans[n] = {'lambda': [d[expr2][1]]}
    d[expr1 + expr2] = (oldtrans, d[expr1][1], d[expr2][2])


regex = input("Experia regulata:")
letters = list(regex)
operators = ['*', '+', '(', ')', None]
d = {}
node = 0
if not letters:
    d = {'lamda': ({}, 0, [0])}
else:
    for i in range(len(letters)):
        if letters[i] not in operators:
            letters[i] = letters[i] + str(i)
    for i in range(len(letters)):
        l = letters[i]
        if l[0] not in operators:
            d[l] = initVariables(node, l)
            node = node + 2
    while len(letters) > 1:
        while '(' in letters:
            p1 = p2 = 0
            for i in range(0, len(letters)):
                if letters[i] == '(':
                    p1 = i
                if letters[i] == ')':
                    p2 = i
                    break
            i = p1 + 1
            while i <= p2:
                l = letters[i]
                if i >= 1:
                    var = letters[i - 1]
                else:
                    var = None
                if l[0] == '*' and var not in operators:
                    star(node, var)
                    node += 1
                    letters[i - 1:i + 1] = [var + '*']
                    i -= 2
                    p2 -= 1
                i += 1
            i = p1 + 1
            while i <= p2:
                l = letters[i]
                if i >= 1:
                    var = letters[i - 1]
                else:
                    var = None
                if l[0] not in operators and var not in operators:
                    concat(var, l)
                    letters[i - 1:i + 1] = [var + l]
                    i -= 2
                    p2 -= 1
                i += 1
            i = p1 + 1
            while i <= p2:
                l = letters[i]
                if l == '+':
                    expr1 = letters[i - 1]
                    expr2 = letters[i + 1]
                    if expr1[0] not in operators and expr2[0] not in operators:
                        add(node, expr1, expr2)
                        node += 1
                        letters[i - 1:i + 2] = [expr1 + '+' + expr2]
                        i -= 2
                        p2 -= 2
                i += 1
            letters[p1:p2 + 1] = letters[p1 + 1:p2]
        else:
            i = 0
            while i < len(letters):
                l = letters[i]
                if i >= 1:
                    var = letters[i - 1]
                else:
                    var = None
                if l[0] == '*' and var not in operators:
                    star(node, var)
                    node += 1
                    letters[i - 1:i + 1] = [var + '*']
                    i -= 2
                i += 1
            i = 0
            while i < len(letters):
                expr2 = letters[i]
                if i >= 1:
                    expr1 = letters[i - 1]
                else:
                    expr1 = None
                if expr2 not in operators and expr1 not in operators:
                    concat(expr1, expr2)
                    letters[i - 1:i + 1] = [expr1 + expr2]
                    i -= 2
                i += 1
            i = 0
            while i < len(letters):
                l = letters[i]
                if l == '+':
                    expr1 = letters[i - 1]
                    expr2 = letters[i + 1]
                    if expr1[0] not in operators and expr2[0] not in operators:
                        add(node, expr1, expr2)
                        node += 1
                        letters[i - 1:i + 2] = [expr1 + '+' + expr2]
                        i -= 2
                i += 1
fform = letters[0]
print(f"Nod start: {d[fform][1]}")
print(f"Stari finale: {d[fform][2]}")
print("Legaturi:\nDin:\tCu:\tLa:\t")
for k1 in d[fform][0]:
    for val in d[fform][0][k1]:
        for k2 in d[fform][0][k1][val]:
            if val == 'lambda':
                print(f"{k1}\tλ\t{k2}")
            else:
                print(f"{k1}\t{val[0]}\t{k2}")
