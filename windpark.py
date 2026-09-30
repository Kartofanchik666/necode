p = []
with open("data.txt", encoding="utf-8-sig") as f:
    for s in f:
        row = [int(i) for i in s.split()]
        if len(row) > 0:
            p.append(row)

a = 12
b = 8
c = 4
money = 60

spend_all = True


def checker(MAS):
    uniq = list(set(MAS))
    if -10 in uniq:
        return False, None

    if len(MAS) == 1:
        return True, MAS[0] + 1

    if len(uniq) == 1:
        return True, uniq[0]

    if len(uniq) == 2 and abs(uniq[0] - uniq[1]) == 1:
        if MAS.count(uniq[0]) == 1 or MAS.count(uniq[1]) == 1:
            if MAS.count(uniq[0]) > MAS.count(uniq[1]):
                return True, uniq[0]
            else:
                return True, uniq[1]

    return False, None


def wind(height):
    if height <= 30:
        return 4
    if height <= 60:
        return 5
    if height <= 90:
        return 6
    if height <= 120:
        return 7
    if height <= 150:
        return 8
    return 9


power_table = [
    [200, 120, 50],
    [400, 240, 100],
    [700, 400, 160],
    [1000, 560, 220],
    [1300, 720, 280],
    [1600, 880, 340]
]


def find_places(size, mast, model_number):
    places = []
    for i in range(len(p) - size + 1):
        for j in range(len(p[0]) - size + 1):
            MAS = []
            for x in range(i, i + size):
                for y in range(j, j + size):
                    MAS.append(p[x][y])

            ok, height = checker(MAS)
            if ok:
                speed = wind(height * 10 + mast)
                power = power_table[speed - 4][model_number]
                places.append([power, i, j, height])

    places.sort(reverse=True)
    return places


A = find_places(3, 100, 0)
B = find_places(2, 70, 1)
C = find_places(1, 50, 2)

used = []
for row in p:
    used.append([False] * len(row))


def is_free(place, size):
    i = place[1]
    j = place[2]
    for x in range(i, i + size):
        for y in range(j, j + size):
            if used[x][y]:
                return False
    return True


def mark(place, size, value):
    i = place[1]
    j = place[2]
    for x in range(i, i + size):
        for y in range(j, j + size):
            used[x][y] = value


def upper_power(places, size, count, start):
    total = 0
    if count == 0:
        return 0
    for k in range(start, len(places)):
        if is_free(places[k], size):
            total += places[k][0]
            count -= 1
            if count == 0:
                return total
    return -1


best_power = -1
best_places = []
selected = []


def search(na, nb, nc, start, total):
    global best_power, best_places

    start_a = 0
    start_b = 0
    if na > 0:
        start_a = start
    else:
        start_b = start

    pa = upper_power(A, 3, na, start_a)
    pb = upper_power(B, 2, nb, start_b)
    pc = upper_power(C, 1, nc, 0)
    if pa == -1 or pb == -1 or pc == -1:
        return
    if total + pa + pb + pc <= best_power:
        return

    if na == 0 and nb == 0:
        result = selected[:]
        for place in C:
            if nc == 0:
                break
            if is_free(place, 1):
                result.append(["C", place])
                nc -= 1
        best_power = total + pc
        best_places = result
        return

    if na > 0:
        places = A
        size = 3
        model = "A"
    else:
        places = B
        size = 2
        model = "B"

    for k in range(start, len(places)):
        place = places[k]
        if is_free(place, size):
            mark(place, size, True)
            selected.append([model, place])

            if na > 0:
                next_start = k + 1
                if na == 1:
                    next_start = 0
                search(na - 1, nb, nc, next_start, total + place[0])
            else:
                search(na, nb - 1, nc, k + 1, total + place[0])

            selected.pop()
            mark(place, size, False)


print("Подходящие места: A =", len(A), "B =", len(B), "C =", len(C))
print("Перебор...")

for na in range(money // a, -1, -1):
    for nb in range(money // b, -1, -1):
        for nc in range(money // c, -1, -1):
            cost = na * a + nb * b + nc * c
            if cost > money:
                continue
            if spend_all and cost != money:
                continue
            search(na, nb, nc, 0, 0)


if best_power == -1:
    print("Подходящей расстановки нет.")
    print("Для поиска с меньшими затратами: spend_all = False")
else:
    letters = "ABCDEFGHIJKLMNO"
    counts = [0, 0, 0]
    total_cost = 0
    scheme = []
    for row in p:
        line = []
        for height in row:
            if height == -10:
                line.append("#")
            else:
                line.append(".")
        scheme.append(line)

    print("\nРезультат:")
    for model, place in best_places:
        if model == "A":
            size, mast, price, number = 3, 100, a, 0
        elif model == "B":
            size, mast, price, number = 2, 70, b, 1
        else:
            size, mast, price, number = 1, 50, c, 2

        power, i, j, height = place
        counts[number] += 1
        total_cost += price
        top = height * 10 + mast
        print(model, letters[j] + str(i + 1),
              "| высота площадки:", height * 10, "м | верхушка:", top,
              "м | ветер:", wind(top), "м/с | мощность:", power,
              "кВт | цена:", price, "млн")

        changed = False
        for x in range(i, i + size):
            for y in range(j, j + size):
                scheme[x][y] = model
                if p[x][y] != height:
                    changed = True
                    scheme[x][y] = model.lower()
                    print("  Изменить клетку:", letters[y] + str(x + 1),
                          "с", p[x][y] * 10, "до", height * 10, "м")
        if not changed:
            print("  Высоту менять не нужно")

    print("\nВетряки: A =", counts[0], "B =", counts[1], "C =", counts[2])
    print("Стоимость:", total_cost, "млн рублей")
    print("Общая мощность:", best_power, "кВт")
    print("\nКарта: # - нельзя строить, . - свободно, a/b/c - изменена высота.")
    print("   " + " ".join(letters[:len(p[0])]))
    for i in range(len(scheme)):
        print(str(i + 1).rjust(2), " ".join(scheme[i]))
