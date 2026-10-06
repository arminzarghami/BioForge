START_CODON = "AUG"
STOP_CODONS = {"UAA", "UAG", "UGA"}


def dna_replace(dna):

    tempDNA = str(dna)
    tempDNA = tempDNA.replace("A", "X")
    tempDNA = tempDNA.replace("T", "A")
    tempDNA = tempDNA.replace("X", "T")

    tempDNA = tempDNA.replace("C", "X")
    tempDNA = tempDNA.replace("G", "C")
    tempDNA = tempDNA.replace("X", "G")

    return tempDNA


def reverse_dna(dna):
    reversed_dna = dna[::-1]
    return reversed_dna

def reverse_complement(dna):
    complementDNA = dna_replace(dna)
    reversedAndComplementedDNA = reverse_dna(complementDNA)
    return reversedAndComplementedDNA


def dna_to_rna(dna):
    return dna.replace("T", "U")


def search_frame(rna, frame, strand, original_dna_length):

    orfs = []
    i = frame

    while i + 2 < len(rna):
        codon = rna[i:i + 3]

        if codon == START_CODON:
            start = i
            j = i + 3

            stop_found = False
            stop_position = None
            stop_codon = None

            while j + 2 < len(rna):
                next_codon = rna[j:j + 3]

                if next_codon in STOP_CODONS:
                    stop_found = True
                    stop_position = j
                    stop_codon = next_codon
                    break
                j += 3

            if stop_found:
                orf_rna = rna[start:stop_position + 3]
                is_complete = True

            else:
                remaining_length = len(rna) - start
                complete_length = (remaining_length // 3) * 3

                orf_rna = rna[start:start + complete_length]
                is_complete = False
          
            if strand == "Forward":
                start_position = start

            else:
                start_position = original_dna_length - 1 - start
          
            orf = {
                "dna": dna,
                "strand": strand, #reverse or forward 
                "frame": frame, #which frame? 0 1 or 2
                "start_pos": start_position, 
                "stop_pos": stop_position,
                "stop_codon": stop_codon,
                "rna": orf_rna, #RNA
                "is_complete": is_complete #is a complete RNA?
            }

            orfs.append(orf)
            i += 3

        else:
            i += 3

    return orfs


def find_orfs(dna):

    all_orfs = []
    dna = dna.upper()
    original_length = len(dna)
    forward_rna = dna_to_rna(dna)

    for frame in range(3):
        frame_orfs = search_frame(
            forward_rna,
            frame,
            "Forward",
            original_length
        )
        all_orfs.extend(frame_orfs)

    reversedRNA = reverse_complement(dna)

    for frame in range(3):
        frame_orfs = search_frame(
            reversedRNA,
            frame,
            "Reverse",
            original_length
        )
        all_orfs.extend(frame_orfs)

    return all_orfs


dna = "ATGCTTTCATAGUAAUGA"
reversed_dna = reverse_dna(dna)
rna = dna_to_rna(dna)
orfs = find_orfs(dna)

for orf in orfs:

    print("_______________________________")
    print(f"Dna: {dna}")
    print(f"Reversed Dna: {reversed_dna}")
    print(f"Full Rna: {rna}")
    print(f"Strand: {orf["strand"]}")
    print(f"Frame: {orf["frame"]}")
    print(f"Start position index: {orf["start_pos"]}")
    print(f"Stop position index: {orf["stop_pos"]}")
    print(f"Stop codons are: {orf['stop_codon']} ")
    print(f"RNA: {orf["rna"]}")
    print(f"is_Complete: {orf["is_complete"]}")
