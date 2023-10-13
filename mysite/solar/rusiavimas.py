import random, datetime


def rusiuoti(elektros_kainos):
    global indeksas
    print(elektros_kainos)
    indeksas = []
    for x in range(23):
        indeksas.append(0)
    for i in range(23):
        maziausia=10000.
        for j in range(23):
            if elektros_kainos[j]=='-' : elektros_kainos[j]=0.0
            if maziausia>float(elektros_kainos[j]) and indeksas[j]==0:
                laikina=j
                maziausia=elektros_kainos[j]
        indeksas[laikina]=i+1
    return indeksas

def ijungti_ikrovima(indeksas):
    global start_in
    start_in=[]
    for x in range(23):
        start_in.append('null')
    for x in range(23):
        if indeksas[x]<=5:
            start_in[x]= 'start'
    return start_in

def įjungti_iskrovima(indeksas):
    global start_out
    start_out=[]
    for x in range(23):
        start_out.append('null')
    for x in range(23):
        if indeksas[x]>=19:
            start_out[x]='start'
    return start_out

def surusiuoti( elektros_kainos):
    rusiuoti(elektros_kainos)
    ijungti_ikrovima(indeksas)
    įjungti_iskrovima(indeksas)
    for x in range(23):
        print(indeksas[x], start_in[x], start_out[x])
    return indeksas, start_in, start_out