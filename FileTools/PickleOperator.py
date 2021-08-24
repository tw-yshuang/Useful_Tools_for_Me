import pickle


def save_pickle(targect, path: str):
    with open(path, 'wb') as f:
        pickle.dump(targect, f)


def load_pickle(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)
