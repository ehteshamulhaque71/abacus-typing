class TrieNode():
	def __init__(self):
		self.children = {}
		self.weight = 0
		self.last = False


class Trie():
	def __init__(self):
		self.root = TrieNode()
		self.suggestions = []

	def formTrie(self, keys):
		for key in keys:
			self.insert(key[0], key[1])

	def insert(self, key, weight):
		node = self.root

		for a in key:
			if not node.children.get(a):
				node.children[a] = TrieNode()

			node = node.children[a]

		node.last = True
		node.weight = weight

	def suggestionsRec(self, node, word):

		if node.last:
			self.suggestions.append([word, node.weight])

		for a, n in node.children.items():
			self.suggestionsRec(n, word + a)

	def getAutoSuggestions(self, key):
		node = self.root
		self.suggestions = []

		for a in key:
			if not node.children.get(a):
				return ['', '', '', '']
			node = node.children[a]

		if not node.children:
			return ['', '', '', '']

		self.suggestionsRec(node, key)
		self.suggestions.sort(key=lambda x: x[1], reverse=True)
		# print(self.suggestions)
		preds = []
		for i in self.suggestions:
			preds.append(i[0])
			if len(preds) == 4:
				return preds
		
		while(len(preds) < 4):
			preds.append('')
		return preds



