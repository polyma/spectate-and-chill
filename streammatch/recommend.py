class Recommender(object):
    @staticmethod
    def from_file(filepath):
        """
        Loads an existing trained recommender model from a file on disk

        filepath    str            the path on disk to the model file

        returns     Recommender    the recommender loaded from the file
        """
        return Recommender()

    def for_user(self, summoner_id):
        """
        Gets general recommendations for a user - which streamers they're likely to want to watch in sorted score order with scores

        summoner_id    int             the summoner to get recommendations for

        returns        list<object>    a list of recommendation objects with score and id
        """
        return [
            {
                "id": 5908,
                "score": 1.0,
                "realm": "NA"
            },
            {
                "id": 51575588,
                "score": 0.75,
                "realm": "NA"
            },
            {
                "id": 20132250,
                "score": 0.5,
                "realm": "NA"
            }
        ]

    def for_streamer(self, summoner_id, score_threshold=0.75):
        """
        Gets a list of users likely to be interested in a streamer's new match

        summoner_id        int      the streamer who has just entered a match
        score_threshold    float    the interest score limit for users to be interested in the match
        """
        return [
            {
                "id": 22508641,
                "score": 1.0,
                "realm": "NA"
            },
            {
                "id": 28341307,
                "score": 0.75,
                "realm": "NA"
            },
            {
                "id": 45193160,
                "score": 0.5,
                "realm": "NA"
            }
        ]
