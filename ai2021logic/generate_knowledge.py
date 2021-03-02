from field_var import field_var


def nextcar(n):
    if n < 3:
        return n + 1
    else:
        return 0


def generate_knowledge(conf):
    kb = []

    allCar = 0
    haveRight = False
    for i in range(4):
        if conf[i] != 'empty':
            allCar += 1
        if conf[i] == 'right of way':
            haveRight = True

    for i in range(4):
        if conf[i] == 'empty':
            kb.append(field_var(i, 0))
        elif conf[i] == 'right of way':
            kb.append(field_var(i, 1))
        elif conf[i] == 'stop':
            kb.append(field_var(i, allCar))
        # assign the car that no empty, no right of way and no stop, have priority between right of way and stop
        elif allCar > 0:

            between = field_var(i, 1 + haveRight)

            if allCar > 1:
                for p in range(1 + haveRight, allCar + 1):
                    between += '|' + field_var(i, p)
            kb.append(between)

        # right before left if left,AKA i no empty, no right of way and right is not stop
        if conf[i] != 'empty' and conf[i] != 'right of way' and conf[nextcar(i)] != 'stop':
            # cur current priority
            for cur in range(1, 5):
                # nxt after priority
                for nxt in range(1, 5):
                    if cur + nxt <= 4:
                        # right car have no priority after current car
                        right = field_var(i, cur) + "==> ~" + field_var(nextcar(i), cur + nxt)
                        kb.append(right)
        # a priority can be assigned to a car
        for j in range(4):
            if i != j and conf[i] != 'empty':
                for p in range(1, 5):
                    apriority = field_var(i, p) + "==> ~" + field_var(j, p)
                    kb.append(apriority)

    return kb
