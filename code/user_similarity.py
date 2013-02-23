from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches, 
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def extract_user_review(self, a, record):
        if record['type'] == 'review':
            yield record['user_id'], record['business_id']

    def user_reviews(self, user_id, business_ids):

        businesses = set(business_ids)
        yield user_id, list(businesses)

    def combine_users(self, user_id, business_ids):

        yield "all_users", [ user_id , business_ids ]

    def user_combos(self, _, users):

        for userN,userM in combinations(users,2):
            yield [ userN, userM ]

    def jaccard(self, userN, userM):

        intersection = set(userN[1]).intersection(set(userM[1]))
        union = set(userN[1]).union(set(userM[1]))
        jaccard = float(len(intersection))/float(len(union))

        if jaccard >= 0.5:
            yield [userN[0],userM[0]], jaccard

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:

        mapper1: extract_user_review <line, record> => <user_id, business_id>
        reducer1: user_reviews <user_id, business_ids> => <user_id, business_ids>
        mapper2: combine_users <user_id, business_ids> => <"all_users", [ user_id, business_ids ]>
        reducer2: user_combos <"all_users", users> => <userN, userM>
        mapper3: jaccard <userN, userM> => <[userN_id,userM_id], jaccard>
        """

        return [self.mr(self.extract_user_review, self.user_reviews),
            self.mr(self.combine_users, self.user_combos),
            self.mr(mapper=self.jaccard)]

if __name__ == '__main__':
    UserSimilarity.run()
