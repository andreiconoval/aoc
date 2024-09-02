
s = 1
t = 6
n = 6

# For AlgGenericDMF, Ford Fulkerson & Edmonds Karp:

f = [
    [0, 0, 5, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

c = [
    [0, 7, 5, 0, 0, 0],
    [0, 0, 1, 5, 2, 0],
    [0, 2, 0, 0, 8, 0],
    [0, 0, 0, 0, 2, 10],
    [0, 0, 0, 3, 0, 13],
    [0, 0, 0, 0, 0, 0]
]

# import generic_dmf_algorithm 
# alg_generic = generic_dmf_algorithm.GenericDMFAlgorithm(n, s, t)
# alg_generic.execute_generic_dmf_algorithm(f, c)


# import alg_forf_fulkerson 
# alg_ff_generic = alg_forf_fulkerson.FordFulkersonAlgorithm(n, s, t)
# alg_ff_generic.execute_ford_fulkerson_algorithm(f,c)

import alg_edmos_karp
alg_ek = alg_edmos_karp.EdmondsKarpAlgorithm(n, s, t)
alg_ek.execute_edmonds_karp_algorithm(f, c)