__author__ = 'jtpollard'

import json
import time
import numpy as np
from collections import defaultdict


FILENAME = '/Users/jtpollard/MSAN/Practicum/sample_data/train.json'
THETA = 0.5


def eff_of_theta(theta):
    """
    function of theta, returns the value
    :param theta:
    :return:
    """
    return float(1-theta)/(1+theta)


def get_recipes(filename):
    """
    opens the json file and returns the json recipes
    :param filename:
    :return:
    """

    f = open(filename)

    recipes = json.load(f)

    f.close()

    return recipes


def intersect(list1, list2):
    """
    finds the intersection of the two lists
    :param list1:
    :param list2:
    :return:
    """

    return list(set(list1) & set(list2))


def union(list1, list2):
    """
    finds the union of the two lists
    :param list1:
    :param list2:
    :return:
    """

    list_union = list1

    for el in list2:

        if el not in list_union:

            list_union.append(el)

    return list_union


def similarity(rec1, rec2):
    """
    computes the similarity of two recipes
    :param rec1:
    :param rec2:
    :return:
    """

    rec1_and_rec2 = intersect(rec1, rec2)
    rec1_or_rec2 = union(rec1, rec2)

    # return the similarity between the recipes
    return float(len(rec1_and_rec2)) / len(rec1_or_rec2)


def get_neighbors(recipes):
    """
    accepts list of recipes. computes the neighbors
    based on similarity and returns a list of lists of indices
    corresponding to the neighbors of each element in the
    passed list
    :param recipes:
    :return:
    """
    neighbors = list()

    for i in range(len(recipes)):

        neighbor_inds = list()
        current_recipe = recipes[i]['ingredients']

        for j in range(len(recipes)):

            if j != i:

                other_recipe = recipes[j]['ingredients']

                if similarity(current_recipe, other_recipe) >= THETA:

                    neighbor_inds.append(j)

        neighbors.append(neighbor_inds)

    return neighbors


def get_links(recipes):
    """
    accepts a list of cuisine and recipes and computes the
    number of links among the set
    :param recipes:
    :return:
    """
    neighbors = get_neighbors(recipes)
    n = len(recipes)
    adjacency = [[0 for c in range(n)] for r in range(n)]

    for i in range(n):

        for j in range(len(neighbors[i])):

            adjacency[i, neighbors[i][j]] += 1

    adjacency = np.matrix(adjacency)

    links = adjacency * adjacency

    return links


def goodness_of_fit(cl1, cl2, link):
    """
    accepts two lists of lists, each of cl1 and cl2 contain lists of recipes
    that are in the cluster associated with recipe i
    also accepts a matrix of links
    :return: a number that tells how "close" the clusters are
    """

    exponent = 1 + 2*eff_of_theta(THETA)
    n1 = len(cl1)
    n2 = len(cl2)
    denominator = ((n1+n2)**exponent) - (n1**exponent + n2**exponent)

    numerator = 0.0

    for i in range(n1):

        for j in range(n2):

            numerator += link[cl1[i], cl2[j]]

    return numerator/denominator


def cluster(s, k):
    """
    -accepts the set of points and the number of clusters desired
    -the set of points is a list of indices
    -runs until the set of clusters has size k
    :param s:
    :param k:
    :return:
    """
    # TODO fill in the clustering algorithm
    pass



if __name__ == "__main__":

    r = get_recipes(FILENAME)

    print len(r)

    cuisines = list()
    ingredients = list()

    for i in range(len(r)):

        c = r[i]['cuisine']

        if c not in cuisines:

            cuisines.append(c)

        for j in range(len(r[i]['ingredients'])):

            el = r[i]['ingredients'][j]

            if el not in ingredients:

                ingredients.append(el)


    print len(cuisines)
    print len(ingredients)



# end of cuisine.py