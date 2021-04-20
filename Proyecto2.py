from thomson import *
from subconjuntos import *
from libs import *

#CHARACTERS
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
letters = or_ing(letters)

digits = "0123456789"
digits = or_ing(digits)

indent = chr(9)
indent = or_ing(indent)
eol = chr(10)
eol = or_ing(eol)

#KEYWORDS
keywords =['while', 'for', 'if', 'switch', 'case']
#TOKENS
ident = "("+letters+")_(("+letters+"|"+digits+")*)"
number = "("+digits+")_(("+digits+")*)"

letter_kw = [ident]
num_kw = [number]

print(letter_kw)
pos_fx, alfa = postfix(letter_kw) 

#Iniciando el AFN 
trans_t, strt_end_t = thomson(pos_fx, alfa)
#Iniciando el AFD
trans_afd, strt_end_afd = subconjuntos(trans_t, strt_end_t)

