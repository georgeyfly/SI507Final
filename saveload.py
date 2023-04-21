#######################def function for save and load data######################
import json
import requests
def saveCache(aList, aFile):
    """
    Parameters
    ----------
    aList: list of info

    aFile: a handle of open file

    Returns
    -------
    None

    """
    for i in aList:
        print(i, file=aFile)
def openCache(inFile):
    ''' opens the cache file if it exists and loads the txt
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    inFile: a handle of open file
    
    Returns
    -------
    The opened cache
    '''
    aList = []
    lines = inFile.readlines()
    for line in lines:
        aList.append(line.strip())
    return aList

def save_cache(cache_list, CACHE_FILENAME):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_list: list
    The list to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_list)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def open_cache(CACHE_FILENAME):
    ''' opens the cache file if it exists and loads the JSON into
    the FIB_CACHE dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_list = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_list = [{}]
    return cache_list