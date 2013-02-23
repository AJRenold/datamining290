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
                yield record['user_id'] , record['business_id']

    def business_users(self, user_id, business_id):

        businesses = set(business_id)
        for business in businesses:
            yield business, [ user_id, list(businesses) ]

    def select_users(self, business, users):

        yield business, users

    def user_combos(self, business, users):

        for userN, userM in combinations(users,2):
            #if len(userN[1]) > 3 and len(userM[1]) > 3:
            yield userN, userM


    def jaccard(self, userN, userM):

        intersection = set(userN[1]).intersection(set(userM[1]))
        union = set(userN[1]).union(set(userM[1]))
        jaccard = float(len(intersection))/float(len(union))

        if jaccard >= 0.5:
            yield [userN[0],userM[0]], jaccard

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <key, value>
        reducer1: <key, [values]>
        mapper2: ...
        """
        
        return [self.mr(self.extract_user_review, self.business_users),
            self.mr(self.select_users, self.user_combos),
            self.mr(mapper=self.jaccard)]


if __name__ == '__main__':
    UserSimilarity.run()
