#!/bin/env python3


#global
import argparse
import os

#local
from invertedIndex.indexer import InvertedIndexer
from iohandler.reader import read_and_process_data
from iohandler.helpers import save_inverted_index_cache, load_inverted_index_cache
from iohandler.queryprocessor import QueryProcessor

def main(args):
    ii = InvertedIndexer()

    if args.store_words:
        read_and_process_data(os.path.join(args.data_path, "documents_cs"), args.verbose, ii)
        if args.save:
            save_inverted_index_cache(ii, args.verbose, args.inverted_index_cache_path)
        
        if args.verbose:
            print(f"""
            There were
            {ii.unique_words_count} unique words
            {ii.total_files} total files
            {ii.total_documents} total documents
            """)

    if args.evaluate_queries:
        if not args.store_words:
            ii = load_inverted_index_cache(args.inverted_index_cache_path, args.verbose)
        qp = QueryProcessor(ii, args.verbose)
        qp.process_queries(os.path.join(args.data_path, "queries_cs.xml"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--store_words",
        action="store_true",
        default=True,
        help="Store words from the xml files")
    parser.add_argument(
        "-sw", "--save",
        action="store_true",
        help="save words after processing them"
    )
    parser.add_argument(
        "-q", "--evaluate_queries",
        action="store_true",
        default=True,
        help="Evaluate queries from the xml file")
    parser.add_argument(
        "-ip", "--inverted_index_cache_path",
        action="store",
        default="bin/inverted-index-cache",
        type=str,
        help="Path the inverted index map is stored in")
    parser.add_argument(
        "-dp", "--data_path",
        action="store",
        default="A2/",
        type=str,
        help="Path the xml document to store words from are")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="get a summary of what's going on while the program is running"
    )

    main(parser.parse_args([] if "__file__" not in globals() else None))