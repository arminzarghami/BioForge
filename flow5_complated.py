d = {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L', 'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*', 'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L', 'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M', 'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V', 'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'}
from models import *
ls_protein = []

def mrna_finder(x):
    ls = []
    result_ls = list()
    for i in range(0, len(x), 3):
        this_codon = x[i:i+3]
        if len(this_codon) == 3:
            ls.append(this_codon)
    try:
        ls = ls[ls.index("AUG"):]
    except ValueError:
        return
    else:
        protein = ''
        while ls != []:
            codon = ls.pop(0)
            if codon in ["UAA", "UAG", "UGA"]:
                try:
                    ls = ls[ls.index("AUG"):]
                except ValueError:
                    result_ls.append((protein, "comel"))
                    return result_ls
                else:
                    result_ls.append((protein, "comel"))
                    protein = ''
            elif codon in d.keys():
                protein += d[codon]
            else:
                return (f"inyeki codon '{codon}' dar dictonary vojod nadarad, vorodi haro check konid, korogi ba in vaze asla kamel , dorost nist")
        if ls == []:
            result_ls.append((protein, "naghes"))
    return result_ls

for orf in orfs:
    original_rna = orf['rna']
    if original_rna.find("AUG") != -1:
        rna = original_rna[original_rna.find("AUG"):]
    else:
        continue
    ls_protein.append(mrna_finder(original_rna)) # bayad toy object bashe ke bedonim in deta ha marbot be keye masalan bege ke id felan ba ba in rna inaro dareh     ye hamchin chizy
# print('--->', ls_protein)
print('--- all protein data ---')
print(ls_protein)
"""
for this_protein in ls_protein:
    wigth_amino = 18.015
    for this_amino in this_protein:
        wigth_amino += amino_weights[this_amino]
    lenght_amino = len(this_protein)
"""
list_test_lenghtweight_filter = []
for i in ls_protein:
    sumer_aminos = 18.015
    for this in i:
        for amino in this[0]:
            sumer_aminos += amino_weights[amino]
    # print(i[0])
    # print(f"sum: {sumer_aminos} lenght: {len(this[0])}")
    list_test_lenghtweight_filter.append((sumer_aminos, len(this[0])))
    # print("+---+"*11)

print('--------- all data lsit lenght&weight ---------')
print(list_test_lenghtweight_filter)

def lenght_filter(this_len, filter_input): # This comes from the object itself. This list is just for testing
    for l in this_len:
        if l[1] >= filter_input:
            print(l[1]) # اینجا همون شی که قابل قبول است را داری میتونی بریزیش توی یک لیست یا ...

print(f"{'---'*11} lenght_filter {'---'*11}")
lenght_filter(list_test_lenghtweight_filter, 3)

def weight_filter(this_weight, filter_input): # This comes from the object itself. This list is just for testing
    for l in this_weight:
        # print(l[0])
        if l[0] >= filter_input:
            print(l[0]) # اینجا همون شی که قابل قبول است را داری میتونی بریزیش توی یک لیست یا ...
print(f"{'---'*11} weight_filter {'---'*11}")
weight_filter(list_test_lenghtweight_filter, 795)

