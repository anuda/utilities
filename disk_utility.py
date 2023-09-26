import os
import pandas as pd
from pathlib import Path
import sys, getopt


root_path=sys.argv[1]
print(root_path)

available_dirs=[]
for root, dir, files in os.walk(root_path):
    for dirname in dir:
        available_dirs.append(os.path.join(root,dirname))


def get_dir_size(path):
    path_ = Path(path)
    owner = path_.owner()
    total = 0
    with os.scandir(path) as d:
        for f in d:
            if f.is_file():
                total += f.stat().st_size
            elif f.is_dir():
                total += get_dir_size(f.path)[1]
    du = (total/ (1024 * 1024))
    return(owner,du)



mem_df=pd.DataFrame(columns=['path','user','du'])

for i in available_dirs:
   (owner,du) = get_dir_size(i)

   temp = pd.DataFrame([[i,owner,du]],columns=['path','user','du'])
   mem_df = mem_df.append(temp)

mem_df = mem_df.sort_values(by='du',ascending=False)
mem_df.to_csv('mem_df.csv',index=False)


# print(mem_df.head())
