# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.ticker as mticks


# Apologies in advance if my code is arcane... =]


adjacency_matrix = np.array([[0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                             [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                             [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                             [1, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                             [0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]])

#Having drawn a bridge from G to I, and a path from D to A
adjacency_matrix = np.array([[0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                             [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                             [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                             [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                             [1, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                             [0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                             [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]])
# note each ride isn't adjacent to itself

def create_m():
    '''Creates M, according to the given rule. As I'm writing this, the 
    formula is this; if column j has l entries in the adjacency matrix;
        a_ij = { 1/(3*l + 1), if i = j
                 3/(3*l + 1), if i adj. to j
                 0, otherwise 
                                             }
    '''
    M = np.zeros((10, 10))
    for j in range(0, 10): # for column in M
        l = adjacency_matrix[:,j].sum() # no. of adj. rides
        for i in range(0, 10): # for entry in column
            if i == j:
                M[i, j] = 1/(3*l + 1)
            elif adjacency_matrix[i,j] == 1:
                M[i, j] = 3/(3*l + 1)
            # else; stay 0
    
    return M

def create_m2():
    '''Creates M NEW RULE
        a_ij = { 1/(5*l + 1), if i = j
                 3/(5*l + 1), if i adj. to j
                 0, otherwise 
                                             }
    '''
    M = np.zeros((10, 10))
    for j in range(0, 10): # for column in M
        l = adjacency_matrix[:,j].sum() # no. of adj. rides
        for i in range(0, 10): # for entry in column
            if i == j:
                M[i, j] = 1/(5*l + 1)
            elif adjacency_matrix[i,j] == 1:
                M[i, j] = 5/(5*l + 1)
            # else; stay 0
    
    return M

def create_m3():
    '''Creates M NEW NEW RULE
        a_ij = { 1/l, if i adj. to j
                 0, otherwise 
                                             }
    '''
    M = np.zeros((10, 10))
    for j in range(0, 10): # for column in M
        l = adjacency_matrix[:,j].sum() # no. of adj. rides
        for i in range(0, 10): # for entry in column
            if adjacency_matrix[i,j] == 1:
                M[i, j] = 1/l
            # else; stay 0
    
    return M


def left_multiply_M(M, x_actual):
    ''' I want this to create a stackplot. I'll left-multiply by M until
    our current x_k is within less that 1% error. That is, 
    (||x_k|| - ||x_longterm||)/||x_longterm|| < 1/100.
    x_actual of course, is the eigenvector calculated in Q1a.
    '''
    x_k = np.array([1,0,0,0,0,0,0,0,0,0]) #initial, all at A
    error = 1
    stepno = 0
    steps = [0]
    distributions = np.array([x_k])
    norm_x_actual = np.linalg.norm(x_actual, ord=np.inf)
    
    while error > 1/100 and stepno < 50:
        # FOR READER'S INFORMATION
        # I edited stuff here for the graph; usually stepno < 1000
        # And see below error doesn' get updated
        # Initially I ran this part until the error got below 1%
        # I recorded the stepno and then added the black line manually
        # so the graphs would all have the same range of steps on x axis
        
        x_k = M @ x_k
        stepno += 1
        norm_x_k = np.linalg.norm(x_k, ord=np.inf)
        #error = (norm_x_k - norm_x_actual)/norm_x_actual
        
        distributions = np.concatenate((distributions, np.array([x_k])), axis=0)
        steps.append(stepno)
        
    #plt.stackplot(steps, distributions[0,:], distributions[1,:], distributions[2,:],
    #              distributions[3,:], distributions[4,:], distributions[5,:],
    #              distributions[6,:], distributions[7,:], distributions[8,:], 
    #              distributions[9,:])
    plt.stackplot(steps, 100*distributions.T, labels=['A', 'B', 'C', 'D', 'E', 'F',
                                                  'G', 'H', 'I', 'J'])
    plt.xlabel("Step number n")
    plt.ylabel("Percentage of visitors in each attraction %")
    plt.title("Distribution of visitors after 50 iterations of M")
    #plt.yaxis.set_major_formatter(mticks.PercentFormatter(xmax=1))
    plt.axvline(43, 0, 100, color='black')
    plt.legend(loc='upper right', bbox_to_anchor=(0.95, 0.85), framealpha = .65)
    
    plt.show()
    
    
    

#def main():
new_M = create_m()
    
eigvals, eigvecs = np.linalg.eig(new_M)    
domeigvec = eigvecs[:,0]
domeigvec /= np.linalg.norm(domeigvec, ord=1)
left_multiply_M(new_M, domeigvec)

#main()
#### My create_m actually does what I want it to. =]. It does what I did manually.

    
    
    
