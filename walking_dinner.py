
from participant import *
from reader import *
from random import shuffle
import numpy as np
import argparse
import sys


# Returns list of pair objects
def create_pairs(participants):

    # Get all the participants into groups in random order
    near = participants["near"]
    shuffle(near)
    far = participants["far"]
    shuffle(far)
    inda = participants["inda"]
    shuffle(inda)
    total_n = len(near) + len(far) + len(inda)

    # Check if the number is divisible by 6
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
    meals = ["entree"] * int((len(pairs)/3)) + ["main"] * int((len(pairs)/3)) + ["dessert"] * int((len(pairs)/3))
    i = 0
    # Make pairs so that people from far are paired with people from Niemi if possible
    # If not, then with people near otaniemi if possible
    # If not, with each other
    while len(far) & len(inda):
        pairs[i] = Pair([far.pop(), inda.pop()], meals[i])
        i += 1
    while len(far) & len(near):
        pairs[i] = Pair([far.pop(), near.pop()], meals[i])
        i += 1
    if len(far):
        print("Had to make pairs where both live far away")
    while len(far):
        pairs[i] = Pair([far.pop(), far.pop()], meals[i])
        i += 1
    # If there were more people in Otaniemi than needed to match people from far away, match them with people near
    # and so on
    while len(near) & len(inda):
        pairs[i] = Pair([near.pop(), inda.pop()], meals[i])
        i += 1
    while len(near):
        pairs[i] = Pair([near.pop(), near.pop()], meals[i])
        i += 1
    while len(inda):
        pairs[i] = Pair([inda.pop(), inda.pop()], meals[i])
        i += 1

    # Add leftovers to pairs making the main course & dessert
    for j in range(0, len(leftovers)):
        pairs[j + int((len(pairs)/3))].participants.append(leftovers[j])

    return pairs

# Create a submatrix for the lower triangular
def create_submatrix_lower(d):
    row = [1,2,3] + [0] * (d-3)
    submatrix = np.zeros((d, d))

    for i in range(d):
        submatrix[i,:] = row
        # Switch last element to first, pushing others back
        row = row[-1:] + row[:-1]

    return submatrix


def set_hosts(pairs):
    """
    Choose who hosts who on which meals
    With a number of pairs higher than 9, no pair will see each other more than once
    """

    # Initialize adjajency matrix
    # 0 = no connection
    # 1 = eat entree together
    # 2 = eat main together
    # 3 = eat dessert together
    n_pairs = len(pairs)
    adjacency_matrix = np.zeros((n_pairs, n_pairs))

    third_n = int(n_pairs / 3)
    # Get indices of entree, main and dessert hosts
    entrees = list(range(third_n))
    mains = list(range(third_n,2 * third_n))
    desserts = list(range(2*third_n, n_pairs))

    # Create a submatrix and construct the block matrix
    submatrix = create_submatrix_lower(third_n)

    adjacency_matrix[np.ix_(mains, entrees)] = adjacency_matrix[np.ix_(desserts, entrees)] = adjacency_matrix[np.ix_(desserts, mains)] = submatrix
    adjacency_matrix[np.ix_(entrees, mains)] = adjacency_matrix[np.ix_(entrees, desserts)] = adjacency_matrix[np.ix_(mains, desserts)] = submatrix.T

    # Set hosts accordingly
    for e in entrees:
        entree_idx = np.where(adjacency_matrix[e,:] == 1)[0]
        for ind in entree_idx:
            pairs[ind].entree_host = pairs[e]

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
    """

    results = np.empty((len(pairs), 6), dtype='<U100')
    for p, pair in enumerate(pairs):
        results[p] = pair.get_info()
    
    np.savetxt(outfile, results, delimiter = ",", fmt='"%s"', comments = "",
              header = "Names,Contact,Diet,Entree,Main,Dessert")


if __name__ == "__main__":
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--infile")
    parser.add_argument("-out", "--outfile")
    
    args = parser.parse_args()
    
    if (not args.infile) or (not args.outfile):
        print("Please provide both input and output file paths")
        sys.exit()
    
    # Run the principal functions
    rdr = Reader(args.infile)
    participants = rdr.read_to_objects()
    pairs = create_pairs(participants)
    set_hosts(pairs)
    write_results(pairs, args.outfile)
