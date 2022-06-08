import argparse
from typing import Dict, List

from dblp_fetcher.find_new_entries import parse_bibtex_file, normalize_title, print_candidates


def compare_publication_lists(db1: List[Dict], db2: List[Dict]):
    print("In first list, but not in second:\n")
    entry_in_first_but_not_second(db1, db2)

    print("\n--------------------------------------------------\n")
    print("In second list, but not in first:\n")
    entry_in_first_but_not_second(db2, db1)

    print("\n--------------------------------------------------\n")
    print("In both lists, but different:\n")
    entry_in_both(db1, db2)


def entry_in_first_but_not_second(db1: List[Dict], db2: List[Dict]):
    titles_in_2 = get_normalized_titles(db2)

    in_first_but_not_second = list(
        filter(lambda entry: "title" in entry and normalize_title(entry["title"]) not in titles_in_2, db1)
    )
    print_candidates(in_first_but_not_second)


def get_normalized_titles(db):
    return set(
        map(
            lambda entry: normalize_title(entry["title"]),
            filter(lambda entry: "title" in entry, db)
        )
    )


def entry_in_both(db1: List[Dict], db2: List[Dict]):
    normalize_title_to_entry_in_2 = {}
    for entry_in_2 in db2:
        if "title" in entry_in_2:
            normalize_title_to_entry_in_2[normalize_title(entry_in_2["title"])] = entry_in_2

    for entry_in_1 in db1:
        normalized_title = normalize_title(entry_in_1["title"])
        if "title" in entry_in_1 and normalized_title in normalize_title_to_entry_in_2:
            entry_in_2 = normalize_title_to_entry_in_2[normalized_title]
            print_candidates([entry_in_1, entry_in_2])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare two publication lists.')
    parser.add_argument(dest="list1", help='the first list')
    parser.add_argument(dest="list2", help='the second list')

    args = parser.parse_args()
    list1, list2 = args.list1, args.list2

    db1 = parse_bibtex_file(list1)
    db2 = parse_bibtex_file(list2)

    compare_publication_lists(db1, db2)
