from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches, 
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <key, value>
        reducer1: <key, [values]>
        mapper2: ...
        """
        
        def extract_user_review(self, _, record):
            if record['type'] == 'review':
                yield record['user_id'], record['review_id']

        def user_reviews(self, user_id, review_ids):
            reviews = []
            for review in review_ids:
                reviews.append(review)

            yield user_id, reviews
        

        return [self.mr(mapper=self.mapper1, reducer=self.reducer1),
                self.mr(mapper=...)]


if __name__ == '__main__':
    UserSimilarity.run()
