from math import sqrt

# Get the list of mutually rated items
def sim_items(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    return si

# Returns a distance-based similarity score for p1 and p2
def sim_distance(prefs, p1, p2):
    si = sim_items(prefs, p1, p2)
    # if they have no ratings in common, return 0
    if len(si): return 0

    # add squares of all differences
    sum_of_squares=sum([pow(prefs[p1][item]-prefs[p2][item], 2)
                        for item in prefs[p1] if item in prefs[p2]])

    return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    si = sim_items(prefs, p1, p2)
    nb = len(si)
    if nb == 0: return 0

    # Sum all prefs
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sum square
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate peason score
    num = pSum - (sum1 * sum2)
    den = sqrt((sum1Sq - pow(sum1, 2)/nb) * (sum2Sq - pow(sum2, 2)/nb))
    if den == 0: return 0

    return num / den

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs, person, other), other)
                    for other in prefs if other != person]
    # Sort the list, highest is first
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue # don't compare to myself

        sim = similarity(prefs, person, other)

        if sim <= 0: continue # ignore score lower or equal to other

        for item in prefs[other]:
            # Score only movie that I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    status_update = 100
    # Create a dict of items showing the items the most similar items
    result = {}

    # Invert the pref matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large dataset
        c += 1
        if c % status_update == 0:
            print "%d / %d" % (c, len(itemPrefs))

        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity = sim_distance)
        result[item] = scores
    return result

def getRecommendatedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times simiarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # Sum if all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

