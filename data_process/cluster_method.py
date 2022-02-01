# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:58:32 2021

@author: shouk
"""
import math
def slow_closest_pair(clusters):
    length = len(clusters)
    min_dist = math.inf
    result = None
    for idx in range(length):
        for idy in range(idx + 1, length):
            dist = clusters[idx].distance(clusters[idy])
            if dist <= min_dist:
                min_dist = dist
                result = (min_dist, clusters[idx], clusters[idy])
    return result
        