def pushDominoes(dominoes):
    p = 0
    q = 0
    l = len(dominoes)
    while p <= l - 1:
        if dominoes[p] == '.':
            p = p + 1
        elif dominoes[p] == 'L':
            q = p
            flag = 1
            while q > 0 and flag:
                if dominoes[q] == 'R':
                    dominoes[q:(p + q) / 2 - 1] = 'R'
                    dominoes[(p + q) / 2 + 1:p] = 'L'
                    flag = 0
                else:
                    q = q - 1
            if q == 0:
                dominoes[:p] = 'L'
        elif dominoes[p] == 'R':
            q = p
            flag = 1
            while q < l - 1 and flag:
                if dominoes[q] == 'L':
                    dominoes[p:(p + q) / 2 - 1] = 'R'
                    dominoes[(p + q) / 2 + 1:q] = 'L'
                    flag = 0
                else:
                    q = q + 1
            # if q==l-1:
            #     dominoes[p:q]='R'
    return dominoes


print(pushDominoes(".L.R...LR..L.."))