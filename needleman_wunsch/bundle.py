import sys
from ruler import Ruler

def main(file_name):
    """Fonction qui s'effectuera lorsque l'on lance ce script"""
    f = open(file_name, "r")
    content = f.read()
    tab_lines0 = content.split('\n') #Sépare selon les lignes
    tab_lines = []
    for line in tab_lines0:
        if line != "":
            tab_lines.append(line) #On retire les lignes vides
    for i in range(0, len(tab_lines) - 1, 2):
        ruler = Ruler(tab_lines[i], tab_lines[i+1])
        ruler.compute()
        d = ruler.distance
        top, bottom = ruler.report()
        print("====== Comparaison # " + str(i//2 + 1) +" - distance = " + str(d))
        print(top)
        print(bottom)
    f.close()

main(sys.argv[1])