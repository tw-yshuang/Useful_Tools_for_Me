'''
    This code edit by YU-SHUN,
    Welcome to contact me if you have any questions.
    e-mail: tw.yshuang@gmail.com
    Github: https://github.com/tw-yshuang
'''

import os, glob
import subprocess
from typing import List

from WordOperator import str_format


def get_filenames(dir_path: str, specific_name: str, withDirPath=True) -> List[str]:
    '''
    get_filenames
    -----
    This function can find any specific name under the dir_path, even the file inside directories.

    specific_name:
        >>> Can type any word or extension.
        e.g. '*cat*', '*.csv', '*cat*.csv',
    '''

    if dir_path[-1] != '/':
        dir_path += '/'

    filenames = glob.glob(f'{dir_path}**/{specific_name}', recursive=True)

    if '*.' == specific_name[:2]:
        filenames.extend(glob.glob(f'{dir_path}**/{specific_name[1:]}', recursive=True))

    if withDirPath is False:
        dir_path_len = len(dir_path)
        filenames = [filename[dir_path_len:] for filename in filenames]

    return filenames


def check2create_dir(dir: str):
    '''
    This function checks if a directory exists and creates it if it doesn't.

    Args:
        `dir` (str): A string that represents the directory path that needs to be
    checked and created if it does not exist.

    Returns:
        a boolean value. If the directory already exists, it returns True. If the directory does not exist
    and is successfully created, it returns False.
    '''
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            print(str_format(f"Successfully created the directory: {dir}", fore='g'))
            return False
        else:
            return True
    except OSError:
        raise OSError(str_format(f"Fail to create the directory {dir} !", fore='r'))


def get_dir_size_py(path: str = '.'):  # slow way
    '''
    The function calculates the total size of a directory in kilobytes by iterating through all files
    and directories within it.

    Args:
        `path` (str): The path to the directory for which we want to get the size. By default, it is set to
    the current directory ('.').

    Returns:
        the size of the directory in kilobytes as an integer.
    '''
    total_size = 0.0

    for root, dirs, files in os.walk(path, onerror=StopIteration):
        if len(files) == 0:
            continue

        for file in files:
            fp = os.path.join(root, file)
            # skip if it is symbolic link
            if os.path.islink(fp):
                total_size += os.lstat(fp).st_size
            else:
                total_size += os.path.getsize(fp)
    return total_size // 1024  # kilobytes as an integer


def get_dir_size_unix(path: str = '.'):  # faster way
    '''
    This function returns the size of a directory in kilobytes using the Unix command "du".

    Args:
        `path` (str): The path to the directory for which we want to get the size. By default, it is set to
    the current directory ('.').

    Returns:
        the size of the directory in kilobytes as an integer.
    '''
    return int(
        subprocess.run(['du', '-sk', path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8').stdout.split()[0]
    )


get_dir_size = get_dir_size_py  # general used but slow than get_dir_size_unix
