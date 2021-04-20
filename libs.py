from graphviz import Digraph
import os
from operator import itemgetter

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
    
def simulacion(trans_S, cadena, strt_end_S, alfa, tipo = 1):
    for item in cadena:
        if item not in alfa:
            print("no existe en alfabeto")
            return 0

    if tipo == 0:
        move_list = []
        for item in cadena:
            for estado in trans_S:
                move_item_T = move(trans_S, estado[0], item)
                move_list.append(move_item_T)

        #eliminando duplicados
        for i in range(len(move_list) - 1, - 1, - 1):        
            if not move_list[i]:
                del(move_list[i])

        ultimo_move = move(trans_S, move_list[-1], EPSILON)
        
        for u in ultimo_move:
            if u == strt_end_S[-1][-1]:
                return 1
            else:
                return 0

    else:
        for item in cadena:
            move_item_S = move(trans_S, strt_end_S[0][0], item)
            
            if not move_item_S:
                print("no tiene transicion")
                return 0

            list_s = list(move_item_S)

            nodo_s = list_s[0]

        count_s = 0

        for nodo in range(len(strt_end_S)):
            if nodo_s == strt_end_S[nodo][1]:
                count_s += 1

        if count_s > 0:
            return 1

def postfix(exp):
    pila = []
    l = []
    alfabeto = []

    cadenaF = []

    exp = exp.replace('?', '|ε')

    for char in exp:
        #Leyendo letras del lenguaje
        if (ord(char) > 96 and ord(char) < 123) or char ==EPSILON or char == '0' or char == '1':
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

    