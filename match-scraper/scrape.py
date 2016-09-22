import argparse
import pickle
import json
import uuid
import os

from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError


def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """
    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
            # Try Again Once
            if error.error_code in [500]:
                try:
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 400, 404]:
                        return None
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                return None

            # Fatal
            else:
                raise error
    return call_wrapper


def chunks(lst, max_chunk):
    for i in range(0, len(lst), max_chunk):
        yield lst[i:i + max_chunk]


def load_match_ids(match_db):
    try:
        with open(os.path.join(match_db, "index.pkl"), "rb") as in_file:
            mapping = pickle.load(in_file)
            return {id_ for lst in mapping.values() for id_ in lst}
    except FileNotFoundError:
        return set()


def save_matches(match_db, matches, max_chunk):
    with open(os.path.join(match_db, "index.pkl"), "rb") as in_file:
        mapping = pickle.load(in_file)

    for chunk in chunks(matches, max_chunk):
        id_ = uuid.uuid4()
        while id_ in mapping:
            id_ = uuid.uuid4()

        with open(os.path.join(match_db, id_ + ".pkl"), "wb") as out_file:
            pickle.dump(chunk, out_file)

        mapping[id_] = {match.id for match in chunk}

    with open(os.path.join(match_db, "index.pkl"), "wb") as out_file:
        pickle.dump(mapping, in_file)


def read_match_id_file(filepath):
    with open(filepath, "r") as in_file:
        return set(json.load(in_file))


def scrape_matches(match_db, match_ids, max_chunk):
    current_ids = load_match_ids(match_db)
    to_get = read_match_id_file(match_ids)
    to_get = list(to_get - current_ids)

    matches = []
    while len(to_get) > 0:
        id_ = to_get.pop(0)
        match = riotapi.get_match(id_)
        if match:
            matches.append(id_)

        if len(matches) >= max_chunk:
            save_matches(match_db, matches, max_chunk)
            matches = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-key", type=str, required=True, help="API key to use for scraping")
    parser.add_argument("-region", type=str, required=True, help="API region to use for scraping")
    parser.add_argument("-db", type=str, required=False, help="Path to DB folder (default \"matches\")")
    parser.add_argument("-chunk", type=int, required=False, help="Max number of matches per chunk file (default 50)")
    parser.add_argument("-ids", type=str, required=True, help="Path to match id file")
    args = parser.parse_args()

    riotapi.set_region(args.region)
    riotapi.set_api_key(args.key)
    riotapi.print_calls(True)
    riotapi.set_load_policy("lazy")
    riotapi.get_match = auto_retry(riotapi.get_match)

    db = args.db if args.db else "matches"
    chunk = args.chunk if args.chunk else 50

    scrape_matches(db, args.ids, chunk)


if __name__ == "__main__":
    main()
