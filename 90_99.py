# chapter10

# 90.word2vecによる学習
import word2vec
import pickle
from collections import OrderedDict
import numpy as np
from scipy import io

def cosine_similarity(x,y):
    multi_norm_xy=np.linalg.norm(x)*np.linalg.norm(y)
    if multi_norm_xy!=0:
        return np.dot(x,y)/multi_norm_xy
    else:
        return -1

print("A90:")

# train
'''
word2vec.word2vec(train="./corpus2.txt",output="./vectors.txt",size=300,threads=4,binary=0)

with open("./vectors.txt","rt")as data:
    lines=data.readline().split(" ")
    size_dict=int(lines[0])
    size_x=int(lines[1])

    dict_index=OrderedDict()
    matrix_x=np.zeros([size_dict,size_x],dtype=np.float64)

    for i,line in enumerate(data):
        tmp=line.strip().split(" ")
        dict_index[tmp[0]]=i
        matrix_x[i]=tmp[1:]

io.savemat("word2matrix_x300",{"matrix_x300":matrix_x})
with open("./word2dict_index_t","wb")as data:
    pickle.dump(dict_index,data)

# 86
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]
print(matrix_x300[dict_index["United_States"]])
print()

# 87
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]
vec1=matrix_x300[dict_index["United_States"]]
vec2=matrix_x300[dict_index["U.S"]]
print(cosine_similarity(vec1,vec2))
print()

# 88
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]
vec_E=matrix_x300[dict_index["England"]]

cosine_list=[]
for i in range(len(dict_index)):
    cosine_list.append(cosine_similarity(vec_E,matrix_x300[i]))

cosine_index=np.argsort(cosine_list)[::-1][1:11]
keys=list(dict_index.keys())

for idx in cosine_index:
    print("{}:{}".format(keys[idx],cosine_list[idx]))
print()

# 89
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]

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
'''

# 91.アナロジーデータの準備
print("A91:")
'''
with open("./family.txt","wt")as output:
    with open("./questions-words.txt","rt")as data:
        
        section_flag=False
        for line in data:
            if section_flag:
                if line.startswith(": "):
                    print("Finish!")
                    break
                output.write(line)
            elif line.startswith(": family"):
                section_flag=True
'''

# 92.アナロジーデータへの適用
print("A92:")

'''
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

keys=list(dict_index.keys())
matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]

with open("./family_result.txt","wt")as output:
    with open("./family.txt")as data:
        for line in data:
            tmps=line.split(" ")

            try:
                col1_vec=matrix_x300[dict_index[tmps[0]]]
                col2_vec=matrix_x300[dict_index[tmps[1]]]
                col3_vec=matrix_x300[dict_index[tmps[2]]]

                mix_vec=col2_vec-col1_vec+col3_vec

                ans=""
                simi_list=[]
                simi=-1
                for i in range(len(dict_index)):
                    simi_list.append(cosine_similarity(mix_vec,matrix_x300[i]))
                simi_idx_list=np.argsort(simi_list)
                ans_index=simi_idx_list[-1]
                ans=keys[ans_index]
                simi=simi_list[ans_index]

            except KeyError:
                ans=""
                simi=-1
            
            output.write("{} {} {}\n".format(line.strip(),ans,simi))
'''

# 93.アナロジータスクの正解率の計算
print("A93:")
'''
with open("./family_result.txt","rt")as data:
    correct=0
    total=0

    for line in data:
        tmp=line.split(" ")
        total+=1
        if tmp[3]==tmp[4]:
            correct+=1

print("{}/{}={:.3f}".format(correct,total,correct/total))
'''

# 94.WordSimilarity-353での類似度計算
print("A94:")
'''
with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_x300")["matrix_x300"]

with open("./combined_out.tab","wt")as output:
    with open("./wordsim353/combined.tab","rt")as data:

        header=True
        for line in data:
            if header:
                header=False
                continue
            
            
            tmp=line.split("\t")

            try:
                simi=cosine_similarity(matrix_x300[dict_index[tmp[0]]],matrix_x300[dict_index[tmp[1]]])
            
            except KeyError:
                simi=-1
            
            output.write("{}\t{}\n".format(line.strip(),simi))
'''

# 95.WordSimilarity-353での評価
print("A95:")

with open("./combined_out.tab","rt")as data:
    human=[]
    system=[]

    N=0
    for line in data:
        tmp=line.strip().split("\t")
        human.append(float(tmp[2]))
        system.append(float(tmp[3]))
        N+=1

human_idx=np.argsort(human)
system_idx=np.argsort(system)

human_rank=[0]*N
system_rank=[0]*N

for i in range(N):
    human_rank[human_idx[i]]=i+1
    system_rank[system_idx[i]]=i+1

S=0
for i in range(N):
    S+=pow(human_rank[i]-system_rank[i],2)
speare_r=1-(6.0*S)/(pow(N,3)-N)

print("スピアマンの順位相関係数：{:.3f}".format(speare_r))

# 96.国名に関するベクトルの抽出
print("A96:")

with open("./word2dict_index_t","rb")as data:
    dict_index=pickle.load(data)

matrix_x300=io.loadmat("word2matrix_x300")["matrix_x300"]

dict_country=OrderedDict()
matrix=np.empty([0,300],dtype=np.float64)
count=0

with open("./countries.txt","rt")as data:
    for line in data:
        try:
            nation=line.strip().replace(" ","_")
            idx=dict_index[nation]
            matrix=np.vstack([matrix,matrix_x300[idx]])
            dict_country[nation]=count
            count+=1
        except:
            pass

io.savemat("./word2matrix_country",{"matrix_x300":matrix})
with open("./word2dict_country","wb")as data:
    pickle.dump(dict_country,data)

print("end")

# 97.k-meansクラスタリング
from sklearn.cluster import KMeans

print("A97:")
K=5

with open("./word2dict_country","rb")as data:
    dict_country=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_country")["matrix_x300"]
predicts=KMeans(n_clusters=K).fit_predict(matrix_x300)
results=zip(dict_country.keys(),predicts)

for country,group in sorted(results,key=lambda x:x[1]):
    print("{}:{}".format(country,group))

# 98.Ward法によるクラスタリング
from scipy.cluster.hierarchy import ward,dendrogram
from matplotlib import pyplot as plt

print("A98:")
with open("./word2dict_country","rb")as data:
    dict_country=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_country")["matrix_x300"]

ward=ward(matrix_x300)
dendrogram(ward,labels=list(dict_country.keys()),leaf_font_size=8)
plt.show()

# 99.t-SNEによる可視化
from sklearn.manifold import TSNE

print("A99:")
K=5

with open("./word2dict_country","rb")as data:
    dict_country=pickle.load(data)

matrix_x300=io.loadmat("./word2matrix_country")["matrix_x300"]

t_sne=TSNE(perplexity=30,learning_rate=500).fit_transform(matrix_x300)
predicts=KMeans(n_clusters=K).fit_predict(matrix_x300)

fig,ax=plt.subplots()
cmap=plt.get_cmap("Set1")

for idx,lb in enumerate(list(dict_country.keys())):
    cval=cmap(predicts[idx]/4)
    ax.scatter(t_sne[idx,0],t_sne[idx,1],marker=".",color=cval)
    ax.annotate(lb,xy=(t_sne[idx,0],t_sne[idx,1]),color=cval)

plt.show()
