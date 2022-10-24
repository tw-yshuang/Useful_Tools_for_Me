import os, shutil
from FileTools.FileSearcher import check2create_dir, get_filenames
from FileTools.WordOperator import replace_keyword


def create_root_txt(dir_path: str):
    for data_type in ['train', 'val', 'test']:
        filenames = get_filenames(f'{dir_path}/{data_type}', '*.jpg')
        # print(filenames)

        if len(filenames) != 0:
            with open(f'{dir_path}/{data_type}.txt', 'w') as f:
                for filename in filenames:
                    f.write(f'{os.path.abspath(filename)}\n')


def symbolic_dir2dir(source_dir: str, target_dir: str):
    for data_type in ['train', 'val', 'test']:
        filenames = get_filenames(f'{source_dir}/{data_type}', '*', withDirPath=False)
        for filename in filenames:
            check2create_dir(f'{target_dir}/{data_type}')
            os.symlink(os.path.abspath(f'{source_dir}/{data_type}/{filename}'), f'{target_dir}/{data_type}/{filename}')


def create_data_yaml(original_path: str, target_path: str):
    shutil.copyfile(original_path, target_path)
    for data_type in ['train', 'val', 'test']:
        replace_keyword(
            target_path,
            target_word=f'{data_type}: *',
            replace_word=f'{data_type}: {"/".join(target_path.split("/")[:-1])}/{data_type}.txt',
        )


if __name__ == '__main__':
    # data_name_suffix = '_DVC'
    task_dir = 'data/coco/coco2014_and_DVC/1007-no6'
    yaml_path = 'data/DVC/1007/test-20_05_06_4_30_10/aa.yaml'

    dir_ls = [
        'data/DVC/1007/test-20_05_06_4_30_10',
        'data/DVC/1007/test-Dan_Far_view',
        'data/DVC/1007/test-Dan_Near_view',
        'data/DVC/1007/test-MTcross_road',
        'data/DVC/1007/test-MTfreeway',
        'data/DVC/1007/test-Tah_subset',
        'data/DVC/1007/test-v0ubset',
        'data/DVC/1007/test-v2ubset',
    ]

    for dir_path in dir_ls:
        target_dir = f'{task_dir}/{dir_path.split("/")[-1]}'

        # check2create_dir(target_dir)
        # symbolic_dir2dir(dir_path, target_dir)
        # symbolic_dir2dir('data/coco/coco2014/no6', target_dir)

        create_data_yaml(yaml_path, f'{target_dir}/sensorFusion.yaml')

        # create_root_txt(target_dir)
