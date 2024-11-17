class TrieNode:
	def __init__(self):
		self.children = {}
		self.words = []

class Trie:
    def __init__(self, keys):
        self.root = TrieNode()
        self.suggestions = []
        self.keys = keys

    def formTrie(self, wordsList):
        i = 1
        for word in wordsList:
            
            self.insert(word[0], word[1])
            # print(i)
            # i += 1

    def insert(self, word, useFrequency):
        # print(word)
        nodeToAddWord = self.travarseAddingNode(self.root, word)
        self.insertWordIntoListByFrequency(nodeToAddWord.words, word, useFrequency)
    
    def travarseAddingNode(self, node, word):
        i = 0
        wordLength = len(word)

        while i < wordLength:
            thisLetter = word[i]
            thisKey = self.keys[thisLetter]

            if thisKey in node.children:
                node = node.children[thisKey]
                i += 1
            else:
                break
            
        while i < wordLength:
            thisLetter = word[i]
            thisKey = self.keys[thisLetter]

            node.children[thisKey] = TrieNode()
            node = node.children[thisKey]
            i += 1
        
        return node
                    
    
    def insertWordIntoListByFrequency(self, wordList, word, useFrequency):
        wordToInsert = [word, useFrequency]
        wordsLength = len(wordList)

        if wordsLength == 0:
            wordList.append(wordToInsert)
            return
        else:
            for i in range(wordsLength):
                comparedFrequency = wordList[i][1]
                insertFrequency = wordToInsert[1]

                if insertFrequency >= comparedFrequency:
                    wordList.insert(i, wordToInsert)
                    return
        

        wordList.append(wordToInsert)
        return


    
    def getSuggestions(self, keyString, suggestionDepth = 0):
        result = []
        node = self.root

        for i in keyString:
            i = int(i)
            if i in node.children:
                node = node.children[i]
            else:
                break
        
        suggestions = node.words

        deepSuggestions = []
        if suggestionDepth > 0:
            self.getDeepSuggestions(node, deepSuggestions)
            deepSuggestions.sort(key=lambda x: x[1], reverse=True)
        return [i[0] for i in suggestions], [i[0] for i in deepSuggestions[:10]]
    

    def getDeepSuggestions(self, node, deepSuggestions):
        for key in node.children.keys():
            if len(node.children[key].words) > 0:
                for word in node.children[key].words:
                    deepSuggestions.append(word)
            self.getDeepSuggestions(node.children[key], deepSuggestions)