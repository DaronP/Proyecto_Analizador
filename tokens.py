

#Leyendo archivo COCOL

#fn = input("Ingrese el nombre del archivo...")

f = open("cocol.txt", "r")
lines = []
tokens = []
keywords = []
characters = []

for line in f.readlines():
    if line[-1:] == "\n":
        lines.append(line[:-1])
    else:
        lines.append(line)
f.close()

name = lines[0].split(" ")[-1]
print(name)

flag = ""

for line in lines:
    if line != "":
        if line == "TOKENS":
            flag = "T"
        if line == "KEYWORDS":
            flag = "K"
        if line == "CHARACTERS":
            flag = "C"
        if "END " in line:
            flag = "end"

        if flag == "T":
            tokens.append(line)
        if flag == "C":
            characters.append(line)
        if flag == "K":
            keywords.append(line)


#Creando el nuevo archivo de Python


new_file = open(name + ".py", 'w')

new_file.write("from thomson import *\n")
new_file.write("from subconjuntos import *\n")
new_file.write("from libs import *\n")
new_file.write("\n")

chrs = []
for char in characters:
    if characters.index(char) == 0:
        new_file.write("#" + char + "\n")

    else:
        caracter = char.replace(".", "")
        char_list = caracter.split(" = ")

        if "chr" in char_list[1] or "CHR" in char_list[1]:
            new_file.write(caracter + "\n")
            new_file.write(char_list[0] + " = or_ing(" + str(char_list[0]).lower() + ")"+ "\n")
            chrs.append(char_list[1])
        
        else:
            new_file.write(caracter + "\n")
            new_file.write(char_list[0] + " = or_ing(" + str(char_list[0]) + ")"+ "\n")
            new_file.write("\n")
new_file.write("\n")

kw_list = []
for kw in keywords:
    if keywords.index(kw) == 0:
        new_file.write("#" + kw + "\n")

    else:
        kyw = kw.replace(chr(34), "")
        kyw = kyw.replace(chr(39), "")
        kyw = kyw.replace(".", "")
        kws = kyw.split(" = ")
        kw_list.append(kws[-1])

new_file.write("keywords =" + str(kw_list))
new_file.write("\n")

letter_kw = []
num_kw = []
for token in tokens:
    if tokens.index(token) == 0:
        new_file.write("#" + token + "\n")

    else:
        t = token.replace(".", "")
        t = t.replace(" = ", " = " + chr(34) + "(" + chr(34) + "+")
        t = t.replace("{", "+" + chr(34) + ")_((" + chr(34) + "+")
        t = t.replace("|", "+" + chr(34) + "|" + chr(34) + "+")
        t = t.replace("}", "+" + chr(34) + ")*)" + chr(34))

        if " EXCEPT KEYWORDS" in t:
            t_l = t.split(" = ")
            letter_kw.append(t_l[0])
            t = t.replace(" EXCEPT KEYWORDS", "")
        else:
            t_l = t.split(" = ")
            num_kw.append(t_l[0])

        new_file.write(t + "\n")
new_file.write("\n")

letter_str = ""
for i in letter_kw:
    letter_str += i
new_file.write("letter_kw = " + "[" + letter_str + "]\n")

num_str = ""
for i in num_kw:
    num_str += i
new_file.write("num_kw = " + "[" + num_str + "]\n")
new_file.write("\n")

new_file.write("print(letter_kw)")

new_file.write("\n")
new_file.write("pos_fx, alfa = postfix(letter_kw) \n")
new_file.write("\n")
new_file.write("#Iniciando el AFN \n")
new_file.write("trans_t, strt_end_t = thomson(pos_fx, alfa)\n")
new_file.write("#Iniciando el AFD\n")
new_file.write("trans_afd, strt_end_afd = subconjuntos(trans_t, strt_end_t)\n")
new_file.write("\n")

new_file.close()