# chapter9

# 80.コーパスの整形
import bz2

print("A80:")

'''
with open("./corpus.txt","wt")as output:
    with bz2.open("./enwiki-20150112-400-r100-10576.txt.bz2","rt")as read_file:
        for line in read_file:
            tokens=[]
            for t in line.split(" "):
                token=t.strip().strip('.,!?;:()[]\'"')
                if len(token)>0:
                    tokens.append(token)
            print(*tokens, sep=' ', end='\n', file=output)
'''

print("end")

# 81.複合語からなる国名への対処
print("A81:")

'''
set_country=set()
dict_country={}
with open("./countries.txt","r")as country_file:
    for line in country_file:
        words=line.split(" ")
        if len(words)>1:
            set_country.add(line.strip())

            if words[0] in dict_country:
                lengths=dict_country[words[0]]
                if not len(words) in lengths:
                    lengths.append(len(words))
                    lengths.sort(reverse=True)
            else:
                dict_country[words[0]]=[len(words)]

with open("./corpus2.txt","wt")as output:
    with open("./corpus.txt","rt")as corpus:
        for line in corpus:
            tokens=line.strip().split(" ")
            result=[]
            skip=0

            for i in range(len(tokens)):
                if skip>0:
                    skip-=1
                    continue
                
                if tokens[i] in dict_country:
                    hit=False
                    for length in dict_country[tokens[i]]:
                        if " ".join(tokens[i:i+length]) in set_country:
                            result.append("_".join(tokens[i:i+length]))
                            skip=length-1
                            hit=True
                            break
                    if hit:
                        continue
                result.append(tokens[i])
            print(*result, sep=' ', end='\n', file=output)

'''
print("end")

# 82.文脈の抽出
import random

print("A82:")

'''
with open("corpus2.txt", "r") as f:
  corpus = f.readlines()

with open("context.txt", "w") as outpur:
  for line in corpus:
    line = line.replace("\n", "")
    tokens = line.split(" ")
    for i, token in enumerate(tokens):
      num = random.randint(1, 5)
      context = tokens[max([i-num, 0]) : min([i+num+1, len(tokens)])]
      for c in context:
        if c != token and token != "" and c != "":
          output.write(token + "\t" + c + "\n")
'''
print("end")                        

# 83.単語/文脈の頻度の計測
from collections import Counter
import pickle

print("A83:")

'''
counter_tc = Counter()
counter_t = Counter()
counter_c = Counter()

line_tc = []
line_t = []
line_c = []
with open("./context.txt", 'rt') as data:
    for i, line in enumerate(data, start=1):

        line = line.strip()
        tokens = line.split('\t')

        line_tc.append(line)
        line_t.append(tokens[0])
        line_c.append(tokens[1])

        if i % 1000000 == 0:
            counter_tc.update(line_tc)
            counter_t.update(line_t)
            counter_c.update(line_c)
            line_tc = []
            line_t = []
            line_c = []
            print('{} done.'.format(i))

counter_tc.update(line_tc)
counter_t.update(line_t)
counter_c.update(line_c)


with open("./count_tc", 'wb') as data:
    pickle.dump(counter_tc, data)
with open("./count_t", 'wb') as data:
    pickle.dump(counter_t, data)
with open("./count_c", 'wb') as data:
    pickle.dump(counter_c, data)

print('N={}'.format(i))
'''

print("end")

# 84.単語文脈行列の作成
import math
from collections import OrderedDict
from scipy import sparse,io

print("A84:")
'''
with open("./count_tc","rb")as data:
    count_tc=pickle.load(data)
with open("./count_t","rb")as data:
    count_t=pickle.load(data)
with open("./count_c","rb")as data:
    count_c=pickle.load(data)

dict_index_t=OrderedDict((key,i)for i,key in enumerate(count_t.keys()))
dict_index_c=OrderedDict((key,i)for i,key in enumerate(count_c.keys()))

t_size=len(dict_index_t)
c_size=len(dict_index_c)
matrix_x=sparse.lil_matrix((t_size,c_size))
N=67659739

for k,f_tc in count_tc.items():
    if f_tc>10:
        tokens=k.split("\t")
        t=tokens[0]
        c=tokens[1]
        ppmi=max([math.log((N*f_tc)/(count_t[t]*count_c[c]))])
        matrix_x[dict_index_t[t], dict_index_c[c]] = ppmi

io.savemat("matrix_x",{"matrix_x":matrix_x})
with open("./dict_index_t","wb")as data:
     pickle.dump(dict_index_t,data)   
'''
print("end")

# 85.主成分分析による次元圧縮
import sklearn.decomposition

print("A85:")
'''
matrix_x=io.loadmat("matrix_x")["matrix_x"]

clf=sklearn.decomposition.TruncatedSVD(300)
matrix_x300=clf.fit_transform(matrix_x)
io.savemat("matrix_x300",{"matrix_x300":matrix_x300})
'''

print("end")

# 86.単語ベクトルの表示
import numpy as np

print("A86:")
'''
with open("./dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./matrix_x300")["matrix_x300"]
print(matrix_x300[dict_index["United_States"]])
'''

# 87.単語の類似度
print("A87:")

def cosine_similarity(x,y):
    multi_norm_xy=np.linalg.norm(x)*np.linalg.norm(y)
    if multi_norm_xy!=0:
        return np.dot(x,y)/multi_norm_xy
    else:
        return -1

with open("./dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./matrix_x300")["matrix_x300"]
vec1=matrix_x300[dict_index["United_States"]]
vec2=matrix_x300[dict_index["U.S"]]
print(cosine_similarity(vec1,vec2))

# 88.類似度の高い単語10件
print("A88:")

with open("./dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./matrix_x300")["matrix_x300"]
vec_E=matrix_x300[dict_index["England"]]

cosine_list=[]
for i in range(len(dict_index)):
    cosine_list.append(cosine_similarity(vec_E,matrix_x300[i]))

cosine_index=np.argsort(cosine_list)[::-1][1:11]
keys=list(dict_index.keys())

for idx in cosine_index:
    print("{}:{}".format(keys[idx],cosine_list[idx]))

# 89.加法構成性によるアナロジー
print("A89:")

with open("./dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./matrix_x300")["matrix_x300"]

vec_S=matrix_x300[dict_index["Spain"]]
vec_M=matrix_x300[dict_index["Madrid"]]
vec_A=matrix_x300[dict_index["Athens"]]

mix_vec=vec_S-vec_M+vec_A

cosine_list=[]
for i in range(len(dict_index)):
    cosine_list.append(cosine_similarity(mix_vec,matrix_x300[i]))

cosine_index=np.argsort(cosine_list)[::-1][1:11]
keys=list(dict_index.keys())

for idx in cosine_index:
    print("{}:{}".format(keys[idx],cosine_list[idx]))

