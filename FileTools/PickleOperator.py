import pickle


def save_pickle(target, path: str):
    '''
    This function saves a Python object as a binary file using the pickle module.

    Args:
        `target`: The object that needs to be saved as a pickle file.

        `path` (str): A string that represents the file path where the pickled object will be saved.
    '''
    with open(path, 'wb') as f:
        pickle.dump(target, f)


def load_pickle(path: str):
    '''
    The function loads a pickle file from a given path and returns its contents.

    Args:
        `path` (str): A string that represents the file path of the pickle file that needs to be loaded.

    Returns:
        The function `load_pickle` is returning the object that was loaded from the pickle file located at the specified `path`.
    '''
    with open(path, 'rb') as f:
        return pickle.load(f)
