#global
import pickle
import jsonpickle
import lzma
import os
import json
import time

#local
from invertedIndex.indexer import InvertedIndexer

def save_inverted_index_cache(ii : InvertedIndexer, verbose : bool, name : str):
    """
    Given the word -> document cache and a file name, store the invertex index
    map as a pickle file, which could later on be loaded without having to store
    words in the cache again.

    :params ii   : invertex index map of all documents.
    :params name : name of the file to store the cache in.
    """
    root = os.path.split(name)[0]
    if not os.path.isdir(root):
        if verbose : print(f"{root} directory does not exist. Making a new one")
        os.mkdir(root)

    #######

        # takes about 23 minutes to save it as a json file. also takes up > 1.5GB.
        # TOO INEFFICIENT.

    #######

    # print("saving as json...")
    # curr = time.time() 
    # with open("bin/cache.json", "w") as file:
    #     file.write(jsonpickle.encode(ii))
    # print(f"Time jsonpickle took to complete : {((time.time() - curr) / 60):.1f} minutes")


    ######

        # takes about 14 minutes to save the contents, and takes up about 56MB, with
        # highest protocol mode turned on while saving the file. Way better than jsonpickle
        # in terms of size, but the save time is still not the best.

    ######


    if verbose : print("saving as pickle... Should take about 15 minutes")
    curr = time.time()    
    with lzma.open(name, "wb") as cache_file:
        pickle.dump(ii, cache_file, pickle.HIGHEST_PROTOCOL)
    if verbose : print(f"minutes pickle took to complete : {((time.time() - curr) / 60):.1f} minutes")

    


def load_inverted_index_cache(name : str, verbose : bool):
    """
    Given a filename, load the pickled contents (invertex index cache).

    :params name : name of the file to load the cache from as an InvertedIndexer object.
    """

    #####

        # Takes about 2.8 minutes to load the cached dictionary to memory (on average)

    #####
    if verbose : print("loading the inverted index cache...Should take about 3 minutes")
    curr = time.time()
    with lzma.open(name, "rb") as cache_file:
        ii = pickle.load(cache_file)
    if verbose : print(f"Time pickle took to complete loading the file : {((time.time() - curr) / 60):.1f} minutes")
    return ii