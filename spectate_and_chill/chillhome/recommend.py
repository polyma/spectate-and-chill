import numpy as np
import pickle
import sys
import os
import argparse
from sklearn import manifold
from sklearn.neighbors import KDTree

from cassiopeia import riotapi, baseriotapi


NUM_COMPONENTS = 30
LEAF_SIZE = 20
METRIC = "euclidean"
REQUIRED = {"id", "region"}


def summoner_masteries_from_cass(summoner_id):
    return [x.__dict__ for x in baseriotapi.get_champion_masteries(summoner_id)]


def get_summoner(summoner_id, region):
    return {"id": summoner_id, "region": region, "masteries": summoner_masteries_from_cass(summoner_id)}


def get_mastery_vector(champion_indexes, summoner_masteries):
    vector = np.zeros(len(champion_indexes), dtype=np.float)
    for mastery in summoner_masteries:
        vector[champion_indexes.index(mastery["championId"])] = mastery["championPoints"]
    return normalize(vector, norm="max")


def normalize(vector, norm="max"):
    vector = vector.astype(np.float)

    if norm == "max":
        vector = np.subtract(vector, vector.min())
        dividend = vector.max()
    elif norm == "l1":
        dividend = np.linalg.norm(vector, ord=1)
    elif norm == "l2":
        dividend = np.linalg.norm(vector, ord=2)
    vector = np.divide(vector, dividend)
    return vector


class Recommender(object):
    def train(self, general_summoners, streamer_summoners):
        self._champion_indexes = sorted([champion.id for champion in riotapi.get_champions()])

        data = np.zeros((len(general_summoners), len(self._champion_indexes)), dtype=np.float)
        for i, row in enumerate(map(lambda x: get_mastery_vector(self._champion_indexes, x["masteries"]), general_summoners)):
            data[i] = row

        self._projection = manifold.LocallyLinearEmbedding(n_components=NUM_COMPONENTS)
        self._projection.fit(data)
        self._update_streamer_tree(streamer_summoners)

    def _update_streamer_tree(self, streamer_summoners):
        points = np.zeros((len(streamer_summoners), NUM_COMPONENTS), dtype=np.float)
        for i, row in enumerate(map(lambda x: get_mastery_vector(self._champion_indexes, x["masteries"]), streamer_summoners)):
            points[i] = self._projection.transform(row)

        self._streamer_tree = KDTree(points, leaf_size=LEAF_SIZE, metric=METRIC)
        self._streamer_index = list()
        for s in streamer_summoners:
            s = dict(s)
            to_remove = set()
            for key in s:
                if key not in REQUIRED:
                    to_remove.add(key)
            for key in to_remove:
                del s[key]
            self._streamer_index.append(s)

    def to_file(self, filepath):
        with open(filepath, "wb") as out_file:
            pickle.dump(self._champion_indexes, out_file)
            pickle.dump(self._projection, out_file)
            pickle.dump(self._streamer_tree, out_file)
            pickle.dump(self._streamer_index, out_file)

    @staticmethod
    def from_file(filepath):
        with open(filepath, "rb") as in_file:
            rec = Recommender()
            rec._champion_indexes = pickle.load(in_file)
            rec._projection = pickle.load(in_file)
            rec._streamer_tree = pickle.load(in_file)
            rec._streamer_index = pickle.load(in_file)
            return rec

    def recommend(self, summoner, champion_masteries, num_recommendations=12):
        if num_recommendations > len(self._streamer_index):
            num_recommendations = len(self._streamer_index)

        mastery_vector = get_mastery_vector(self._champion_indexes, champion_masteries)
        projection = self._projection.transform(mastery_vector)
        neighbors = self._streamer_tree.query(projection, k=num_recommendations, return_distance=True)

        distances = neighbors[0]
        indexes = neighbors[1]

        return [
            {
                "id": self._streamer_index[index]["id"],
                "region": self._streamer_index[index]["region"],
                "score": distances[0][i]
            }
            for i, index in enumerate(indexes[0])
        ]


def setup_cass():
    riotapi.set_load_policy("lazy")
    riotapi.set_rate_limit(25000, 10)
    riotapi.set_data_store(None)
    riotapi.set_api_key(os.environ["API_KEY"])
    riotapi.set_region("NA")
    riotapi.print_calls(True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-general", type=str)
    parser.add_argument("-streamers", type=str)
    parser.add_argument("-model", type=str)
    parser.add_argument("-train", action="store_true")
    parser.add_argument("-update", action="store_true")
    parser.add_argument("-summoner", type=str)
    parser.add_argument("-region", type=str)
    parser.add_argument("-recs", type=int)
    args = parser.parse_args()

    setup_cass()

    if not args.model:
        args.model = "model.pkl"

    if args.train and args.update:
        print("Pick train or update")
        sys.exit(1)

    if args.train:
        if not args.general or not args.streamers:
            print("Need to specify general and streamers files.")
            sys.exit(1)

        with open(args.general, "rb") as in_file:
            general = pickle.load(in_file)

        with open(args.streamers, "rb") as in_file:
            streamers = pickle.load(in_file)

        riotapi.set_region("NA")

        recommender = Recommender()
        recommender.train(general, streamers)
        recommender.to_file(args.model)
    elif args.update:
        if not args.streamers:
            print("Need to specify streamers file")
            sys.exit(1)

        with open(args.streamers, "rb") as in_file:
            streamers = pickle.load(in_file)

        recommender = Recommender.from_file(args.model)
        recommender._update_streamer_tree(streamers)
        recommender.to_file(args.model)
    else:
        if not args.summoner or not args.region:
            print("Need to specify summoner and region if recommending, or train if training")
            sys.exit(1)

        if not args.recs:
            args.recs = 12

        recommender = Recommender.from_file(args.model)
        riotapi.set_region(args.region)
        summoner = riotapi.get_summoner_by_name(args.summoner)
        masteries = summoner_masteries_from_cass(summoner.id)
        summoner = {"id": summoner.id, "region": args.region}

        for rec in recommender.recommend(summoner, masteries, num_recommendations=args.recs):
            print("{} - {}: {}".format(rec["id"], rec["region"], rec["score"]))


if __name__ == "__main__":
    main()
