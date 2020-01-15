from string import ascii_lowercase
from time import perf_counter as clock

text = "a dead dad ceded a bad babe a beaded abaca bed"

class DictOfPiles():

    """Dictionnaire de piles, indicée par des entiers naturels. Permet de rapidement construire l'arbre de Huffman."""

    def __init__(self):
        self.dict = {}
        self.size = 0

    def add(self, key, value):
        """Ajoute à la pile indicée par key l'élément value."""
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]
        self.size += 1

    def pop(self, key):
        """Renvoie l'élément haut dessus de la pile indicée par key et le supprime. Si la pile est vide après l'opération, on la supprime."""
        try:
            value = self.dict[key].pop()
            if self.dict[key] == []:
                self.dict.pop(key)
            self.size -= 1
            return value
        except:
            ValueError("La pile " + str(key) + " n'existe pas.")

    def is_empty(self):
        """Renvoie True si aucune pile n'existe."""
        return self.dict == {}

    def is_singleton(self):
        """Renvoie True si il n'y a qu'une seule pile à un élément."""
        return self.size == 1

    def min(self):
        """Renvoie le minimum des indices des piles si celui-ci existe."""
        if self.is_empty():
            raise ValueError("Empty DictOfPiles")
        else:
            return min(self.dict.keys())

    def pop_min(self):
        """Effectue un pop sur la pile dont l'indice est le plus petit"""
        try:
            return self.pop(self.min())
        except:
            TypeError("Ce dictionnaire de pile est vide.")

    def __repr__(self):
        return self.dict.__repr__()


class Node():

    def __init__(self, tag, left = None, right = None):
        """Crer une feuille si on ne donne pas des fils à gauche ou à droite, créer un noeud sinon."""
        self.tag = tag
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left == None and self.right == None:
            return self.tag.__repr__()
        else:
            return "(" + self.tag.__repr__() + ', ' + self.left.__repr__() + ', ' + self.right.__repr__() + ')'


class TreeBuilder():

    def __init__(self, txt):
        self.letters = {}
        self.count(txt)

    def count(self, txt):
        """Compte le nombre d'apparition d'une lettre dans un texte et le stocke dans un dictionnaire."""
        alphabet = set()
        for letter in txt:
            alphabet.add(letter)
        for char in alphabet:
            score = 0
            for letter in txt:
                if letter == char:
                    score += 1
            if score != 0:
                self.letters[char] = score

    def get_score(self, data):
        """Renvoie le socre d'une Node, en séparant le cas où c'est une feuille de celui où le Node a des fils."""
        if isinstance(data, int):
            return data
        else:
            return data[1]

    def tree(self):
        """Construit l'arbre en utilisant un dictionnaire de pile qui contient les Nodes dans une pile indicée par leur score. La construction cmmence en ajoutant toutes les feuilles a ce dictionnaire et fini lorsqu'il ne reste qu'une Node, qui est l'arbre tout entier."""
        scores = DictOfPiles()
        for letter in self.letters:
            score = self.letters[letter]
            scores.add(score, Node((letter, score)))
        while not(scores.is_singleton()):
            node1 = scores.pop_min()
            node2 = scores.pop_min()
            score = self.get_score(node1.tag) + self.get_score(node2.tag)
            new_node = Node(score, node1, node2)
            scores.add(score, new_node)
        return scores.pop_min()


class Codec():

    def __init__(self, tree):
        self.encoder = {}
        self.decoder = {}
        self.build(tree)

    def build(self, og_tree):
        """Construit un codeur et un décodeur à partir d'un arbre de Huffman, tous deux des dictionnaires qui font correspondre un caractère et son code."""
        def aux(tree, code):
            if isinstance(tree.tag, int):
                aux(tree.left, code + '0')
                aux(tree.right, code + '1')
            else:
                self.encoder[tree.tag[0]] = code
                l_code = len(code)
                if l_code in self.decoder.keys():
                    self.decoder[l_code][code] = tree.tag[0]
                else:
                    self.decoder[l_code] = {code : tree.tag[0]}
        aux(og_tree, '')

    def encode(self, txt):
        coded = ''
        for char in txt:
            try:
                coded += self.encoder[char]
            except:
                raise ValueError('Le caractère ' + char +" n'est pas présent dans ce codage.")
        return coded

    def decode(self, coded):
        decoded = ''
        tampon = ''
        l_tampon = 0
        code_length = set(self.decoder.keys())
        min_length, max_length = min(code_length), max(code_length)
        for bit in coded:
            tampon += bit
            l_tampon += 1
            if l_tampon >= min_length:
                if l_tampon in code_length:
                    if tampon in self.decoder[l_tampon]:
                        decoded += self.decoder[l_tampon][tampon]
                        tampon = ''
                        l_tampon = 0
            elif l_tampon > max_length:
                raise ValueError("Ce caractère n'est pas présent dans le codage.")
        return decoded

    def encode_bin(self, txt):
        """Codage en bytes: à part la conversion, l'autre étapde est de s'assurer que le texte que l'on code a une longueur multiple de 8."""
        coded = self.encode(txt)
        self.pad = 8 - (len(coded) % 8)
        coded += '0' * self.pad
        bin_code = bytearray()
        for i in range(0, len(coded), 8):
            bin_code.append(int(coded[i : i + 8], 2))
        return bin_code

    def decode_bin(self, code_bin):
        """Fait la conversion inverse, en retirant le padding avant d'appeler la fonction .decode()."""
        coded = ''
        for bit in code_bin:
            coded += '{:0>8}'.format(bin(bit)[2:])
        coded = coded[:(len(coded) - self.pad)]
        return self.decode(coded)


def timed_coding(text):
    """Fonction de diagnostic. Permet de voir si le codage fonctionne, et en combien de temps. Les temps sont en pourcentages du temps total pour chaque étape."""
    time0 = clock()
    t = TreeBuilder(text)
    tree = t.build_tree()
    time1 = clock()
    c = Codec(tree)
    time2 = clock()
    coded = c.encode_bin(text)
    time3 = clock()
    decoded = c.decode_bin(coded)
    time4 = clock()
    total_time = time4 - time0
    print("Construction de l'arbre:", (time1 - time0) / total_time)
    print("Construction du codec :", (time2 - time1) / total_time)
    print("Codge :", (time3 - time2) / total_time)
    print("Decodge :", (time4 - time3) / total_time)
    return decoded == text, len(coded) / len(text), total_time