import json
import os

from tqdm import tqdm

import json
import os
from tqdm import tqdm


def merge_datasets(input_path, output_path):
    with open(output_path, 'w') as out:
        for query_path, candidate_path in input_path:
            print(query_path)
            print(candidate_path)
            with open(query_path, 'r') as f1:
                with open(candidate_path, 'r') as f2:
                    for query, candidate in tqdm(zip(f1, f2)):
                        query = json.loads(query)
                        candidate = json.loads(candidate)

                        assert str(query['authorIDs']) == str(candidate['authorIDs'])

                        line = json.dumps({'query_id': query['documentID'],
                                           'query_authorID': query['authorIDs'],
                                           'query_text': query['fullText'],
                                           'candidate_id': candidate['documentID'],
                                           'candidate_authorID': candidate['authorIDs'],
                                           'candidate_text': candidate['fullText'],
                                           }, ensure_ascii=False)
                        out.write(line + '\n')




if __name__ == "__main__":
    input_paths = [
        '/shared/3/projects/hiatus/Amazon',
        '/shared/3/projects/hiatus/gmane',
        '/shared/3/projects/hiatus/realnews',
        '/shared/3/projects/hiatus/wiki_discussions',
        '/shared/3/projects/hiatus/Reddit/data',
        '/shared/3/projects/hiatus/BookCorpus',
        '/shared/3/projects/hiatus/wiki'
    ]

    output_path = '/shared/3/projects/hiatus/pretraining/data'

    train_input_paths = [(os.path.join(p, 'train_queries.jsonl'), os.path.join(p, 'train_candidates.jsonl')) for p in
                         input_paths]
    merge_datasets(train_input_paths, os.path.join(output_path, 'train.jsonl'))

    dev_input_paths = [(os.path.join(p, 'dev_queries.jsonl'), os.path.join(p, 'dev_candidates.jsonl')) for p in
                       input_paths]
    merge_datasets(dev_input_paths, os.path.join(output_path, 'dev.jsonl'))

    test_input_paths = [(os.path.join(p, 'test_queries.jsonl'), os.path.join(p, 'test_candidates.jsonl')) for p in
                        input_paths]
    merge_datasets(test_input_paths, os.path.join(output_path, 'test.jsonl'))