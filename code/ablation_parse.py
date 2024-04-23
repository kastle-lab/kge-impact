import os
dirPath = os.path.dirname(os.path.abspath(__file__))
print(dirPath) 
input_path = "../dataset/fb15k-239"
output_path = "../dataset/ablation"
trainOrTest = "train"
iOf_write = open(os.path.join(output_path, f"iOf-{trainOrTest}.txt"), "w")
sco_write = open(os.path.join(output_path, f"sco-{trainOrTest}.txt"), "w")
iOfSco_write = open(os.path.join(output_path, f"iOfSco-{trainOrTest}.txt"), "w")

with open(os.path.join(input_path,f"{trainOrTest}.txt"),"r") as inp:
    lines = [ line.strip() for line in inp.readlines() ]

iOf_set = set()
sco_set = set()
for line in lines:
    s, p, o = line.split("\t")
    if(p == "instanceOf"):
        iOf_write.write(line+'\n')
        iOfSco_write.write(line+'\n')        
    if(p == "subclassOf"):
        print(p)
        sco_write.write(line+'\n')
        iOfSco_write.write(line+'\n')        