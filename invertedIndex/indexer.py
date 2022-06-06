#global

#local
from .map.hashset import Hashset

class InvertedIndexer:

    def __init__(self):
        """
        @property : data
            A dictionary that stores all words from the corupus, their frequency,
            and all document the word appears in.

            ___________

            Signature: { word: Hashset([docId1, docId2, ...]) }
            ___________
            

        """
        self.map = {}
        self.unique_words_count = 0
        self.total_files = 0
        self.total_documents = 0

    def __iter__(self):
        for i in self.map.keys():
            yield i

    def __getitem__(self, key):
        return self.map[key]

    def __contains__(self, key):
        return key in self.map


    def get_data(self):
        return self.map

    def __add_word(self, word : str, documentId : str):
        """
        Adds a word to the index map.
        If the word was already present, then the documentId is stored (no duplicates).
        Otherwise, the word, along with the document it is present in, is added.

        :params word       : word to be added to the index map.
        :params documentId : document the word is present in
        """
        if word == "":
            return

        if word in self.map:
            if documentId not in self.map[word]:
                self.map[word].add(documentId)
            
        else:
            self.map[word] = Hashset()
            self.map[word].add(documentId)

        self.unique_words_count += 1


    def add_sentences(self, sentence : str, documentId : str):
        """
        Gets a sentence as an input, and processes them (any non-alphanumeric character is removed),
        and then stores each word in the sentence in the index map.

        :params sentence    : sentence to extract words from and store those individual words to the
                            index map

        :params documentId  : document the sentence is present in.
        """
        word = ""
        for character in sentence:
            if character.isalnum():
                word += character
            else:
                self.__add_word(word.strip(), documentId)
                word = ""
        