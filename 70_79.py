# chapter8

# 70.データの入手・整形
import random

print("A70:")
with open("./sentiment.txt","w") as fw:
    sent_list=[]
    with open("./rt-polaritydata/rt-polarity.pos","r")as pos:
        for line in pos:
            sent_list.append("+1 "+line)
    with open("./rt-polaritydata/rt-polarity.neg","r")as neg:
        for line in neg:
            sent_list.append("-1 "+line)
    random.shuffle(sent_list)
    
    for line in sent_list:
        fw.write(line)
print("Finished Writing!")

# 71.ストップワード
print("A71:")

from nltk.corpus import stopwords

stopwords_list=[s for s in stopwords.words("english")]

def is_stopword(string):
    if string in stopwords_list:
        return True
    else:
        return False

# 72.素性抽出
import snowballstemmer
from collections import Counter

print("A72:")

stemmer=snowballstemmer.stemmer("english")
word_counter=Counter()

with open("./sentiment.txt","r")as sent_file:
    for line in sent_file:
        for word in line[3:].split(" "):
            word=word.strip()

            if is_stopword(word):
                continue
            word=stemmer.stemWord(word)
            if word!="!" and word!="?" and len(word)<=1:
                continue
            
            word_counter.update([word])

features=[word for word, count in word_counter.items() if count>=6]

with open("./features.txt","w")as output:
    for line in features:
        output.write(line+"\n")


# 73.学習
import numpy as np

print("A73:")

def sigmoid(data_x,theta):
    return 1.0/(1.0+np.exp(-data_x.dot(theta)))

def cost(data_x, theta, data_y):
    m = data_y.size
    h = sigmoid(data_x, theta)
    j = 1 / m * np.sum(-data_y * np.log(h) -(np.ones(m) - data_y) * np.log(np.ones(m) - h))
    return j

def gradient(data_x, theta, data_y):
	'''最急降下における勾配の算出
	戻り値：
	thetaに対する勾配の行列
	'''
	m = data_y.size
	h = sigmoid(data_x, theta)
	grad = 1 / m * (h - data_y).dot(data_x)

	return grad

def extract_features(data,dict_features):
    data_one_x=np.zeros(len(dict_features)+1,dtype=np.float64)
    data_one_x[0]=1

    for word in data.split(" "):
        word=word.strip()
        if is_stopword(word):
            continue
        word=stemmer.stemWord(word)
        try:
            data_one_x[dict_features[word]]=1
        except:
            pass
    return data_one_x

def load_dict_features(filename):
    with open(filename,"r")as input_file:
        return {line.strip():i for i,line in enumerate(input_file.readlines(),start=1)}

def create_train_data(filename,dict_features):
    with open(filename,"r")as true_file:
        true_list=true_file.readlines()
        data_x=np.zeros([len(true_list),len(dict_features)+1],dtype=np.float64)
        data_y=np.zeros(len(true_list),dtype=np.float64)
        for i,line in enumerate(true_list):
            data_x[i]=extract_features(line[3:],dict_features)
            if line[0:2]=="+1":
                data_y[i]=1
        return data_x,data_y

def LG_train(data_x,data_y,alpha,count):
    theta = np.zeros(data_x.shape[1])
    c = cost(data_x, theta, data_y)
    print('\t学習開始\tcost：{}'.format(c))
    for i in range(1, count + 1):
        grad = gradient(data_x, theta, data_y)
        theta -= alpha * grad
        if i % 100 == 0:
            c = cost(data_x, theta, data_y)
            e = np.max(np.absolute(alpha * grad))
            print('\t#{}\tcost：{}\tE:{}'.format(i, c, e))
    c = cost(data_x, theta, data_y)
    e = np.max(np.absolute(alpha * grad))
    print('\t#{} \tcost：{}\tE:{}'.format(i, c, e))
    return theta


dict_features=load_dict_features("./features.txt")
#data_x,data_y=create_train_data("./sentiment.txt",dict_features)
#theta=LG_train(data_x,data_y,alpha=6.0,count=1000)
#np.save("theta.npy",theta)

# 74.予測
print("A74:")

theta=np.load("./theta.npy")
review=input("Review:")
data_one_x=extract_features(review,dict_features)
print(data_one_x)
h=sigmoid(data_one_x,theta)
if h>0.5:
    print("+1:{:.3f}".format(h))
else:
    print("-1:{:.3f}".format(1-h))

# 75.素性の重み
print("A75:")

with open("./features.txt","r")as input_file:
    features=input_file.readlines()

theta=np.load("./theta.npy")
index_sorted=np.argsort(theta)
print("==top10==")
for idx in index_sorted[:-11:-1]:
    if idx>0:
        print("{}\t{}".format(theta[idx],features[idx-1].strip()))
    else:
        print("None")

print("==worst10==")
for idx in index_sorted[0:10:]:
    if idx>0:
        print("{}\t{}".format(theta[idx],features[idx-1].strip()))
    else:
        print("None")

# 76.ラベル付け
print("A76:")

dict_features=load_dict_features("./features.txt")
theta=np.load("./theta.npy")
with open("./sentiment.txt","r")as read_file:
    with open("./result.txt","w")as output:
        for line in read_file:
            data_one_x=extract_features(line[3:],dict_features)
            h=sigmoid(data_one_x,theta)
            if h>0.5:
                output.write("{}\t{}\t{}\n".format(line[0:2],"+1",h))
            else:
                output.write("{}\t{}\t{}\n".format(line[0:2],"-1",h))

# 77.正解率の計測
print("A77:")

def calc_score(filename):
    TP=0
    FP=0
    FN=0
    TN=0

    with open(filename,"r")as result_file:
        for line in result_file:
            tar=line.split("\t")

            if len(tar)<3:
                continue
            
            if tar[0]=="+1":
                if tar[1]=="+1":
                    TP+=1
                else:
                    FN+=1
            else:
                if tar[1]=="+1":
                    FP+=1
                else:
                    TN+=1
        
        acc=(TP+TN)/(TP+FP+FN+TN)
        pre=TP/(TP+FP)
        recall=TP/(TP+FN)
        F=(2*recall*pre)/(recall+pre)

        return acc,pre,recall,F

acc,pre,recall,F=calc_score("./result.txt")
print("正解率:{:.3f}\t適合率:{:.3f}\t再現率:{:.3f}\tF:{:.3f}".format(acc,pre,recall,F))

# 78.5分割交差検定
print("A78:")

dict_features=load_dict_features("./features.txt")

with open("./sentiment.txt","r")as read_file:
    data=read_file.readlines()

sents=[]
unit=int(len(data)/5)
for i in range(5):
    sents.append(data[i*unit:(i+1)*unit])

with open("./cross_result.txt","w")as cross_result:
    for i in range(5):
        print(i+1)

        train_data=[]
        for j in range(5):
            if i==j:
                val_data=sents[j]
            else:
                train_data+=sents[j]
        
        data_x=np.zeros([len(train_data),len(dict_features)+1],dtype=np.float64)
        data_y=np.zeros(len(train_data),dtype=np.float64)
        for i,line in enumerate(train_data):
            data_x[i]=extract_features(line[3:],dict_features)
            if line[0:2]=="+1":
                data_y[i]=1

        theta=LG_train(data_x,data_y,alpha=6.0,count=1000)

        for line in val_data:
            data_one_x=extract_features(line[3:],dict_features)
            h=sigmoid(data_one_x,theta)
            if h>0.5:
                cross_result.write('{}\t{}\t{}\n'.format(line[0:2], '+1', h))
            else:
                cross_result.write('{}\t{}\t{}\n'.format(line[0:2], '-1', 1-h))

acc,pre,recall,F=calc_score("./cross_result.txt")
print("正解率:{:.3f}\t適合率:{:.3f}\t再現率:{:.3f}\tF:{:.3f}".format(acc,pre,recall,F))

# 79.適合率ー再現率グラフの描画
import matplotlib.pyplot as plt

print("A79:")

results=[]
with open("./result.txt","r")as input_file:
    for line in input_file:
        data=line.split("\t")

        lb=data[0]
        if data[1]=="-1":
            p=1.0-float(data[2])
        else:
            p=float(data[2])
        results.append((lb,p))

thresholds=[]
acc=[]
pre=[]
recall=[]
F=[]

for t in np.arange(0.02,1.0,0.02):
    with open("./tmp.txt","w")as tmp_result:
        for lb,p in results:
            if p>t:
                tmp_result.write("{}\t{}\t{}\n".format(lb,"+1",p))
            else:
                tmp_result.write("{}\t{}\t{}\n".format(lb,"-1",1-p))
    a,p,r,f=calc_score("./tmp.txt")
    thresholds.append(t)
    acc.append(a)
    pre.append(p)
    recall.append(r)
    F.append(f)

plt.plot(thresholds, acc, color='green', linestyle='--', label='accuracy')
plt.plot(thresholds, pre, color='red', linewidth=3, label='precision')
plt.plot(thresholds, recall, color='blue', linewidth=3, label='recall')
plt.plot(thresholds, F, color='magenta', linestyle='--', label='F')

plt.xlim(xmin=0,xmax=1.0)
plt.ylim(ymin=0,ymax=1.0)

plt.xlabel("threshold")
plt.ylabel("score")

plt.grid(axis="both")

plt.show()
