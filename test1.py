c = [[0, 7, 5, 0, 0, 0],
     [0, 0, 1, 5, 2, 0],
     [0, 2, 0, 0, 8, 0],
     [0, 0, 0, 0, 2, 10],
     [0, 0, 0, 3, 0, 13],
     [0, 0, 0, 0, 0, 0]]

f = [[0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]

c1 = [[0, 7, 3, 0, 0, 0],
      [0, 0, 1, 5, 1, 0],
      [0, 2, 0, 0, 6, 0],
      [0, 0, 0, 0, 2, 6],
      [0, 0, 0, 3, 0, 7],
      [0, 0, 0, 0, 0, 0]]

c_AO = [[0, 7, 9, 0, 0, 0],
        [0, 0, 2, 5, 0, 0],
        [0, 2, 0, 1, 13, 0],
        [0, 0, 0, 0, 2, 10],
        [0, 0, 0, 1, 0, 9],
        [0, 0, 0, 0, 0, 0]]

c_genPref = [[0, 8, 3, 0, 0],
             [0, 0, 2, 3, 1],
             [0, 2, 0, 0, 5],
             [0, 0, 0, 0, 5],
             [0, 0, 0, 0, 0]]

c_PrefFIFO = [[0, 7, 9, 0, 0],
              [0, 0, 2, 3, 1],
              [0, 1, 0, 0, 13],
              [0, 0, 0, 0, 4],
              [0, 0, 0, 0, 0]]

c_PrefEMax = [[0, 7, 5, 0, 0],
              [0, 0, 2, 3, 0],
              [0, 3, 0, 4, 6],
              [0, 0, 0, 0, 7],
              [0, 0, 0, 0, 0]]


s = 1
t = 6
n = 6


# import alg_scalare_capacitate # No good implementation
# alg_scap = alg_scalare_capacitate.CapacityScalingAlgorithm(n,s,t,f,c)
# alg_scap.execute_capacity_scaling_algorithm(f,c)

# import alg_scalare_bit
# alg_sbit = alg_scalare_bit.BitScalingAlgorithm(n,s,t,c1)
# alg_sbit.execute_bit_scaling_algorithm(c1)


# import alg_ahuja_orlin_shortest_path

# alg_ah_o_short = alg_ahuja_orlin_shortest_path.AhujaOrlinShortestPathAlgorithm(n,s,t)
# alg_ah_o_short.execute_ahuja_orlin_shortest_path(c_AO)


# import alg_ahuja_orlin_retele_stratificate

# alg_ah_o_ret_strat = alg_ahuja_orlin_retele_stratificate.AhujaOrlinLayeredNetworksAlgorithm(n,s,t)
# alg_ah_o_ret_strat.execute_ahuja_orlin_layered_networks(c_AO)


# import alg_generic_cu_preflux

# alg_gen_cu_pref = alg_generic_cu_preflux.GenericPreflowAlgorithm(5,1,5)
# alg_gen_cu_pref.execute_generic_preflow_algorithm(c_genPref)


# import alg_preflux_fifo

# alg_pref_fifo = alg_preflux_fifo.PreflowFIFOAlgorithm(5, 1, 5)
# alg_pref_fifo.execute_generic_preflow_algorithm(c_PrefFIFO)

# import alg_pref_cu_eticheta_maxima

# alg_pref_max_label = alg_pref_cu_eticheta_maxima.PreflowWithHighestLabelAlgorithm(5,1,5)
# alg_pref_max_label.execute_highest_label_preflow_algorithm(c_PrefEMax)