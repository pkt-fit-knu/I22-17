def Iris(a,b,c,d):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    if (d<1):
        return "Iris-setosa"
    elif (a>6.5):
        return "Iris-virginica"
    else:
        return "Iris-versicolor"

def CheckIris():
    f = open('iris.data', 'r')
    for line in f:
        val = line.split(',')
        if len(val)>3:
            print(Iris(val[0],val[1],val[2],val[3]))

CheckIris()
