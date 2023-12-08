testFile = open("test.txt","r")

head = open("head.txt", "w")
tail = open("tail.txt", "w")
rel = open("rel.txt", "w")

lines = [ line.strip() for line in testFile.readlines() ]

s_set = set()
p_set = set()
o_set = set()
for line in lines:
    s, p, o = line.split("\t")
    s_set.add(s)
    p_set.add(p)
    o_set.add(o)


for s in s_set:
    head.write(f"{s}\n")
for p in p_set:
    rel.write(f"{p}\n")
for o in o_set:   
    tail.write(f"{o}\n")

