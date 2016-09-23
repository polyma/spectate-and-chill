import numpy as np
import pickle
from sklearn import decomposition
from sklearn.neighbors import KDTree

from cassiopeia import riotapi, baseriotapi


NUM_COMPONENTS = 131
LEAF_SIZE = 20
METRIC = "euclidean"
REQUIRED = {"id", "region"}


def summoner_masteries_from_cass(summoner_id):
    return [x.__dict__ for x in baseriotapi.get_champion_masteries(summoner_id)]


def get_mastery_vector(champion_indexes, summoner_masteries):
    vector = np.zeros(len(champion_indexes), dtype=np.float)
    for mastery in summoner_masteries:
        vector[champion_indexes.index(mastery["championId"])] = mastery["championPoints"]
    return normalize(vector, norm="l1")


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
    def __init__(self, general_summoners, streamer_summoners):
        self.__champion_indexes = sorted([champion.id for champion in riotapi.get_champions()])
        self.__train(general_summoners, streamer_summoners)

    def __train(self, general_summoners, streamer_summoners):
        data = np.zeros((len(general_summoners), len(self.__champion_indexes)), dtype=np.float)
        for i, row in enumerate(map(lambda x: get_mastery_vector(self.__champion_indexes, x["masteries"]), general_summoners)):
            data[i] = row

        self.__projection = decomposition.PCA(n_components=NUM_COMPONENTS)
        self.__projection.fit(data)

        points = np.zeros((len(streamer_summoners), NUM_COMPONENTS), dtype=np.float)
        for i, row in enumerate(map(lambda x: get_mastery_vector(self.__champion_indexes, x["masteries"]), streamer_summoners)):
            points[i] = self.__projection.transform(row)

        self.__streamer_tree = KDTree(points, leaf_size=LEAF_SIZE, metric=METRIC)
        self.__streamer_index = list()
        for s in streamer_summoners:
            s = dict(s)
            to_remove = set()
            for key in s:
                if key not in REQUIRED:
                    to_remove.add(key)
            for key in to_remove:
                del s[key]
            self.__streamer_index.append(s)

    def to_file(self, filepath):
        with open(filepath, "wb") as out_file:
            pickle.dump(self, out_file)

    @staticmethod
    def from_file(filepath):
        with open(filepath, "rb") as in_file:
            return pickle.load(in_file)

    def recommend(self, summoner, champion_masteries, num_recommendations=12):
        mastery_vector = get_mastery_vector(self.__champion_indexes, champion_masteries)
        projection = self.__projection.transform(mastery_vector)
        neighbors = self.__streamer_tree.query(projection, k=num_recommendations, return_distance=True)

        distances = neighbors[0]
        print(distances)
        indexes = neighbors[1]
        print(indexes)

        return [
            {
                "id": self.__streamer_index[index]["id"],
                "region": self.__streamer_index[index]["region"],
                "score": distances[0][i]
            }
            for i, index in enumerate(indexes[0])
        ]


riotapi.set_load_policy("lazy")
riotapi.set_rate_limit(25000, 10)
riotapi.set_data_store(None)
riotapi.set_api_key("RGAPI-e4491f0b-b99a-49c4-b817-5f9b00267da1")
riotapi.set_region("NA")

with open("general_masteries.pkl", "rb") as in_file:
    general = pickle.load(in_file)
with open("streamer_masteries.pkl", "rb") as in_file:
    streamers = pickle.load(in_file)

summoner = riotapi.get_summoner_by_name("DrCyanide")
summoner = {"id": summoner.id, "region": "NA"}
masteries = summoner_masteries_from_cass(summoner["id"])
rec = Recommender(general, streamers)
