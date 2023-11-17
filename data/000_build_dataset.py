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



def data_merge(output_path: str):
    print("Merging train data")
    train_input_paths = [(os.path.join(p, 'train_queries.jsonl'), os.path.join(p, 'train_candidates.jsonl')) for p in [output_path]]
    merge_datasets(train_input_paths, os.path.join(output_path, 'train.jsonl'))

    print("Merging dev data")
    dev_input_paths = [(os.path.join(output_path, 'dev_queries.jsonl'), os.path.join(output_path, 'dev_candidates.jsonl')) for p in [output_path]]
    merge_datasets(dev_input_paths, os.path.join(output_path, 'dev.jsonl'))

    print("Merging test data")
    test_input_paths = [(os.path.join(output_path, 'test_queries.jsonl'), os.path.join(output_path, 'test_candidates.jsonl')) for p in [output_path]]
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


    input_base_path = '/shared/3/projects/hiatus/hrs_hua/hrs1_08_14'
    hrs_release_08 = [
        'hrs1_08-14-23_background_bgg_350_anonymized.jsonl',
        'hrs1_08-14-23_background_globalvoices_anonymized.jsonl',
        'hrs1_08-14-23_background_instructables_anonymized.jsonl',
        'hrs1_08-14-23_background_stackexchange_literature_anonymized.jsonl',
        'hrs1_08-14-23_background_stackexchange_stem_anonymized.jsonl',
        'hrs1_08-14-23_boardgamegeek_foreground_anonymized.jsonl',
        'hrs1_08-14-23_globalvoices_foreground_anonymized.jsonl',
        'hrs1_08-14-23_instructables_foreground_anonymized.jsonl',
        'hrs1_08-14-23_stackexchangehumanities_foreground_anonymized.jsonl',
        'hrs1_08-14-23_stackexchangestem_foreground_anonymized.jsonl']
    hrs_release_08_names = [
        'background_bgg_350',
        'background_globalvoices',
        'background_instructables',
        'background_stackexchange_literature',
        'background_stackexchange_stem',
        'boardgamegeek_foreground',
        'globalvoices_foreground',
        'instructables_foreground',
        'stackexchangehumanities_foreground',
        'stackexchangestem_foreground'
    ]


    for i in range(len(hrs_release_08)):
        hrs_file = hrs_release_08[i]
        output_name = hrs_release_08_names[i]

        ### Set dirs.
        input_file = os.path.join(input_base_path,'raw_data', hrs_file)
        output_path = os.path.join(input_base_path, 'generated_data', output_name)
        create_path(output_path)
        print("Input file path:", input_file)
        print("Output file path:", output_path)

        ### Four steps to generate the datasets.
        data_partition(input_file, output_path)
        data_align(output_path)
        data_merge(output_path)
        data_convert_to_data(output_path)



if __name__ == "__main__":
    main()
