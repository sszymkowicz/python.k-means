__author__ = 'Slawek'

import matplotlib.pyplot as plt
import random as rand
import functools as fnc
import numpy

dist = lambda p1, p2: ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5

minT = []
with open("199607daily.txt", "r") as f:
    for i in f.readlines()[1:]:
        try:
            minT.append(float(i.split(',')[3]))
        except ValueError:
            pass
    f.close()

points = [(i, minT[i]) for i in range(len(minT))]

print("\n*** K-Means ***")
while True:
    try:
        clusters = int(input("Number of clusters: "))
    except ValueError:
        print("\nInput has to be an integer!\nTry Again...")
        continue
    else:
        break

c = [(rand.uniform(0, len(minT)), rand.uniform(min(minT), max(minT))) for _ in range(clusters)]
old_c = [(rand.uniform(0, len(minT)), rand.uniform(min(minT), max(minT))) for _ in range(clusters)]
c_moved = [[] for _ in range(clusters)]
c_affiliation = [[] for _ in range(clusters)]

while True:
    for p in points:
        tmp_c = 0
        for i in range(len(c)):
            if dist(p, c[i]) < dist(p, c[tmp_c]):
                tmp_c = i
        c_affiliation[tmp_c].append(p)

    for i in range(len(c)):
        c[i] = (fnc.reduce(lambda x, y: x + y, [j[0] for j in c_affiliation[i]]) / len(c_affiliation[i]),
                fnc.reduce(lambda x, y: x + y, [j[1] for j in c_affiliation[i]]) / len(c_affiliation[i]))

    error = max(minT) * 0.01
    flag = False
    for i in range(len(c)):
        if not (abs(c[i][0] - old_c[i][0]) < error * (len(minT)*0.1) and abs(c[i][1] - old_c[i][1]) < error):
            flag = True

    if flag:
        for i in range(len(old_c)):
            c_moved[i].append(old_c[i])
        old_c = numpy.copy(c)
        c_affiliation.clear()
        c_affiliation = [[] for _ in range(clusters)]
    else:
        break

for i in range(clusters):
    plt.scatter(*zip(*c_affiliation[i]), marker='x', c=numpy.random.rand(3, 1))
for i in range(len(c_moved)-1):
    plt.scatter(*zip(*c_moved[i]), marker='o', c='red', s=40)
plt.scatter(*zip(*c), marker='o', c='red', s=75)
plt.show()