import numpy as np
import functools
import pickle
from sklearn import decomposition, KDTree

from cassiopeia import baseriotapi, riotapi


NUM_COMPONENTS = 10
LEAF_SIZE = 20
METRIC = "euclidean"


def get_mastery_vector(champion_indexes, summoner):
    baseriotapi.set_region(summoner["region"])
    masteries = baseriotapi.get_champion_masteries(summoner["id"])
    gen = map(lambda x: x.championPoints, masteries)
    return normalize(np.fromiter(gen, np.float), norm="l1")


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
        to_mastery_vector = functools.partial(get_mastery_vector, self.__champion_indexes)
        data = np.zeros((len(self.__champion_indexes), len(general_summoners)), dtype=np.float)
        for i, row in enumerate(map(to_mastery_vector, general_summoners)):
            data[i] = row

        self.__projection = decomposition.PCA(n_components=NUM_COMPONENTS)
        self.__projection.fit(data)
        # self.__projection.explained_variance_ # Eigenvalues

        points = np.zeros((len(streamer_summoners), NUM_COMPONENTS), dtype=np.float)
        for i, row in enumerate(map(to_mastery_vector, streamer_summoners)):
            points[i] = self.__projection.transform(row)

        self.__streamer_tree = KDTree(points, leaf_size=LEAF_SIZE, metric=METRIC)
        self.__streamer_index = streamer_summoners
        self.__user_tree = None
        self.__user_index = []

    def to_file(self, filepath):
        with open(filepath, "wb") as out_file:
            pickle.dump(self, out_file)

    @staticmethod
    def from_file(filepath):
        """
        Loads an existing trained recommender model from a file on disk

        filepath    str            the path on disk to the model file

        returns     Recommender    the recommender loaded from the file
        """
        with open(filepath, "rb") as in_file:
            return pickle.load(in_file)

    def for_user(self, summoner, num_recommendations=5):
        """
        Gets general recommendations for a user - which streamers they're likely to want to watch in sorted score order with scores

        summoner_id    int             the summoner to get recommendations for

        returns        list<object>    a list of recommendation objects with score and id
        """
        mastery_vector = get_mastery_vector(self.__champion_indexes, summoner)
        projection = self.__projection.transform(mastery_vector)
        neighbors = self.__streamer_tree.query(projection, k=num_recommendations)
        self.__user_tree = KDTree(np.vstack(self.__user_tree.data, projection), leaf_size=LEAF_SIZE, metric=METRIC)
        self.__user_index.append(summoner)

        return [
            {
                "id": self.__streamer_index[index]["id"],
                "region": self.__streamer_index[index]["region"],
                "score": distance
            }
            for distance, index in neighbors
        ]

    def for_streamer(self, summoner, score_threshold=4):
        """
        Gets a list of users likely to be interested in a streamer's new match

        summoner_id        int      the streamer who has just entered a match
        score_threshold    float    the interest score limit for users to be interested in the match
        """
        mastery_vector = get_mastery_vector(self.__champion_indexes, summoner)
        projection = self.__projection.transform(mastery_vector)
        neighbors = self.__user_tree.query_radius(projection, score_threshold, sort_results=True, return_distance=True)

        return [
            {
                "id": self.__user_index[index]["id"],
                "region": self.__user_index[index]["region"],
                "score": distance
            }
            for distance, index in neighbors
        ]
