
from participant import *
from reader import *
from random import shuffle
import numpy as np
import argparse
import sys
import pandas as pd


# Match pairs by location
def create_pairs_by_location(participants):
    """
    Create pairs by location
    :param participants: dict with 3 fields: inda, near and far, each holding a list of Participant objects
    :return: list of Pair objects
    """

    # Get all the participants into groups in random order
    near = participants["near"]
    shuffle(near)
    far = participants["far"]
    shuffle(far)
    inda = participants["inda"]
    shuffle(inda)
    total_n = len(near) + len(far) + len(inda)

    # Check if the number is divisible by 6
    # Put extra people aside, prioritize people living further away
    leftovers = []
    remainder = total_n % 6
    if remainder:
        while (len(far) > 0) & (len(leftovers) < remainder):
            leftovers.append(far.pop())
        while (len(near) > 0) & (len(leftovers) < remainder):
            leftovers.append(near.pop())
        while (len(inda) > 0) & (len(leftovers) < remainder):
            leftovers.append(inda.pop())

    left_n = int(len(near) + len(far) + len(inda))
    pairs = [None] * int((left_n / 2))
    i = 0
    # Make pairs so that people from far are paired with people in if possible
    # If not, then with people near if possible
    # If not, with each other
    while (len(far) > 0) & (len(inda) > 0):
        pairs[i] = Pair([far.pop(), inda.pop()])
        i += 1
    while (len(far) > 0) & (len(near) > 0):
        pairs[i] = Pair([far.pop(), near.pop()])
        i += 1
    if len(far) > 0:
        print("Had to make pairs where both live far away")
    while len(far) > 0:
        pairs[i] = Pair([far.pop(), far.pop()])
        i += 1
    # If there were more people in than needed to match people from far away, match them with people near
    # and so on
    while (len(near) > 0) & (len(inda) > 0):
        pairs[i] = Pair([near.pop(), inda.pop()])
        i += 1
    while len(near) > 0:
        pairs[i] = Pair([near.pop(), near.pop()])
        i += 1
    while len(inda) > 0:
        pairs[i] = Pair([inda.pop(), inda.pop()])
        i += 1

    # Add leftovers to pairs making the main course & dessert
    for j in range(0, len(leftovers)):
        pairs[j + int((len(pairs)/3))].participants.append(leftovers[j])

    return pairs


def create_pairs_simple(participants):
    """
    Create pairs randomly
    :param participants: list of Participant objects
    :return: list of Pair objects
    """

    shuffle(participants)

    # Check if the number is divisible by 6
    # Put extra people aside
    leftovers = []
    total_n = len(participants)
    remainder = total_n % 6
    if remainder:
        while len(leftovers) < remainder:
            leftovers.append(participants.pop())
    # Create pairs
    pairs = []
    while len(participants) > 0:
        pairs.append(Pair([participants.pop(), participants.pop()]))

    # Add leftovers to pairs making the main course & dessert
    for j in range(len(leftovers)):
        pairs[j + int((len(pairs) / 3))].participants.append(leftovers[j])

    return pairs


def create_submatrix_lower(d):
    """
    Create a submatrix for the lower triangular part of the complete (block) adjacency matrix
    :param d: integer, the size of the matrix
    :return: d times d 2D numpy array
    """
    row = [1,2,3] + [0] * (d-3)
    submatrix = np.zeros((d, d))

    for i in range(d):
        submatrix[i,:] = row
        # Switch last element to first, pushing others back
        row = row[-1:] + row[:-1]

    return submatrix


def set_hosts(pairs):
    """
    Set hosts for every meal, define rotation of pairs
    :param pairs: list of Pair objects
    :return: Nothing, modifies pairs in place
    """

    # Initialize adjajency matrix
    # 0 = no connection
    # 1 = eat starter together
    # 2 = eat main together
    # 3 = eat dessert together
    n_pairs = len(pairs)
    adjacency_matrix = np.zeros((n_pairs, n_pairs))

    third_n = int(n_pairs / 3)
    # Get indices of starter, main and dessert hosts
    starters = list(range(third_n))
    mains = list(range(third_n,2 * third_n))
    desserts = list(range(2*third_n, n_pairs))

    # Create a submatrix and construct the block matrix
    submatrix = create_submatrix_lower(third_n)

    adjacency_matrix[np.ix_(mains, starters)] = adjacency_matrix[np.ix_(desserts, starters)] = adjacency_matrix[np.ix_(desserts, mains)] = submatrix
    adjacency_matrix[np.ix_(starters, mains)] = adjacency_matrix[np.ix_(starters, desserts)] = adjacency_matrix[np.ix_(mains, desserts)] = submatrix.T

    # Set hosts accordingly
    for e in starters:
        starter_idx = np.where(adjacency_matrix[e,:] == 1)[0]
        for ind in starter_idx:
            pairs[ind].starter_host = pairs[e]

    for m in mains:
        main_idx = np.where(adjacency_matrix[m,:] == 2)[0]
        for ind in main_idx:
            pairs[ind].main_host = pairs[m]

    for d in desserts:
        dessert_idx = np.where(adjacency_matrix[d,:] == 3)[0]
        for ind in dessert_idx:
            pairs[ind].dessert_host = pairs[d]


def write_results(pairs, outfile):
    """
    Write results to csv
    :param pairs: list of Pair objects
    :param outfile: string, output file path
    :return: -
    """

    results = np.empty((len(pairs), 6), dtype='<U100')
    for p, pair in enumerate(pairs):
        results[p] = pair.get_info()

    results = pd.DataFrame(results)

    results.to_csv(outfile, header=["Names","Contact","Diet","Starter","Main","Dessert"], index=False)
    
    #np.savetxt(outfile, results, delimiter=",", fmt='"%s"', comments="",
    #           header="Names,Contact,Diet,Starter,Main,Dessert")


if __name__ == "__main__":
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("-l", "--location", action="store_true")
    
    args = parser.parse_args()
    
    if (not args.infile) or (not args.outfile):
        print("Please provide both input and output file paths")
        sys.exit()

    # Read input data
    # Create pairs by location or by random
    rdr = Reader(args.infile)
    if args.location:
        participants = rdr.read_by_location()
        pairs = create_pairs_by_location(participants)
    else:
        participants = rdr.read_simple()
        pairs = create_pairs_simple(participants)
    set_hosts(pairs)
    write_results(pairs, args.outfile)
