


with open("gracious_quran.txt") as f:
    lines = f.readlines()

verses = []
for line in lines:
    line = line.strip()
    if any(line):
        if ":" in line.split()[0]:
            verses.append([])
        verses[-1].append(line)


print(len(verses))