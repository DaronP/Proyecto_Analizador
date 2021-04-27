from graphviz import Digraph
import os
from operator import itemgetter

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

EPSILON = 'ε'

def grafo(nodos, lim, name):
    f = Digraph('finite_state_machine', filename='./%s.gv' % name)
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for i in range(len(lim)):
        f.node(str(lim[i][1]))
    f.attr('node', shape='circle')
    for i in range(len(nodos)):
        f.edge(str(nodos[i][0]), str(nodos[i][2]), label= str(nodos[i][1]))

    f.view()


def sacar_lista(lista, pila = []):
    res = []
    try:
        for val in lista:
            if type(val) is list:
                sacar_lista(val, pila)
            else:
                pila.append(val)
    except:
        pass
    for j in range(0, len(pila), 3):
        if j < len(pila):
            res.append([pila[j], pila[j + 1], pila[j + 2]])
    return res


def cerr_e(trans, lim):
    if type(lim) is int:
        nodos_limit = []
        nodos_limit.append(lim)
    else:
        nodos_limit = list(lim)

    if type(nodos_limit) is list:
        for nodo in nodos_limit:
            epsilon = []
            for nod in trans:
                if nod[0] == nodo and nod[1] == EPSILON:
                    epsilon.append(nod)
            for tran in epsilon:
                if tran[2] not in nodos_limit:
                    nodos_limit.append(tran[2])
    
    e_trans = set()
    for val in nodos_limit:
        e_trans.add(val)

    return e_trans

def move(trans, estado, symbol):
    try:
        estado = list(estado)
    except:
        pass

    move_trans = []
    #Si es una lista de estados
    if type(estado) is list:
        for est in estado:
            transicion = []
            for nodo in trans:
                if nodo[0] == est and nodo[1] == symbol:
                    transicion.append(nodo)
            
            for tran in transicion:
                if tran[2] not in move_trans:
                    move_trans.append(tran[2])
        
        mov = set()
        for i in move_trans:
            mov.add(i)
        
        return mov

    #Si es un unico estado
    else:
        transicion = []
        for nodo in trans:
            if nodo[0] == estado and nodo[1] == symbol:
                transicion.append(nodo)
        
        for item in transicion:
            if item[2] not in move_trans:
                move_trans.append(item[2])
        
        mov = set()
        for i in move_trans:
            mov.add(i)
        
        return mov

def transition(nodo_inicial, char, trans):
    if type(nodo_inicial) is not list:
        nodo_inicial = [nodo_inicial]

    flag = False
    nodo_trans = []
    
    for nodo in nodo_inicial:        
        for t in trans:
            if t[0] == nodo and t[1] == char:
                nodo_trans.append(t)
        
    if len(nodo_trans) > 0:
        flag = True

    return flag
    
def simulacion(trans_S, cadena, strt_end_S, alfa):

    for char in cadena:
        if char not in alfa:
            return Catch_Error(0, cadena)
        
        else:
            trans_char = transition(strt_end_S[0][0], char, trans_S)
            
            if type(strt_end_S[0][0]) is not list:
                nodo_inicial = [strt_end_S[0][0]]

            flag = False
            nodo_trans = []

            for nodo in nodo_inicial:        
                for t in trans_S:
                    if t[0] == nodo and t[1] == char:
                        nodo_trans.append(t)
                
            if len(nodo_trans) > 0:
                flag = True

            return flag

    

def postfix(exp):

    exp = exp[:0] + '(' + exp[0:]
    exp = exp[:-1] + exp[-1] + ')'

    pila = []
    l = []
    alfabeto = []

    cadenaF = []

    exp = exp.replace('?', '|ε')

    for char in exp:
        #Leyendo letras del lenguaje
        if (ord(char) > 64 and ord(char) < 91) or (ord(char) > 96 and ord(char) < 123) or char ==EPSILON or char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or char == '5' or char == '6' or char == '7' or char == '8' or char == '9':
            l.append(char)
            alfabeto.append(char)
        #Leyendo otros tokens
        else:
            #Parentesis
            if pila == [] or char == '(' or pila[-1] == '(':
                pila.append(char)

            #Kleene o mas
            elif char == '*' or char == '+' or char == '?':
                if pila[-1] == '*' or pila[-1] == '+':
                    l.append(char)
                else:
                    pila.append(char)

            #Concatenacion
            elif char == '_':
                for i in range(len(pila) - 1):
                    if len(pila) > 0 and (pila[-1] == '*' or pila[-1] == '+'):
                        l.append(pila.pop())
                    
                if pila[len(pila)-1] == '_':
                    l.append(char)
                else:
                    pila.append(char)

            #Or
            elif char == '|':
                while pila[-1] == '*' or pila[-1] == '+' or pila[-1] == '_':
                    l.append(pila.pop())

                if pila[-1] == '|':
                    l.append(char)
                else:
                    pila.append(char)

            
            else:      
                for i in range(len(pila) - 1):
                    if len(pila) > 0 and pila[-1] != '(':
                        l.append(pila.pop())
                pila.pop()
                
                       

    while len(pila) > 1:
        l.append(pila.pop())
    
    #Evaluacion del alfabeto
    for i in range(len(alfabeto) - 1, - 1, - 1):        
        if(alfabeto[i] in alfabeto[:i]):
            del(alfabeto[i])
    
    for i in range(len(l)):
        if l[i] == '+':
            cadenaF.append(l[i-1])  
            cadenaF.append('*')                      
            cadenaF.append('_')
            
        elif l[i] != '+':
            cadenaF.append(l[i])

    return(cadenaF, alfabeto)

def or_ing(char):
    char_list = []

    for i in char:
        if i != char[-1]:
            char_list.append(i)
            char_list.append('|')
        else:
            char_list.append(i)
    
    char_str = ""

    for i in char_list:
        char_str += i
    
    return char_str

def Catch_Error(err, word = ""):
    if err == 0:
        print("ERROR: Token no existente: ", word)
    if err == 1:
        print("ERROR: New Line no existente")
    if err == 2:
        print("ERROR: Palabra no existente: ", word)

    
def scanner(keywords, minimo, fname):
    t_file = open(fname, "r")

    t_list = []

    for line in t_file:
        t_list.append(line)

    t_file.close()

    for linea in t_list:
        flag_fl = False
        first_letter = ""
        word = ""

        for l in linea:
            if flag_fl == False:
                first_letter = l
                flag_fl = True

            if l == chr(32):
                if word in keywords:
                    print("Keyword: ", word)
                    word = ""
                    flag_fl = False

                else:
                    if first_letter in minimo[0][2]:
                        flag_word = simulacion(minimo[0][0], word, minimo[0][1], minimo[0][2])

                        if flag_word and word not in keywords:
                            print("Token: ", word, " Type: ident")
                            word = ""
                        else:
                            Catch_Error(0, word)

                    elif first_letter in minimo[1][2]:
                        flag_word = simulacion(minimo[1][0], word, minimo[1][1], minimo[0][2])

                        if flag_word and word not in keywords:
                            print("Token: ", word, " Type: number")
                            word = ""
                        else:
                            Catch_Error(0, word)
                    
                    if first_letter not in minimo[0][2] and first_letter not in minimo[1][2]:
                        Catch_Error(2, word=word)
            
            elif l == chr(10):
                print("New Line")
                if word in keywords:
                    print("Keyword: ", word)
                    word = ""
                    flag_fl = False

                else:
                    if first_letter in minimo[0][2]:
                        flag_word = simulacion(minimo[0][0], word, minimo[0][1], minimo[0][2])

                        if flag_word and word not in keywords:
                            print("Token: ", word, " Type: ident")
                            word = ""
                        else:
                            Catch_Error(0, word)

                    elif first_letter in minimo[1][2]:
                        flag_word = simulacion(minimo[1][0], word, minimo[1][1], minimo[0][2])

                        if flag_word and word not in keywords:
                            print("Token: ", word, " Type: number")
                            word = ""
                        else:
                            Catch_Error(0, word)
                    
                    if first_letter not in minimo[0][2] and first_letter not in minimo[1][2]:
                        Catch_Error(2, word=word)
            
            else:
                word += l
            
            

