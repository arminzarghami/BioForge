import re

# userInput = input()
# reversed = int(str(userInput)[::-1])
# print(reversed)



#AUGCUUUCA 
#forward frame 0: A to A from first to last
#forward frame 1: U to A
#forward frame 2: G to A

#then reverse it and do the same for reverse frame ...


# AUG → Methionine (M
# CUU → Leucine (L
# UCA → Serine (S

# AUG CUU UCA --> MLS


codonFile = open(r"E:\PythonQuera\MiniProject\data\codon_table.txt", "r")

readFile = codonFile.readline()

# RNA = input()
# result = re.search(RNA , readFile)

codonDict = {} 

for line in readFile:
    key, value = line.strip().split(" ", 1)
    codonDict[key.strip()] = value.strip()

print(codonDict)

res = {}

with open(r"E:\PythonQuera\MiniProject\data\codon_table.txt", "r") as file:
    for line in file:
            key, value = line.strip().split(':', 1)
            res[key.strip()] = value.strip()

        

print(res)