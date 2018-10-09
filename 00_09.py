# chapter1

# 00.文字列の逆順
string0="stressed"
print("A0:{}".format(string0[::-1]))

# 01.「パタトクカシーー」
string1="パタトクカシーー"
print("A1:{}".format((string1[1::2])))

# 02.「パトカー」+「タクシー」＝「パタトクカシーー」
string2_1="パトカー"
string2_2="タクシー"
print("A2:{}".format("".join([(sub1+sub2) for sub1,sub2 in zip(string2_1,string2_2)])))

# 03.円周率
string3="Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
string3=string3.replace(",","")
string3=string3.replace(".","")
print("A3:{}".format([len(word) for word in string3.split(" ")]))

# 04.元素記号
string4="Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
str4=string4.split(" ")
one=[0,4,5,6,7,8,14,15,18]
key4=[]
value4=[]
for i,word in enumerate(str4):
    if i in one:
        key4.append(word[0])
        value4.append(str4.index(word))
    else:
        key4.append(word[0:2])
        value4.append(str4.index(word))
print("A4:{}".format(dict(zip(key4,value4))))

# 05.n-gram
def create_bigram(seq):
    return [tuple(seq[idx:idx+2]) for idx in range(len(seq)-1)]

string5="I am an NLPer"
print("A5_1:{}".format(create_bigram(string5)))
print("A5_2:{}".format(create_bigram([word for word in string5.split(" ")])))

# 06.集合
string6_1="paraparaparadise"
string6_2="paragraph"
X=set(create_bigram(string6_1))
Y=set(create_bigram(string6_2))
print("A6_1:X|Y={},X&Y={},X-Y={}".format(X|Y,X&Y,X-Y))
print("A6_2: se in X={}, se in Y={}".format(("s","e")in X,("s","e")in Y))

# 07.テンプレートによる文生成
def create_template_sent(x,y,z):
    return "{}時の{}は{}".format(x,y,z)
print("A7:{}".format(create_template_sent(x=12,y="気温",z=22.4)))

# 08.暗号文
def cipher(sent):
    return ''.join(chr(219-ord(w)) if w.islower() else w for w in sent)

string8="Hello, world!"
print("A8:入力：{},暗号化：{},復号化：{}".format(string8,cipher(string8),cipher(cipher(string8))))

# 09.Typoglycemia
def Typoglycemia(sent):
    import random
    words=sent.split(" ")
    result=[]
    for w in words:
        if len(w)<=4:
            result.append(w)
        else:
            random_w=list(w[1:-1])
            random.shuffle(random_w)
            result.append(w[0]+"".join(random_w)+w[-1])
    return " ".join(result)

string9="I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print("A9:{}".format(Typoglycemia(string9)))

