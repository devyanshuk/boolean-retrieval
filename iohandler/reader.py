#global
from lxml import etree
from pathlib import Path

#local
from invertedIndex.indexer import InvertedIndexer

def process_doc(document, ii : InvertedIndexer):
    """
    Given the root of the xml document (DOC), process three of it's
    children, namely TITLE, TEXT and HEADING (add them to the inverted
    index map).

    :params document : root element of an xml file (marked by <DOC>)
    """
    document_id = document.find("DOCID").text
    titles = document.findall("TITLE")
    texts = document.findall("TEXT")
    headings = document.findall("HEADING")

    for title in titles:
        ii.add_sentences(title.text, document_id)

    for text in texts:
        ii.add_sentences(text.text, document_id)

    for heading in headings:
        ii.add_sentences(heading.text, document_id)


def read_and_process_data(PATH, verbose, ii : InvertedIndexer):
    """
    Use glob pattern to match all xml files in the specified directory, and process them.

    :params PATH : directory all the xml and the dtd files are present in.
    :params ii   : inverted index map to store the word -> document results in.
    """
    lxml_parser = etree.XMLParser(load_dtd=True, resolve_entities=False, recover=True)

    for path in Path(PATH).glob("*.xml"):
        if verbose : print(f"reading from {path}...")
        tree = etree.parse(path, parser=lxml_parser)
        
        for doc in tree.getroot().findall("DOC"):
            process_doc(doc, ii)
            ii.total_documents += 1

        if verbose : print(f"finished reading from {path}, stored all words")
        ii.total_files += 1