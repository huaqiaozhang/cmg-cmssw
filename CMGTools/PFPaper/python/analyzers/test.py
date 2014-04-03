import operator
sc = sorted( clusters, key=lambda x: x.energy(), reverse=True)
for c in sc: print c
