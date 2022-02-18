from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import matplotlib.pyplot as plt
map = {"Vitis vinifera":0,
       "Drosophila melanogaster":0}
color = {"Vitis vinifera":"blue",
       "Drosophila melanogaster":"red"}
with open("BLAST/input.txt", "r") as file:
    for line in file:
        seq = line.strip('\n')
        filename = "BLAST/output.xml"

        try:
            blast_infile = open(filename, "r")
            print("Using saved file.")
        except:
            print("Performing online BLAST search")
            blastResult = NCBIWWW.qblast("blastn", "nt", seq)
            result = blastResult.read()
            save_file = open(filename, "w")
            save_file.write(result)
            save_file.close()
            blastResult.close()
            blast_infile = open(filename)
            print("Search complete")

        blast_infile = open(filename, "r")
        blast_records = NCBIXML.parse(blast_infile)
        for item in blast_records:
            for key in map:
                if key in item.alignments[0].title:
                    map[key] +=1
                    
                
        blast_infile.close()



for key in map:
    plt.bar(range(len(map)), map[key], 0.5, color=color[key], label=key)
    print(map[key])

plt.xlabel("Organism")
plt.title("Title of Chart")
plt.legend()
plt.show()