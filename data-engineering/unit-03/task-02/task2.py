import pymongo

# TODO 2: Complete the `get_recent_favorite_movie_by_user` function by replacing
#         the `<query>` string with the actual query.
def get_recent_favorite_movie_by_user(user_id, collection):
    """
    user_id: reviewerID (string)
    collection: pymongo pointer to a collection established via MongoClient
    returns: asin of the movie most recently rated as 5 by the reviewer with
             user_id (string)
    """
    reviews = collection.find(
        {"reviewerID": user_id, "overall": 5},
        {"asin": 1, "_id": 0}
    ).sort("unixReviewTime", pymongo.DESCENDING)
    try:
        return reviews.next().get('asin')
    except StopIteration:
        return


# TODO 3: Complete the `get_users_by_favorite_movie` function by replacing
#         the `<query>` string with the actual query.
def get_users_by_favorite_movie(favorite_asin, collection):
    """
    favorite_asin: asin (string)
    collection: pymongo pointer to a collection established via MongoClient
    returns: list of reviewerIDs (string) of the reviewers who rated the movie
             with asin equal to favorite_asin with 5
    """
    reviewers = collection.find(
        {"asin": favorite_asin, "overall": 5},
    )
    #[print(reviewer["reviewerID"], reviewer["overall"], reviewer["asin"]) for reviewer in reviewers]
    return [reviewer["reviewerID"] for reviewer in reviewers]


# TODO 4: Complete the `get_movies_reviewed_by_user` function by replacing
#         the `<query>` string with the actual query.
def get_movies_reviewed_by_user(user_id, collection):
    """
    user_id: reviewerID (string)
    collection: pymongo pointer to a collection established via MongoClient
    returns: set of the asin of the movies reviewed by the reviewer with
             user_id (string)
    """
    reviews = collection.find(
        {"reviewerID": user_id},
        {"asin": 1, "_id": 0}
    )
    return {review['asin'] for review in reviews}


# TODO 5: Complete the `get_recommendations` function by replacing
#         the None values assigned to favorite_asin, already_seen, and
#         similar_users with calls to the three functions you implemented
#         earlier. Provide the functions with arguments as needed.
def get_recommendations(user_id, collection):
    """
    user_id: reviewerID (string)
    collection: pymongo pointer to a collection established via MongoClient
    returns: list of asin of the movies that were rated with 5 (overall) by
             the users who rated the most recent user_id's 5 movie with 5 as
             well ordered from the most recent review
    """
    favorite_asin = get_recent_favorite_movie_by_user(user_id, collection)
    already_seen = get_movies_reviewed_by_user(user_id, collection)
    similar_users = get_users_by_favorite_movie(favorite_asin, collection)
    similar_users = [user for user in similar_users if user != user_id]
    candidate_recommendations = collection.find(
        {"reviewerID": {"$in": similar_users}, "overall": 5},
        {"asin": 1, "_id": 0}
    ).sort("unixReviewTime", pymongo.DESCENDING)
    candidate_recommendations =  [
        recommendation["asin"] for recommendation in candidate_recommendations
        if recommendation["asin"] not in already_seen
    ]
    recommendations = []
    for recommendation in candidate_recommendations:
        if recommendation not in recommendations:
            recommendations.append(recommendation)
        if len(recommendations) >= 10:
            break
    return recommendations

if __name__ == "__main__":
    # TODO 1: Replace the <CONNECTION_STRING> with the actual connection string
    #         that you can obtain from Azure.
    uri = "mongodb://cyberphordataengineeringunit02:rRcL9iTOc5XSPS0ySLRROJRUzcAe8IKQinrgazcI6bUCRg8jqBrwvIr2WU4gzvbIH3GpHNF6sshEACDbrMcYcw==@cyberphordataengineeringunit02.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cyberphordataengineeringunit02@"
    client = pymongo.MongoClient(uri)
    reviews_col = client['Customer_reviews']['movie_reviews']
    assert get_recent_favorite_movie_by_user("AWF2S3UNW9UA0", reviews_col) == "0005019281"
    assert get_users_by_favorite_movie("0005019281", reviews_col) == ['A1VKW06X1O2X7V', 'A5NYUBEKXFLX5', 'A2DJ8B8GE4V2VD', 'A2L0G56BNOTX6S', 'AWF2S3UNW9UA0', 'A3O4UUT83DG3OU', 'A3TK5Q142X5Q8A', 'A1GHUN5HXMHZ89', 'AAM67Y93KTIOL', 'A1GQF4JDJXBRLH', 'A3UEOL981G9TXY', 'AZBWH4HLG3JWV', 'A33EWPXESP9GQH', 'A38IHZTC22PHEH', 'A1PXS5N63PS6WR', 'A27BF3YQB9N8AH', 'A1FIPOMYT9W4FS', 'A2PNKBQJQT7RS8', 'AVWWFK3FZDEL2', 'A126Q2HVTCS9P2', 'A10O6QLKFO3R6R', 'A2D4HRAA7E0FRQ', 'AZB4CQ9JZSUQB', 'AKOE75QZDY7A4', 'A258ONALWRQMV1', 'A1M4W5ZUKL7QT7', 'A1U3G5C5JX3Y6B', 'AJLAJCO6GTFWN', 'AVECJZDR0LYZN', 'A3L3ORBU5IXTMX', 'ATXWVGLKWDPX4', 'A306NASGVUDFKF', 'A197O2J5BA4AQ', 'A2OHY2ZPWUX1XR', 'A28L7RYP6FYGN9', 'A2P64DWIPY4O2', 'A2S689D469XHA1', 'A38I4SUI5XZVUT', 'AFWFSEHPJABT9', 'ATAGA4N9SMWWQ', 'A13MTBI2DEEQ0K', 'A38JFF6SGZEO37', 'A1ZIBVOIPBWR3U', 'A1MUTGFKWD74U4', 'A2PSMIRDHYYONP', 'A2UNEJNV11TNQ9', 'A3NK0FJRFM8QGN', 'A1HP3B92A3JDQ1', 'A1CMD08Z49PGKQ', 'AARUYE130LY8W', 'A1FP2LA6M2OJX0', 'A2TBX8WPVXLTU1', 'A370EYV6NOCKCF', 'ATWFMTZEH77H1', 'A3VERR8USXCHS4', 'A34FIXMNVBMS1T', 'AOY8BQ755A5YL', 'A4BZ72C28JFIC', 'A1BBBIN5NMNPV7', 'A363G63SXEGECS', 'A1GQIFHHSJVWO7', 'A1YCGGT3M8NR7C', 'A13V0P2YT13S9H', 'A39N89RKKCWUHJ', 'A2IDX2U03CL90F', 'A2EKIE8ATFNAWU', 'AG94A4EVFG0MQ']
    assert get_movies_reviewed_by_user("AWF2S3UNW9UA0", reviews_col) == {'0005019281', '0767825616', '0780625781'}
    assert get_recommendations("AWF2S3UNW9UA0", reviews_col) == ['0780613678', '0767726227', '0780627806', '0780623746', '0782002064', '0767832485', '0783107986', '0767809688', '0783113196', '0767825373']