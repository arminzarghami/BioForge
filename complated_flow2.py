import re


def test(string):
    try:
        if "organism=" in string:
            user_id, _, organism, sample = re.search(
                r"^>(\w+)\s+(organism=(\w*)\s+)sample=(\w+)\s*$",
                string
            ).groups()

            return user_id, organism, sample

        else:
            user_id, sample = re.search(
                r"^>(\w+)\s+sample=(\w+)\s*$",
                string
            ).groups()

            return user_id, "", sample

    except AttributeError:
        return False


completed_record = []
ls_errors = []

current_header = None
sequence = ""

file_path = r"C:\Users\Dell\Desktop\Folders\botcamp\mini project after w6\mini project\extract file\data"

with open(f"{file_path}\\test_fasta.txt", "r", encoding="utf-8") as file:

    for this_line in file:

        this_line = this_line.strip()

        # New header
        if this_line.startswith(">"):

            # First save the previous record
            if current_header is not None:

                sequence = sequence.upper()

                if re.fullmatch(r"[ATCG]+", sequence):
                    completed_record.append(
                        (current_header, sequence)
                    )
                else:
                    ls_errors.append("FastaFileError")

            # Now start the new record
            current_header = test(this_line)
            sequence = ""

        else:
            # Sequence line
            sequence += this_line
            # print(sequence)
            # break

# Save the final record
if current_header is not None:

    sequence = sequence.upper()

    if re.fullmatch(r"[ATCG]+", sequence):
        completed_record.append(
            (current_header, sequence)
        )
    else:
        ls_errors.append("FastaFileError")


# print(completed_record)
# print(ls_errors)

for i in completed_record:
    print(i)


for i in ls_errors:
    print(i)

# line aval bashe error hesabesh nimikoneh
