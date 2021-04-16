from os import walk
from os import mknod
import glob
'''
    This code edit by YU-SHUN from NTUT IEM,
    if have any problem, please contact this e-mail: t105370742@ntut.org.tw.
'''


def get_filenames(dir_path, specific_name, isImported=False):
    '''
        This function can find any specific name under the dir_path, even the file inside directories under the path.
        -----
        `specific_name`: 
        --
        >>> Can type any word or extension. 
        e.g. '*cat*', '.csv', '*cat*.csv'
    '''
    specific_name = '/*{}'.format(specific_name)
    filenames = []

    if isImported is True:
        imported_root_ls = read_imported_root_from_txt()
    else:
        imported_root_ls = []

    for root, dirs, file in walk(dir_path):
        load_filenames = glob.glob(root + specific_name)

        if imported_root_ls == ['']:
            if len(load_filenames) == 1:
                filenames.append(load_filenames)
            else:
                filenames.extend(load_filenames)
        else:
            for filename in load_filenames:
                check_num = 0
                for imported_root in imported_root_ls:
                    if(imported_root == filename):
                        check_num = 1
                        break
                if(check_num == 1):
                    continue
                filenames.append(filename)

    return filenames


def read_imported_root_from_txt():
    path = "./already_imported_root.txt"
    try:
        imported_root_info = open(path).read()
    except FileNotFoundError:
        mknod(path)
        imported_root_info = []

    imported_root_ls = seprate_data_item(imported_root_info, ",\n")
    return imported_root_ls


def seprate_data_item(data_item, str_type):
    seprated_ls = data_item.split(str_type)
    return seprated_ls


def write_imported_root_to_txt(filename_root):
    imported_root_info = open("already_imported_root.txt", "r")
    if(imported_root_info.read() == ""):
        imported_root_info = open(
            "already_imported_root.txt", "w", encoding="utf-8")
        imported_root_info.write(str(filename_root))
    else:
        imported_root_info = open(
            "already_imported_root.txt", "a", encoding="utf-8")
        imported_root_info.write(",\n" + str(filename_root))
    imported_root_info.close()


if __name__ == "__main__":
    path = "Data"
    specific_name = ".jpg"
    filenames = get_filenames(path, specific_name, isImported=True)

    for filename in filenames:
        write_imported_root_to_txt(filename)
