import re
find_valid_codon_regex = r"(\w{3}\s[\w*])\s*$"
folder_address = r"C:\Users\Dell\Desktop\Folders\botcamp\mini project after w6\mini project\extract file\data" 
dictonary_codon = {}
dictonary_amino = {}
c_liner_filecodon = 0
ls_errors = []
with open(f"{folder_address}\\codon_table.txt", "r", encoding="utf-8") as file:
    reader = file.readlines()
    for read in reader:
        c_liner_filecodon+=1
        read = read.strip()
        if read.startswith('#') == False:
            if read == "":
                continue
            else:
                if re.search(find_valid_codon_regex, read):
                    read = read.split()
                    if read[0] not in dictonary_codon.keys():
                        if len(read[0]) == 3:
                            dictonary_codon[read[0]] = read[1]
                    else:
                        ls_errors.append(f"{" ".join(read)} valid nist chon az ghabl vojod darad dar line {c_liner_filecodon} toy file codon")
                else:
                    ls_errors.append(f"datafileeror in file codon '{read}' valid nist dar line {c_liner_filecodon}")

c_liner_fileamino = 0
find_valid_amino_regex = r"^\s*([ACDEFGHIKLMNPQRSTVWY]\s+\d+(?:\.\d+)?)\s*$"
with open(f"{folder_address}\\amino_weights.txt", "r", encoding="utf-8") as file:
    reader = file.readlines()
    for read in reader:
        c_liner_fileamino += 1
        read = read.strip()
        if read.startswith('#') == False:
            if read == "":
                continue
            else:
                if re.search(find_valid_amino_regex, read):
                    read = read.split()
                    if read[0] not in dictonary_amino:
                        dictonary_amino[read[0]] = read[1]
                    else:
                        ls_errors.append(f"datafileeror in {read[0]} ba {dictonary_amino[read[0]]} meghdar az ghabl hast va man ejazeh nadarm meghdar ra bezarm {read[1]}")
                else:
                    ls_errors.append(f"datafileeror in file amino '{read}' valid nist dar line {c_liner_fileamino}")


if len(dictonary_codon.keys()) == 64:
    print("true")
else:
    print("tedad codon ha 64 ta nist")

if len(dictonary_amino.keys()) == 20:
    print("true")
else:
    print("tedad amino ha 20 ta nist")

print("vaghti joftsh true bashe okyeh")
