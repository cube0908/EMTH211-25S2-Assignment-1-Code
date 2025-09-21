# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 14:32:25 2025


"""

import numpy as np
import matplotlib.pyplot as plt

A = np.array([[-2. +  .5j,  .1 + 0.j, -.5 + 1.j,  0. + -.1j,   .1 +  0.j],
              [ .2 +  0.j,  3. + 0.j,  0. + 0.j,  .1 +  .1j,   0. +  .2j],
              [ 0. +  .1j, -.1 + 0.j,  3. + 0.j,  2. +  0.j,   .1 + -.1j],
              [ 1. +  .2j,  0. + 1.j,  .3 + 0.j, -4. +  1.j,   1. +  1.j],
              [ .1 +  0.j,  .2 + 0.j,  1. + 0.j,  .1 +  .1j,   3. +  .1j]])
I = np.eye(5)

centres = [A[i][i] for i in range(A.shape[0])]
row_radii = []
for i in range(A.shape[0]):
    summed = 0
    for j in range(A.shape[0]):
        if j != i:
            summed += abs(A[i][j])
    row_radii.append(summed)
    
col_radii = []
for j in range(A.shape[0]):
    summed = 0
    for i in range(A.shape[0]):
        if j != i:
            summed += abs(A[i][j])
    col_radii.append(summed)


fig , ax = plt . subplots ()
ax . grid ()
for i in range ( A . shape [ 0 ] ) :
    ax . add_patch ( plt . Circle (( centres [ i ] . real , centres [ i ] . imag ) ,
                                   row_radii [ i ] , color = 'blue' , alpha = .2 ) )
    ax . add_patch ( plt . Circle (( centres [ i ] . real , centres [ i ] . imag ) ,
                                   col_radii [ i ] , color = 'green' , alpha = .2 ) )
ax . axis ('equal')
plt.title("Gershgorin discs, plotted")

#Above is for plotting Gershgorin discs

#Now, for inverse power method
#I'll adapt my power method code from one of the quizzes

##BELOW FROM PREVIOUS QUIZ
def rayleigh(y, x):
    '''Computes Rayleigh quotient. y = Ax.'''
    return (np.dot(y, x))/(np.dot(x, x))

def power_method(A, x0, max_iter=1000, tol=1e-7):
    '''will find an eigenvector associated with the dominant eigenvalue of a 
    matrix, A using the power method with a starting guess of x0.'''
    x_new = x0
     
    R_new = np.inf
    
    
    
    k = 0
    error = tol + 1
    while k < max_iter and error >= tol:
        
        #if k > 0: #i.e. if we actually have something to compare
        R_old = R_new 
        R_new = rayleigh(A@x_new, x_new) 
        error = abs(R_new - R_old)/abs(R_new)  
         
        x_old = x_new #Updating; x_old was last iteration's x_new
        y_new = A @ x_old # finding Ax = y
        x_new = y_new/np.linalg.norm(y_new, ord=np.inf) #scaling Y for new x
         
        k += 1
        
    return R_new, x_new
##ABOVE adapted FROM PREVIOUS QUIZ

#Okay. So probably better to use LU decomposition to minimise computational
#cost. But since our n is fixed, I think it's better to just compute
#Binverse with np's function for it, and just use this directly.
#This trades the time I'd use for bugfixing for computational time... 

def find_eigenvalue(A, q, x0):
    '''given approx. location q for eigenvalue, will use shifted inverse
    power method to find an approximation of (ideally) that eigenvalue.
    x0 is some random starting vector, I want to be able to change it, to
    see if there's a slightly different result.
    This will be annoying, since three candidates for q (centres of discs)
    are really similar, two are both 3.'''
    B = A - q*I
    B_inv = np.linalg.inv(B)
    returned_evalue, returned_evector = power_method(B_inv, x0)
    evalue = (1/returned_evalue)+q #returned eval is 1(eval-1)
    return evalue


#our initial qs will be the centres of the discs
#Let's set
x0 = np.ones(5)
found_evals = []
for i in range(A.shape[0]):
    found_evals.append(find_eigenvalue(A, centres[i], x0))
    
targeted_evals = []
targeted_evals.append( find_eigenvalue(A, 5, x0))
targeted_evals.append( find_eigenvalue(A, 1, x0))

final_evals = [found_evals[0], found_evals[1], found_evals[3], targeted_evals[0], targeted_evals[1]]



fig , ax = plt . subplots ()
ax . grid ()
for i in range ( A . shape [ 0 ] ) :
    ax . add_patch ( plt . Circle (( centres [ i ] . real , centres [ i ] . imag ) ,
                                   row_radii [ i ] , color = 'blue' , alpha = .2 ) )
    ax . add_patch ( plt . Circle (( centres [ i ] . real , centres [ i ] . imag ) ,
                                   col_radii [ i ] , color = 'green' , alpha = .2 ) )
ax . axis ('equal')
plt.title("SIPM-computed eigenvalues and NumPy-computed eigenvalues")
evalsreal = [n.real for n in final_evals]
evalsimag = [n.imag for n in final_evals]
ax . plot (evalsreal, evalsimag, 'ro')
numpee_evals, numpee_evegs = np.linalg.eig(A)
npevalsreal = [n.real for n in numpee_evals]
npevalsimag = [n.imag for n in numpee_evals]
ax . plot (npevalsreal, npevalsimag, 'kx')













