import pickle


def save_pickle(target, path: str):
    with open(path, 'wb') as f:
        pickle.dump(target, f)


def load_pickle(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)
