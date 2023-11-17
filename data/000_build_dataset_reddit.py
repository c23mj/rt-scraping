import os
from partition import partition
from align import align
from merge import merge_datasets
from convert_to_datasets import create_dataset


def create_path(path: str):
    """Creates path if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created the path: {path}")



def data_partition(input_file: str, output_path: str):
    nrows = 1000000  # None to use the whole file
    partition(input_file, output_path, nrows)



def data_align(output_path: str):
    print("Aligning dev dataset!")
    align(os.path.join(output_path, 'dev_candidates.jsonl'), os.path.join(output_path, 'dev_queries.jsonl'))

    print("Aligning test dataset!")
    align(os.path.join(output_path, 'test_candidates.jsonl'), os.path.join(output_path, 'test_queries.jsonl'))

    print("Aligning train dataset!")
    align(os.path.join(output_path, 'train_candidates.jsonl'), os.path.join(output_path, 'train_queries.jsonl'))



def data_merge(innput_path: str, output_path: str):
    print("Merging train data")
    train_input_paths = [(os.path.join(p, 'train_queries.jsonl'), os.path.join(p, 'train_candidates.jsonl')) for p in [innput_path]]
    merge_datasets(train_input_paths, os.path.join(output_path, 'train.jsonl'))

    print("Merging dev data")
    dev_input_paths = [(os.path.join(p, 'dev_queries.jsonl'), os.path.join(p, 'dev_candidates.jsonl')) for p in [innput_path]]
    merge_datasets(dev_input_paths, os.path.join(output_path, 'dev.jsonl'))

    print("Merging test data")
    test_input_paths = [(os.path.join(p, 'test_queries.jsonl'), os.path.join(p, 'test_candidates.jsonl')) for p in [innput_path]]
    merge_datasets(test_input_paths, os.path.join(output_path, 'test.jsonl'))    



def data_convert_to_data(output_path: str):
    print('Creating training dataset...')
    train_inpath = os.path.join(output_path, 'train.jsonl')
    train_outpath = os.path.join(output_path, 'train')
    create_dataset(train_inpath, train_outpath)

    print('Creating dev dataset...')
    dev_inpath = os.path.join(output_path, 'dev.jsonl')
    dev_outpath = os.path.join(output_path, 'dev')
    create_dataset(dev_inpath, dev_outpath)

    print('Creating test dataset...')
    test_inpath = os.path.join(output_path, 'test.jsonl')
    test_outpath = os.path.join(output_path, 'test')
    create_dataset(test_inpath, test_outpath)




def main():


    reddit_data_input_path = '/shared/3/projects/hiatus/reddit'
    reddit_data_output_path = '/shared/3/projects/hiatus/hrs_hua/reddit'

    ### Given existing [train_candidates.jsonl, train_queries.jsonl, dev_candidates.jsonl, dev_queries.jsonl, test_candidates.jsonl, test_queries.jsonl]
    ### We only need step3 , step4 for merge and convert.

    
    data_merge(reddit_data_input_path, reddit_data_output_path)
    data_convert_to_data(reddit_data_output_path)



if __name__ == "__main__":
    main()
