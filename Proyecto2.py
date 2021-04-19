import thomson
import subconjuntos
import libs

#CHARACTERS
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
letters = character(letters)

digits = "0123456789"
digits = character(digits)

indent = chr(9)
indent = character(indent)
eol = chr(10)
eol = character(eol)

#KEYWORDS
keywords =['while', 'for', 'if', 'switch', 'case']
#TOKENS
ident = letters+"(("+letters+"|"+digits+")*)"
number = digits+"(("+digits+")*)"

letter_kw = [ident]
num_kw = [number]

