# Yacc example
import warnings
import ply.yacc as yacc
# Get the token map from the lexer. This is required.
from lex import tokens
from lex import reserved
from lex import symbol_tab

indentFlag=0
counter=0
tac=[]
def displayQuad(tac):
    print("Res\t| Op\t| Arg1\t| Arg2")
    for i in tac:
        for j in i:
            print(j, end='\t| ')
        print()
    print("#############################")

def p_assign(p):
    '''expression : ID EQUAL expression
                    | ID EQUAL EMP_LIST
                    | ID EQUAL EMP_TUPLE
                    | ID EQUAL EMP_SET
                    | ID EQUAL STR_CONST
                    | ID EQUAL ID
                    '''
                    
    p[0] = p[2]
    
    for value in symbol_tab.values():
        for key in value.keys():
            if key==p[1]:
                value[key].append(p[3])
    global indentFlag
    indentFlag = 0
    tac.append([p[1],p[2],p[3],indentFlag])

    
def p_expression_plus(p):
    '''expression : ID PLUS EQUAL term
                    | factor PLUS factor
                    | expression PLUS term
                    |  ID PLUS factor 
                    | factor PLUS ID
                    | ID PLUS ID
                    | expression PLUS ID
                    | ID PLUS expression
                    '''
    if(type(p[1])==int and type(p[3])==int):
        p[3]=p[1]+p[3]
        p[1]=' '
        tac.append([p[1],' ',p[3],indentFlag])
        p[0]=p[3]
    else:
        tac.append([p[1],p[2],p[3],indentFlag])
  

def p_print_statement(p):
    '''expression : PRINT PARANOPEN STR_CONST PARANCLOSE
                    | PRINT PARANOPEN ID PARANCLOSE
                    | PRINT PARANOPEN term PARANCLOSE'''
    global indentFlag 
    indentFlag=0

def p_expression_minus(p):
    '''expression : expression MINUS term
                    | ID MINUS EQUAL term
                    | MINUS term
                    | term MINUS expression
                    | term MINUS term
                    | ID MINUS ID
                    | term MINUS ID
                    | ID MINUS term'''
    if (len(p) == 4):
         #p[0] = p[1] - p[3]
        tac.append([p[1],p[2],p[3],0])
    elif (len(p) == 3):
         p[0] = -p[2]
         
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    
    '''term : term MULTIPLY factor
            | ID MULTIPLY ID
            | ID MULTIPLY factor
            | factor MULTIPLY ID
            | ID MULTIPLY term
            | term MULTIPLY ID
            | factor MULTIPLY factor
    '''
    if(type(p[1])==int and type(p[3])==int):
        p[3]=p[1]*p[3]
        p[1]=' '
        tac.append([p[1],' ',p[3]])
        p[0]=p[3]
    else:
        tac.append([p[1],p[2],p[3]])
  
 
def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    '''factor : INT
            | FLOAT'''
    p[0] = p[1]

def p_factor_expr(p):
    'factor : PARANOPEN expression PARANCLOSE'
    p[0] = p[2]

def p_loops(p):
    '''expression : whileloop
                    | forloop
                    | forloop2
                    | whileloop2'''
def p_while2(p):
    '''whileloop2 : LEVEL1 WHILE PARANOPEN ID EQUAL factor PARANCLOSE COLON 
                    | LEVEL1 WHILE PARANOPEN ID EQUAL STR_CONST PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID EQUAL ID PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATER factor PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATER STR_CONST PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATER ID PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATEREQ factor PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATEREQ STR_CONST PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID GREATEREQ ID PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSER factor PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSER STR_CONST PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSER ID PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSEREQ factor PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSEREQ STR_CONST PARANCLOSE COLON
                    | LEVEL1 WHILE PARANOPEN ID LESSEREQ ID PARANCLOSE COLON
                    | LEVEL1 WHILE BOOL COLON
                    | LEVEL1 WHILE STR_CONST COLON
                    | LEVEL1 WHILE factor COLON
                    | LEVEL1 WHILE ID COLON'''
    print("While loop starts")
    global indentFlag
    indentFlag=2

def p_while(p):
    '''whileloop :  WHILE PARANOPEN ID EQUAL factor PARANCLOSE COLON 
                    | WHILE PARANOPEN ID EQUAL STR_CONST PARANCLOSE COLON
                    | WHILE PARANOPEN ID EQUAL ID PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATER factor PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATER STR_CONST PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATER ID PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATEREQ factor PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATEREQ STR_CONST PARANCLOSE COLON
                    | WHILE PARANOPEN ID GREATEREQ ID PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSER factor PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSER STR_CONST PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSER ID PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSEREQ factor PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSEREQ STR_CONST PARANCLOSE COLON
                    | WHILE PARANOPEN ID LESSEREQ ID PARANCLOSE COLON
                    | WHILE BOOL COLON
                    | WHILE STR_CONST COLON
                    | WHILE factor COLON
                    | WHILE ID COLON'''
    print("While loop starts")
    global indentFlag
    indentFlag=1
    global counter
    if(len(p)==4):
        if(p[2]=='True' or p[2]==1):
            x=True
        if(p[2]=='False' or p[2]==1):
            x=False
        tac.append(['if',p[1],x])
    else:
        tac.append(['ifwhile',p[3],p[4],p[5]])
    counter+=1

def p_for2(p):
    '''forloop2 : LEVEL1 FOR ID IN RANGE PARANOPEN term PARANCLOSE COLON 
                    | LEVEL1 FOR ID IN RANGE PARANOPEN LEN PARANOPEN ID PARANCLOSE PARANCLOSE COLON
                    | LEVEL1 FOR ID IN STR_CONST COLON
                    | LEVEL1 FOR ID IN ID COLON
                    | LEVEL1 FOR ID IN PARANOPEN STR_CONST PARANCLOSE COLON
                 '''
    global indentFlag
    indentFlag=2
    print("For2 loop starts")
    
def p_for(p):
    '''forloop : FOR ID IN RANGE PARANOPEN term PARANCLOSE COLON 
                    | FOR ID IN RANGE PARANOPEN LEN PARANOPEN ID PARANCLOSE PARANCLOSE COLON
                    | FOR ID IN STR_CONST COLON
                    | FOR ID IN ID COLON
                    | FOR ID IN PARANOPEN STR_CONST PARANCLOSE COLON
                 ''' 
    global indentFlag
    indentFlag=1
    global counter
    label='l'
    temp='t'
    tac.append(['iffalse',p[2],label+str(counter),p[6],"<"])
    counter+=1
    print("For loop starts")

def p_indent_assign2(p):
    '''expression : LEVEL2 ID EQUAL expression
                  | LEVEL2 ID EQUAL ID
                  | LEVEL2 ID EQUAL STR_CONST'''
    if indentFlag==2:
        p[0] = p[2]
        print("level2   ",p[2])
        for value in symbol_tab.values():
            for key in value.keys():
                if key==p[2]:
                    value[key].append(p[4])

    else:
        print("in else")
        print("Syntax error in input")
        
def p_indent_assign(p):
    '''expression : LEVEL1 ID EQUAL expression
                  | LEVEL1 ID EQUAL ID
                  | LEVEL1 ID EQUAL STR_CONST
                  | LEVEL1 ID EQUAL factor'''
    if indentFlag==1:
        p[0] = p[2]
        tac.append([p[2],p[3],p[4],indentFlag])
        print("level1   ",p[2])
        for value in symbol_tab.values():
            for key in value.keys():
                if key==p[2]:
                    value[key].append(p[4])
        
    else:
        print("Syntax error in input")
            
def p_indent_expression_plus(p):
   '''expression : LEVEL1 ID PLUS EQUAL term
                    | LEVEL1 expression PLUS term
                    | LEVEL1 ID PLUS factor 
                    | LEVEL1 factor PLUS ID
                    | LEVEL1 ID PLUS ID
                    | LEVEL1 expression PLUS ID
                    | LEVEL1 ID PLUS expression
                    | LEVEL1 factor PLUS factor'''
    
   if(type(p[2])==int and type(p[4])==int):
        p[3]=p[1]+p[3]
        p[1]=' '
        tac.append([p[1],' ',p[3],1])
        p[0]=p[3]
   else:
        tac.append([p[2],p[3],p[4],1])
def p_indent2_print_statement(p):
    '''expression : LEVEL2 PRINT PARANOPEN STR_CONST PARANCLOSE
                    | LEVEL2 PRINT PARANOPEN ID PARANCLOSE
                    | LEVEL2 PRINT PARANOPEN term PARANCLOSE'''
    if indentFlag==2:
        pass 
    else:
        print("syntax error")
def p_indent_print_statement(p):
    '''expression : LEVEL1 PRINT PARANOPEN STR_CONST PARANCLOSE
                    | LEVEL1 PRINT PARANOPEN ID PARANCLOSE
                    | LEVEL1 PRINT PARANOPEN term PARANCLOSE'''
    if indentFlag==1:
        pass 
    else:
        print("Syntax error in input!")

def p_blank(p):
    'expression : '

def p_comment(p):
    '''expression : HASH expression
                    | HASH ID
                    | HASH STR_CONST'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

f = open('inputFile.py')
data = f.read()

data=data.split('\n')

for i in data:
    if(i!=' '):
        print(i)
        yacc.parse(i)

print("symbol table after updating the values")
print("###########################")
print("SYMBOL TABLE")
# print(symbol_tab)
print("\nID \t\t| TYPE \t\t| LINE NO. \t| VALUE\t\t| SCOPE\n")

if 'level0' in symbol_tab:  
    values0 = list(symbol_tab['level0'].values())
    keys0 = list(symbol_tab['level0'].keys())
    for i in range(len(keys0)):
        values0[i].insert(0,keys0[i])
    for i in values0:
        for j in range(1, len(i)):
            print(i[j],end=' \t\t| ')
        print("level 0")
        print()

if 'level1' in symbol_tab:
    values1 = list(symbol_tab['level1'].values())
    keys1 = list(symbol_tab['level1'].keys())
    for i in range(len(keys1)):
        values1[i].insert(0,keys1[i])

    for i in values1:
        for j in range(1, len(i)):
            print(i[j],end=' \t\t| ')
        print("level 1")
        print()

if 'level2' in symbol_tab:
    values2 = list(symbol_tab['level2'].values())
    keys2 = list(symbol_tab['level2'].keys())
    for i in range(len(keys2)):
        values2[i].insert(0,keys2[i])

    for i in values2:
        for j in range(1, len(i)):
            print(i[j],end=' \t\t| ')
        print("level 2")
        print()
# print(values0)
print("###########################")


#tac
temp='t'
tac1=[]
k=0
s=-1
goto=[]
dr=[]
for i in tac:
    
    temp1=temp+str(k)
    if(i[0]=='ifwhile'):
        if(len(goto)>0):
                    tac1.append(goto[-1])   
                    goto.pop()
                    s+=1
                    l='l'+str(s)
                    tac1.append([l,'Label',' ',' '])
        dr.append(i[1])
        s+=1
        l='l'+str(s)
        tac1.append([l,'Label',' ',' '])
        tac1.append([temp1,i[1],i[2],i[3]])
        tac1.append(['iffalse',temp1,' ','l'+str(s+1)])
        k+=1
        temp1=temp+str(k)
        tac1.append([temp1,'*',i[1],4])
        k+=1
        temp1=temp+str(k)
        tac1.append([i[1],'+',i[1],1])
        goto.append([l,'goto',' ',' '])
        
    if(i[0]=='if'):
        if(len(goto)>0):
                    tac1.append(goto[-1])   
                    goto.pop()
                    s+=1
                    l='l'+str(s)
                    tac1.append([l,'Label',' ',' '])
        tac1.append([temp1,' ',' ',i[2]])
        s+=1
        l='l'+str(s)
        tac1.append([l,'Label',' ',' '])
        tac1.append(['iffalse',temp1,' ','l'+str(s+1)])
        
        goto.append([l,'goto',' ',' '])

    if(i[0]=='iffalse'):
        if(len(goto)>0):
                    tac1.append(goto[-1])   
                    goto.pop()
                    s+=1
                    l='l'+str(s)
                    tac1.append([l,'Label',' ',' '])
                   
                
                    
        tac1.append([i[1],' ',' ',0,' '])
        k+=1
        temp1=temp+str(k)
        s+=1
        l='l'+str(s)
        tac1.append([l,'Label',' ',' '])                        
        tac1.append([temp1,i[4],i[1],i[3]])
        tac1.append([i[0],temp1,' ','l'+str(s+1)])   
        k+=1
        temp1=temp+str(k)
        tac1.append([temp1,'*',i[1],4])
        tac1.append([i[1],'+',i[1],1])
        goto.append([l,'goto',' ',' '])
    if(len(goto)>0 and len(i)==4):
        if(i[3]==0):
                    tac1.append(goto[-1])   
                    goto.pop() 
                    s+=1
                    l='l'+str(s)
                    tac1.append([l,'Label',' ',' '])

    
    if(i[0]!='iffalse' and i[0]!='if' and i[0]!='ifwhile'):         
        if(i[1]=='='):
               if(i[2]==None):
                    temp3='t'+str(int(temp1[1])-1)
               else:
                    temp3=i[2]
               tac1.append([i[0],' ',' ',temp3])
               
        else:
                if(i[0]==None):
                    temp2='t'+str(int(temp1[1])-1)
                else:
                    temp2=i[0]
                print(temp2)
                tac1.append([temp1,i[1],temp2,i[2]])
                k+=1   
        
     
if(len(goto)>0):
    tac1.append(goto[-1])   
    goto.pop()
                   

for i in tac1:
    if(i[3]==None):
        x1=i[0]
        x='t'+str(int(x1[1])-1)
        i[3]=x
if(tac1[::-1][0][1]=='goto'):
    s+=1
    l='l'+str(s)
    tac1.append([l,'Label',' ',' '])

def common_sub_eliminate(tacc):
    
    cse=[]
    for i in range(len(tacc)):
        if(tacc[i][1]!=' ' and tac1[i][1]!='Label' and tac1[i][1]!='goto'):
            cse.append([[tacc[i][1],tacc[i][2],tacc[i][3]],i])
    common=[]
    for i in range(len(cse)):
        a=cse[i][0]
        for j in range(i+1,len(cse)):
            b=cse[j][0]
            if(a==b):
                common.append([cse[i][1],cse[j][1]])
    
    common=common[::-1]
    
    for i in common:
        tacc[i[1]][1],tacc[i[1]][2],tacc[i[1]][3]=' ',' ',' '
        tacc[i[1]][3]=tacc[i[0]][0]
    return tacc


def copy_propagation(tac1):
    for i in range(len(tac1)):
      if((tac1[i][1]==' ') and (tac1[i][2]==' ') and (type(tac1[i][3])==str)):
            res=tac1[i][0]
            arg=tac1[i][3]
     
            for j in range(i+1,len(tac1)):
                      if(tac1[j][2]==res):
                          tac1[j][2]=arg
                      if(tac1[j][3]==res):
                          tac1[j][3]=arg
            


def constant_folding(tac1):
    for i in tac1:
        if(i[1]!=' '):
            if(type(i[2])==int and type(i[3])==int):
                if(i[1]=='*'):
                    i[3]=i[2]*i[3]
                    i[2],i[1]=' ',' '
                elif(i[1]=='+'):
                    i[3]=i[2]+i[3]
                    i[2],i[1]=' ',' '
                elif(i[1]=='-'):
                    i[3]=i[2]-i[3]
                    i[2],i[1]=' ',' '
                else:
                    i[3]=i[2]/i[3]
                    i[2],i[1]=' ',' '



def constant_propagation(tac1):
    
    for i in range(len(tac1)):
      if(len(tac1[i])<=4):
          if(tac1[i][0] not in dr):
              if((tac1[i][1]==' ') and (tac1[i][2]==' ') and (type(tac1[i][3])==int)):
                    res=tac1[i][0]
                    arg=tac1[i][3]
                    for j in range(i+1,len(tac1)):
                          if(tac1[j][2]==res):
                              tac1[j][2]=arg
                          if(tac1[j][3]==res):
                              tac1[j][3]=arg
                

def dead_code_elimination(tac1):
    
    rem=[]
    lo=[]
    
    for i in range(len(tac1)):
            flag=0
            if(tac1[i][1]==' ' and tac1[i][2]==' ' and type(tac1[i][3])==int):
                res=tac1[i][0]
                for j in range(i+1,len(tac1)):
                    if((tac1[j][3]==res) or (tac1[j][2]==res)):
                        flag=1
                if(flag==0):
                    rem.append(i)
                    
            elif((type(tac1[i][3])==bool) and tac1[i+1][1]=='Label'):
                if(tac1[i][3]==False):
                    lo.append(i)
                    rem.append(i)
            
    for i in lo:
        for j in range(i+2,len(tac1)):
            rem.append(j)
            if(tac1[j][1]=='Label'):
                break
    rem=list(set(rem))
    rem=sorted(rem,reverse=True) 
    rem=rem[1:]
    for i in rem:
        del tac1[i]


# print("TAC")
tacFile = open('TAC.txt', 'w')
tacFileList = []
for i in tac1:
    # print(i)
    if i[1]==" " and i[3]==" ":
        tacFileList.append(str(i[0]) + " = " + str(i[2]) + "\n")
    elif i[1]=="goto":
        tacFileList.append(str(i[1])+ " " +str(i[0])+"\n")
    elif i[1]=="Label":
        tacFileList.append(str(i[0])+":"+"\n")
    elif i[1] in ["+","-","*","/",">","<",">=","<="]:
        tacFileList.append(str(i[0])+ " = "+ str(i[2])+" "+str(i[1])+" "+str(i[3])+"\n")
    elif i[0] in ["iffalse", "iftrue"]:
        tacFileList.append(str(i[0])+ " " +str(i[1])+ " goto "+ str(i[3])+"\n")

    else:
        tacFileList.append(str(i[0]) + " = " + str(i[1]) + str(i[2]) + str(i[3]) + "\n")

for i in range(len(tacFileList)):
    tacFile.write(tacFileList[i])
    
tacFile.close()
# # print(tacFileList)

print("Quadruple table before common_sub_eliminate:")
displayQuad(tac1)

common_sub_eliminate(tac1)
print("Quadruple table after common_sub_eliminate:")
displayQuad(tac1)


print("Quadruple table before copy_propagation")
displayQuad(tac1)
copy_propagation(tac1)
print("Quadruple table after copy_propagation:")
displayQuad(tac1)


print("Quadruple table before constant_propagation:")
displayQuad(tac1)
constant_propagation(tac1)
print("Quadruple table after constant_propagation:")
displayQuad(tac1)

print("Quadruple table before constant_folding:")
displayQuad(tac1)
print("Quadruple table after constant_folding:")
constant_folding(tac1)
displayQuad(tac1)


print("Quadruple table before dead_code_elimination:")
displayQuad(tac1)
print("Quadruple table after dead_code_elimination:")
dead_code_elimination(tac1)
displayQuad(tac1)

