#global
from lxml import etree
import os

#local
from invertedIndex.indexer import InvertedIndexer
from invertedIndex.map.hashset import Hashset

class QueryProcessor:

    AND     = "AND"
    OR      = "OR"
    NOT     = "NOT"
    AND_NOT = "AND NOT"

    OPERATORS  = {
        NOT     : 2,
        AND_NOT : 1,
        AND     : 0,
        OR      : 0
    }

    OP_FUNC = {
        AND     : lambda x, y  : x.intersection(y),
        OR      : lambda x, y  : x.union(y),
        AND_NOT : lambda x, y  : x.and_not(y)
    }

    def __init__(self, ii : InvertedIndexer, verbose : bool):
        self.ii = ii
        self.verbose = verbose

    def __convert_postfix(self, array):
        """
        Given a query (as a list of indiviual query fragments), represented by an indix order,
        convert it to postfix form which will then later on be used to evaluate it.

        :params array : an infix representation of the query with each fragments being a part of list.
        """
        postfix_stack = []
        word_postfix_stack = []
        operator_stack = []
        i = 0
        while i < len(array): 
            elem = array[i].strip()
            if not elem in self.OPERATORS:
                postfix_stack.append(Hashset() if not elem in self.ii else self.ii[elem])
                word_postfix_stack.append(elem)
            else:
                if elem == self.AND and array[i+1] == self.NOT:
                    elem = self.AND_NOT 
                    i += 1
                while operator_stack != [] and self.OPERATORS[elem] >= self.OPERATORS[operator_stack[-1]]:
                        op = operator_stack.pop()
                        postfix_stack.append(op)
                        word_postfix_stack.append(op)
                operator_stack.append(elem)
            i += 1

        while operator_stack != []:
            op = operator_stack.pop()
            postfix_stack.append(op)
            word_postfix_stack.append(op)

        if self.verbose : print(f"Query in postfix : {' '.join(word_postfix_stack)}")
        return postfix_stack


    def __eval_postfix(self, postfix):
        """
        Given a postfix representation of a query, evaluate them one by one, utilizing the
        OP_FUNC fictionary that returns a anonymous function.

        :params : list representing postfix of a query.
        """
        res_stack = []
        for elem in postfix:
            if isinstance(elem, Hashset):
                res_stack.append(elem)
            elif elem in self.OPERATORS:
                item1 = res_stack.pop()
                item2 = res_stack.pop()
                res_stack.append(self.OP_FUNC[elem](item2, item1))
        return res_stack.pop()

    def __process_single_query(self, document):
        """
        Given a xml 'top' element, extract 'query' from it and process
        that query. A query might look like this:
            word1 AND word2 OR word3
        
        :params document : a xml 'top' element from queries_cs.xml file
        """
        query = document.find("query").text
        if self.verbose : print(f"Query in infix : {query}")
        postfix = self.__convert_postfix(query.split())
        return self.__eval_postfix(postfix)

    def __save_result(self, result, file, base="bin"):
        """
        Given a result (a Hashset), and a file to store the result to,
        store it one per a line.

        :params result : result of the postfix evaluation (Hashset).
        :params file   : file to store the result to.
        :params base   : base directory of the file.
        """

        file_path = os.path.join(base, file)

        if not os.path.isdir(base):
            if self.verbose : print(f"Making a new directory : {base}")
            os.mkdir(base)

        subdir = os.path.split(file_path)[0]
        if not os.path.isdir(subdir):
            if self.verbose : print(f"Making a new directory : {subdir}")
            os.mkdir(subdir)

        with open(file_path, "w") as inp:
            for item in result:
                inp.write(item.key)
                inp.write("\n")
        if self.verbose: print(f"Finished storing query results at {file_path}")
    
    def process_queries(self, PATH : str):
        """
        Given a path to the queries_cs.xml file, extract all the elements marked by the key
        'top', and 'num' and use this element to extract 'query' and process them one by one.

        :params PATH : path to queries_cs.xml file.
        """
        lxml_parser = etree.XMLParser(load_dtd=True, resolve_entities=False, recover=True)
        tree = etree.parse(PATH, parser=lxml_parser)
        
        for doc in tree.getroot().findall("top"):
            result = self.__process_single_query(doc)
            if self.verbose : print(f"{result.size} documents found for the query")
            num = doc.find("num").text
            self.__save_result(result, num)
