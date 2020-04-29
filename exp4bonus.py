'''
子句集消解实验
'''
'''
->:>
析取：%
合取：^
全称：@
存在：#
'''
dict = {}
symbol = 0
# 1.消去>蕴涵项 a>b变为~a%b
def del_inlclue(orign):

    ind = 0
    flag=0
    orignStack=[]
    right_bracket = 0
    while (ind < len(orign)):
        orignStack.append(orign[ind])
        if ((ind+1<len(orign)) and (orign[ind+1]=='>')):
            flag=1
            if orign[ind].isalpha():#是字母
                orignStack.pop()
                orignStack.append('~')
                orignStack.append(orign[ind])
                orignStack.append('%')
                ind=ind+1
            if orign[ind]==')':
                right_bracket=right_bracket+1
                tempStack = []
                while(right_bracket!=-1):
                    tempStack.append(orignStack[-1])
                    if orignStack[-1]=='(':
                        right_bracket=right_bracket-1
                    orignStack.pop()
                right_bracket = right_bracket + 1
                tempStack.pop()#去掉'('
                orignStack.append('(~')
                tempStack.reverse()
                for i in tempStack:
                    orignStack.append(i)
                orignStack.append('%')
                ind=ind+1
        ind=ind+1
    if flag==1:
        a=''
        for i in orignStack:
            a=a+i
        return a
    else:
        return orign


#2.处理否定连接词
def dec_neg_rand(orign):

    #处理~(@x)p(x) 变为(#x)~p(x)#####################################
    ind = 0
    flag = 0
    orignStack = []
    left_bracket = 0
    while (ind < len(orign)):
        orignStack.append(orign[ind])
        if orign[ind]=='~':
            if orign[ind+1]=='(':
                if orign[ind+2]=='@' or orign[ind+2]=='#':
                    flag=1
                    ind=ind+1
                    orignStack.pop()#去掉前面的~
                    orignStack.append(orign[ind])
                    if orign[ind+1]=='@':
                        orignStack.append('#')
                    else:
                        orignStack.append('@')
                    orignStack.append(orign[ind+2])#'x'
                    orignStack.append(orign[ind+3])#')'
                    orignStack.append('~')
                    ind=ind+3
        ind=ind+1
    if flag==1:
        a=''
        for i in orignStack:
            a=a+i
        orign2=a
    else:
        orign2=orign
    #print('orign2',orign2)


    # 处理~(p%q) 变为~p^~q#####################################
    ind = 0
    flag = 0
    orignStack = []
    left_bracket = 0
    while (ind < len(orign2)):
        orignStack.append(orign2[ind])
        if orign2[ind] == '~':
            if orign2[ind + 1] == '(':
                orignStack.pop()

                ind=ind+2#此时为p
                left_bracket=left_bracket+1
                orignStack.append('(~')
                while left_bracket>=1:
                    orignStack.append(orign2[ind])
                    if orign2[ind]=='(':
                        left_bracket=left_bracket+1
                    if orign2[ind]==')':
                        left_bracket=left_bracket-1
                    if left_bracket==1 and orign2[ind+1]=='%' and orign2[ind+2]!='@' and orign2[ind+2]!='#':
                        flag=1
                        orignStack.append('^~')
                        ind=ind+1
                    if left_bracket == 1 and orign2[ind + 1] == '^' and orign2[ind + 2] != '@' and orign2[ind + 2] != '#':
                        flag = 1
                        orignStack.append('%~')
                        ind = ind + 1
                    ind=ind+1
        ind=ind+1
    if flag==1:
        a=''
        for i in orignStack:
            a=a+i
        orign3=a
    else:
        orign3=orign2
    #print('orign3',orign3)


    # 处理~~p 变为p#####################################
    ind = 0
    flag = 0
    bflag = 0
    orignStack = []
    while (ind < len(orign3)):
        orignStack.append(orign3[ind])
        if orign3[ind] == '~':
            if orign3[ind + 1] == '~':
                flag = 1
                orignStack.pop()
                ind = ind + 1
        ind = ind + 1

    if flag == 1:
        a = ''
        for i in orignStack:
            a = a + i
        orign4 = a
    else:
        orign4 = orign3
    # print('orign4', orign4)
    # 处理~(~p) 变为p#####################################
    ind = 0
    flag = 0
    bflag=0
    orignStack = []
    while (ind < len(orign4)):
        orignStack.append(orign4[ind])
        if orign4[ind] == '~':
            if orign4[ind + 1] == '(':
                left_bracket = 1
                if orign4[ind+2]=='~':
                    flag=1
                    orignStack.pop()
                    ind=ind+2
                    while left_bracket>=1:
                        orignStack.append(orign4[ind+1])
                        if orign4[ind+1]=='(':
                            left_bracket=left_bracket+1
                        if orign4[ind+1]==')':
                            left_bracket=left_bracket-1
                        if orign4[ind+1]=='%' or orign4[ind+1]=='^':
                            bflag=1
                        ind=ind+1

                    orignStack.pop()

        ind = ind + 1

    if flag==1 and bflag==0:
        a=''
        for i in orignStack:
            a=a+i
        orign5=a
    else:
        orign5=orign4
    #print('orign5',orign5)
    return orign5


#3.命题变量标准化，使后面y=w
def standard_var(orign):#对变量标准化,简化,不考虑多层嵌套

    flag = 1
    desOri=[]
    des=['w','k','j']
    j=0
    orignStack = []
    left_bracket=0
    ind = 0
    while flag!=0:
        flag=0
        while (ind < len(orign)):
            orignStack.append(orign[ind])
            if orign[ind] == '@' or orign[ind]=='#':
                x=orign[ind+1]#保存x
                if orign[ind+1] in desOri:
                    orignStack.append(des[j])
                    desOri.append(des[j])
                    j=j+1
                    orignStack.append(')')
                    ind=ind+3
                    if ind<len(orign):
                        if orign[ind].isalpha():#(@x)p(x,y)这种情况
                            orignStack.append(orign[ind])#p
                            ind = ind + 1
                            if orign[ind]=='(':
                                left_bracket = left_bracket + 1
                                orignStack.append(orign[ind])
                                ind=ind+1
                                while left_bracket>0:
                                    if orign[ind]== ')':
                                        left_bracket = left_bracket - 1
                                    if orign[ind]== '(':
                                        left_bracket=left_bracket+1
                                    if orign[ind]== x:
                                        flag=1
                                        orignStack.append(des[j-1])
                                    else:
                                        orignStack.append(orign[ind])
                                    ind=ind+1
                                ind=ind-1

                    if ind<len(orign):
                        if orign[ind] == '(' :
                            left_bracket = left_bracket + 1
                            orignStack.append(orign[ind])
                            ind = ind + 1
                            while left_bracket > 0:
                                if orign[ind] == ')':
                                    left_bracket = left_bracket - 1
                                if orign[ind] == '(':
                                    left_bracket = left_bracket + 1
                                if orign[ind] == x:
                                    flag = 1
                                    orignStack.append(des[j - 1])
                                else:
                                    orignStack.append(orign[ind])
                                ind = ind + 1
                            ind=ind-1

                else:
                    desOri.append(orign[ind+1])
            ind=ind+1

    a=''
    for i in orignStack:
        a=a+i
    orign2=a
    return orign2

#4.消去存在量词（skolem化）
def del_exists(orign):
    ind = 0
    flag = 1
    orignStack = []
    x=''
    y=''
    # 第1种情况：前面有全称量词 (@x)((#y)p(x,y))
    while flag!=0: #为了嵌套的情况出现
        flag=0
        while (ind < len(orign)):
            orignStack.append(orign[ind])

            if orign[ind] == '(' and orign[ind+1] == '@' and orign[ind+4]=='(' :
                x=orign[ind+2]
                orignStack.append(orign[ind+1:ind+5])
                ind=ind+5#指向
                while orign[ind]!='#':
                    orignStack.append(orign[ind])
                    ind=ind+1
                orignStack.pop()
                y=orign[ind+1]#为y
                ind=ind+2#指向p
                flag=1

            ind = ind + 1

        if flag==1:
            orignStack2=[]
            for i in orignStack:
                if i==y:
                    orignStack2.append('g(')
                    orignStack2.append(x)
                    orignStack2.append(')')
                else:
                    orignStack2.append(i)
    a = ''
    for i in orignStack2:
        a = a + i
    orign2 = a
    ind = 0
    flag = 1
    orignStack = []
    # 第2种情况：前面有全称量词 (#y)p(x,y)
    while flag != 0:  # 为了嵌套的情况出现
        flag = 0
        while (ind < len(orign2)):
            orignStack.append(orign2[ind])
            if orign2[ind] == '#' :
                y=orign2[ind+1]
                orignStack.pop()
                orignStack.pop()
                ind=ind+2#指向')'
                flag=1
            ind = ind + 1
        if flag==1:
            orignStack2 = []
            for i in orignStack:
                if i == y:
                    orignStack2.append('g(')
                    orignStack2.append(x)
                    orignStack2.append(')')
                else:
                    orignStack2.append(i)

    a = ''
    for i in orignStack2:
        a = a + i
    orign2 = a
    return orign2


#5.前束化
def convert_to_front(orign):#化为前束形
    ind = 0
    orignStack = []
    tempStack=[]#存放全称量词
    while (ind < len(orign)):
        orignStack.append(orign[ind])
        if orign[ind]=='(' and orign[ind+1]=='@':
            orignStack.pop()
            tempStack.append(orign[ind:ind+4])
            ind=ind+3

        ind = ind + 1

    orignStack=tempStack+orignStack
    a=''
    for i in orignStack:
        a = a + i
    orign2 = a
    return orign2

#6.消去全称量词
def del_all(orign):
    ind = 0
    orignStack = []
    ###########开始1#############
    while ind < len(orign):
        if orign[ind]=="@":
            orignStack.pop()
            ind += 3
        else:
            orignStack.append(orign[ind])
            ind += 1
    return "".join(orignStack)
    ###########结束1#############

#7.得到合取范式
def get_form(orign):
    global dict
    ind = 1
    orignStack = []
    global symbol
    #转换表达式,匹配括号等等,类似递归--2020.04.11完成
    while ind < len(orign):
        a = 1
        medStack = []
        if orign[ind] == ")" and orign[ind-1].isalpha():
            if(orign[ind-4]=="~" or orign[ind-4]=="^"):
                num = 4
            elif(orign[ind-2]==",") or (orign[ind-4] == ","):
                num = 7
                a = 2
                medStack.append(orign[ind])
            elif(orign[ind-5].isalpha()):
                num = 5
                if orign[ind-6]=="~" or orign[ind-6]=="^":
                    num += 1
                a = 2
                medStack.append(orign[ind])
            else :
                num = 3
            medStack.append(orign[ind])
            for i in range(num):
                medStack.append(orignStack.pop())
            medStack.reverse()
            orignStack.append(str(symbol))
            dict[str(symbol)] = "".join(medStack)
            symbol = symbol+1
        else:
            orignStack.append(orign[ind])
        ind += a
    orign = "".join(orignStack)
    #print(orign)

    #匹配)
    dict1 = {}
    symbol = 1
    while (")"in orign):
        orign,dict1 = Del_Brackets(orign,dict1)
        #print(orign)
    symbol -= 1
    #print(symbol)
    times = 1
    #print(dict1)
    #交换律，分配律
    while symbol > 0:
        orign=for_pro(orign,dict1[str(symbol)],orign.index(str(symbol)),times)
        times += 1
        symbol -= 1
        #print(orign)
    #返回原来的样式
    orignStack=[]
    for i in orign:
        if i not in dict.keys():
            orignStack.append(i)
        else:
            orignStack.append(dict[i])
    orign = "".join(orignStack)
    #print(orign)
    return orign

#处理循环括号
def Del_Brackets (orign,dict1):
    global symbol
    ind = 0
    orignStack=[]
    while (ind < len(orign)):
        if orign[ind] == ")" and orign[ind - 1].isdigit():
            med1Stack = []
            med1Stack.append(orign[ind])
            for i in range(4):
                med1Stack.append(orignStack.pop())
            med1Stack.reverse()
            dict1[str(symbol)] = "".join(med1Stack)
            orignStack.append(str(symbol))
            symbol += 1
        else:
            orignStack.append(orign[ind])
        ind += 1
    return "".join(orignStack),dict1

#分配律以及结合律
def for_pro(orign,str,index,symbol):
    #结合律
    if (str[2]==orign[index-1]):
        if symbol == 1:
            new_str = "("+orign[index-2]+str[2]+str[1]+str[2]+str[3]+")"
        else :
            new_str =  orign[index - 2] + str[2] + str[1] + str[2] + str[3]
    #分配律
    else :
        if symbol == 1:
            new_str ="("+orign[index-2]+orign[index-1]+str[1]+")"+str[2]+"("+orign[index-2]+orign[index-1]+str[3]+")"
        else :
            new_str =orign[index - 2] + orign[index - 1] + str[1] + ")" + str[2] + "(" + orign[index - 2] + \
                      orign[index - 1] + str[3]
    new_orign = orign.replace(orign[index - 2:index+1], new_str)
    return new_orign

#将公式转化为子句集合表示,变量更名
def To_Set(orign):
    orignStack = []
    #将公式转化为子句集合表示
    for i in orign :
        if i == "^":
            orignStack.append(",")
        else :
            orignStack.append(i)
    adjustStack = orign.split("^")
    #变量更名
    ind = 1
    re_dict = set()
    finalStack = []
    for ad in adjustStack :
        for re in re_dict :
            if re in ad :
                ad = ad.replace(re,"x"+str(ind))
                ind += 1
        finalStack.append(ad)
        for i in range(1,len(ad)):
            if (ad[i-1] == "(" and ad[i+1] == ")") or (ad[i-1] == "(" and ad[i+1] == ",") or (ad[i-1] == "," and ad[i+1]==")"):
               re_dict.add(ad[i])
            elif ad[i].isdigit():
                re_dict.add(ad[i-1]+ad[i])

    return finalStack
import sys
#codeIn = sys.stdin.read()
#orign=codeIn
orign = '(@x)(p(x)>((@y)(p(y)>p(f(x,y)))^~(@y)(Q(x,y)>p(y))))'
print('orign:',orign)
a=del_inlclue(orign)
print('1.去除蕴含后:',a)
a=dec_neg_rand(a)
print('2.处理否定连接词后:')
print(a)
a=standard_var(a)
print('3.变量命名标准化后:')
print(a)
a=del_exists(a)
print('4.消去存在量词后:')
print(a)
a=convert_to_front(a)
print('5.前束化后:')
print(a)
a=del_all(a)
print('6.消去全称量词后:')
print(a)
a=get_form(a)
print('7.化为合取范式后:')
print(a)
a=To_Set(a)
print('8.变量更名、将公式用子句集合表示:')
print(a)

#print(dict)
#print(a)
#选做
# #定义化为合取范式、将公式转化为子句集合表示、更换变量名称的函数#
# 调用函数完成子句集的分解
###########开始2#############


###########结束2#############