# chapter4

# 準備
"""
import MeCab

m=MeCab.Tagger("-Ochasen")
with open("neko.txt","r") as fi:
    with open("neko.txt.mecab","w") as fo:
        fo.write(m.parse(fi.read()))
"""

# 30.形態素解析結果の読み込み
import re

with open("./neko.txt.mecab","r") as fp:
    col=[]
    sent=[]
    Keys=["surface","base","pos","pos1"]
    for line in fp:
        Values=[]
        words=re.split("\t|,|\n",line)
        if words[0]=="EOS":
            if sent:
                col.append(sent)
                sent=[]
            continue
        Values.append(words[0])
        Values.append(words[7])
        Values.append(words[1])
        Values.append(words[2])
        sent.append(dict(zip(Keys,Values)))
#print("A30:")
#print(col)

# 31.動詞
verb_sur=[]
for d in col:
    for sen in d:
        if sen["pos"]=="動詞":
            verb_sur.append(sen["surface"])
#print("A31:")
#print(verb_sur)

# 32.動詞の原形
verb_base=[]
for d in col:
    for sen in d:
        if sen["pos"]=="動詞":
            verb_base.append(sen["base"])
#print("A32:")
#print(verb_base)

# 33.サ変名詞
noun_sa=[]
for d in col:
    for sen in d:
        if sen["pos"]=="名詞" and sen["pos1"]=="サ変接続" and sen["base"]!="*":
            noun_sa.append(sen["base"])
#print("A33:")
#print(noun_sa)

# 34.「AのB」
noun_of=[]
for d in col:
    for i in range(1,len(d)-1):
        if d[i]["surface"]=="の" and d[i-1]["pos"]=="名詞" and d[i+1]["pos"]=="名詞":
            noun_of.append(d[i-1]["surface"]+d[i]["surface"]+d[i+1]["surface"])
#print("A34:")
#print(noun_of)

# 35.名詞の連接
nouns=[]
tmp_noun=[]
for d in col:
    for sen in d:
        if sen["pos"]=="名詞":
            tmp_noun.append(sen["surface"])
        else:
            if len(tmp_noun)>=2:
                nouns.append("".join(tmp_noun))
            tmp_noun=[]
    if len(tmp_noun)>=2:
        nouns.append("".join(tmp_noun))
    tmp_noun=[]
#print("A35:")
#print(nouns)

# 36.単語の出現頻度
import collections

word_freq=collections.Counter()
for d in col:
    for sen in d:
        word_freq.update(sen["surface"])
#print("A36:")
#print(word_freq.most_common())

# 37.頻度上位10語
from matplotlib import pyplot as plt

data=list(word_freq.most_common(10))
X_lab=[]
Y=[]
for data_con in data:
    tmp=list(data_con)
    X_lab.append(tmp[0])
    Y.append(tmp[1])
#フォントを指定すると文字化け解消
#plt.bar(left=range(10),height=Y,tick_label=X_lab,align="center")
#plt.show()

# 38.ヒストグラム
counts=list(zip(*word_freq.most_common()))[1]
'''
plt.xlabel("word-frequency")
plt.ylabel("word-kinds")
plt.hist(counts,bins=20,range=(1,20),normed=True)
plt.xlim(xmin=1, xmax=20)
plt.grid(axis="y")
plt.show()
'''

# 39.Zipfの法則
'''
plt.scatter(range(1,len(counts)+1),counts)
plt.xlim(1,len(counts)+1)
plt.ylim(1,counts[0])
plt.xscale("log")
plt.yscale("log")
plt.grid(axis="both")
plt.show()
'''