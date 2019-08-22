
class TrieNode:
    def __init__(self):
        self.children = [None ] *27
        self.item = 0
        self.maxfrequency = -1
        self.nextindex =-1
        self.word = None
        self.definition = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def index(self, char):
        return ord(char) - ord('a')

    def insert(self, string, frequency, definition):
        # insert from the root
        node = self.root

        for char in range(len(string)):
            index = self.index(string[char])

            if node.children[index] is not None:
                # print("old: ", index)
                # print(frequency, "node max freq: ", node.maxfrequency)

                # while inserting, check whether the current frequency is bigger
                # if yes, replace the max
                if frequency > node.maxfrequency:
                    node.maxfrequency = frequency
                    # print("max freq2: ",node.maxfrequency)

                    # then save the index holding the max
                    node.nextindex = index

                # also check when there is same frequency as the current max
                elif frequency == node.maxfrequency:
                    if node.nextindex > index:
                        node.nextindex = index
                        # print("next index: ",node.nextindex)
                # print("max freq: ",node.maxfrequency)

                # keep track of total number of children
                node.item += 1

                # move the node to the next
                node = node.children[index]


            # else if node containing char doesnt exist
            # create a new node and move to it
            else:
                # print("new: ", index)
                # print(frequency)
                # print()
                node.children[index] = TrieNode()

                # same condition as existing node above
                if frequency > node.maxfrequency:
                    node.maxfrequency = frequency
                    node.nextindex = index
                elif frequency == node.maxfrequency:
                    if node.nextindex > index:
                        node.nextindex = index
                node.item += 1
                node = node.children[index]

        # create a node at the last slot of the array as indicator of end of the word
        node.children[-1] = TrieNode()

        # save the word and definition at the last node
        node.word = string
        node.maxfrequency = frequency
        node.definition = definition

        # add the item also when the prefix is a word
        node.item += 1

    def autocomplete(self, prefix):

        node = self.root

        # the loop is to move the pointer to the last node of the prefix entered
        for char in prefix:
            index = self.index(char)

            if node.children[index] is not None:
                node = node.children[index]
            else:
                # if unable to do so then means the prefix doesnt exist
                return False
        previous = node

        while True:
            # keep moving the node until it found the last node

            if node.nextindex >= 0:
                node = node.children[node.nextindex]

            # the node.children[-1] will always be None when nothing is created to store the information
            # only the last node contains the word and definition stored inside a node
            elif node.children[-1] is not None:
                break
            else:
                node = node.children[node.nextindex]

        # then return the info stored at the last node
        return node.word, node.maxfrequency, previous.item, node.definition

'''    def print_trie(self):
        node = self.root
        print("root letter: ", node.maxfrequency, node.nextindex)
        for i in range(27):
            if node.children[i] is not None:
                print("first letter: ", i, node.children[i].maxfrequency, node.children[i].nextindex)
        node = node.children[1]
        for i in range(27):
            if node.children[i] is not None:
                print("second letter: ", i, node.children[i].maxfrequency, node.children[i].nextindex)
        node = node.children[4]
        for i in range(27):
            if node.children[i] is not None:
                print("third letter: ", i, node.children[i].maxfrequency, node.children[i].nextindex)
        node = node.children[0]
        for i in range(27):
            if node.children[i] is not None:
                print("fourth letter: ", i, node.children[i].maxfrequency, node.children[i].nextindex)
        node = node.children[18]
        for i in range(27):
            if node.children[i] is not None:
                print("fifth letter: ", i, node.children[i].maxfrequency, node.children[i].nextindex)'''


t = Trie()
# t.insert("advantage", 1600, "def 1")
#t.insert("beast", 720, "def 2")
#t.insert("best", 720, "def 3")
#t.insert("beat", 100, "def 4")
# t.insert("acenture", 696, "def 5")
# t.insert("advoyer", 109, "def 6")
# t.insert("advantageable", 1500, "def 7")


read_dict = open("bigger_dictionary.txt", "r")

for line in read_dict:

    if line.strip():
        line1 = line.rstrip()
        segments = line1.split(':',1)
        if segments[0] == 'word':
            word = segments[1].strip()
        if segments[0] == 'frequency':
            freq = int(segments[1])
        if segments[0] == 'definition':
            defn = segments[1].strip()
            t.insert(word, freq, defn)

user_prefix = input("Enter a prefix: ")

# keep looping until user enter *** to quit the program
while user_prefix != "***":

    if t.autocomplete(user_prefix) == False:
        print("There is no word in the dictionary that has [",user_prefix,"] as a prefix.")
    else:
        word, freq, numword, definition = t.autocomplete(user_prefix)
        print("Auto-complete suggestions: ",word,"\nDefinition: ",definition,"\nThere are ", numword, " words in the dictionary that have [",user_prefix,"] as a prefix.")

    user_prefix = input("Enter a prefix: ")