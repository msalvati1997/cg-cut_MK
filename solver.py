import solver
from docplex.mp.model import Model
from typing import Tuple
import numpy as np
import sys

def MKPpopulate(name: str) -> Tuple:
    # populateMKP

    '''
    This function extracts the raw data from a .txt file and populates the objective function coefficients
    array, the constraints coefficients matrix A and the right hand side b array
    
    Arguments:
        name -- the name of the .txt file that contains the raw data
        
    returns:
        c -- objective function coefficients array (shape = 1 * n)
        A -- constraints coefficients matrix A (shape = m * n)
        b -- right hand side values (shape = 1 * m)
    '''
    
    # Opening .txt file to read raw data of an instance
    file = open(str(name), 'r')
    x = []
    for line in file:
        splitLine = line.split()
        for i in range(len(splitLine)):
            x.append(splitLine[i])
    file.close()
    
    
    # Define parameters
    NumColumns, NumRows, BestOF = int(x.pop(0)), int(x.pop(0)), float(x.pop(0))
    print('This instance has %d variables and %d constraints' %(NumColumns, NumRows))

    if BestOF != float(0):
        print('Best known integer objective value for this instance = ', BestOF)
    else:
        print('Best integer objective value for this instance is not indicated')
    
    # Populating Objective Function Coefficients
    c = np.array([float(x.pop(0)) for i in range(NumColumns)])
    
    assert type(c) == np.ndarray
    assert len(c)  == NumColumns
    
    
    # Populating A matrix (size NumRows * NumColumns)
    ConstCoef = np.array([float(x.pop(0)) for i in range(int(NumRows * NumColumns))])    
    
    assert type(ConstCoef) == np.ndarray
    assert len(ConstCoef)  == int(NumRows*NumColumns)
    
    A = np.reshape(ConstCoef, (NumRows, NumColumns)) # reshaping the 1-d ConstCoef into A
    
    assert A.shape == (NumRows, NumColumns)
    
    
    # Populating the RHS
    b = np.array([float(x.pop(0)) for i in range(int(NumRows))])

    assert len(b) == NumRows
    assert type(b) == np.ndarray
    
    return (c, A, b)



def solveCplex(instance) :
 # Call the function on a given instance
 c, A, b = MKPpopulate(instance)
 # Define the ranges for variables and constraints
 nCols, nRows = range(len(c)), range(len(b))
 # Create an empty model
 mkp = Model('Mkp')
 # Define decision variables
 x = mkp.binary_var_list(nCols, lb = 0, ub = 1, name = 'x')
 constraints = mkp.add_constraints(sum(A[i][j] * x[j] for j in nCols) <= b[i] for i in nRows)
 profit = mkp.sum(c[j] * x[j] for j in nCols)
 mkp.add_kpi(profit, 'profit')
 objective = mkp.maximize(profit)
 mkp.solve()
 # Reporting results
 mkp.report()
 with open("solutions/sol_"+instance.split("/")[1], "w") as solfile:
    solfile.write(mkp.solution.to_string())




if __name__ == '__main__':
    if len(sys.argv) == 1:
        solveCplex("istances/mknapcb1_1.txt")
    elif len(sys.argv) == 2:
        solveCplex(sys.argv[1])
    else:
        print("type  ::::python solver.py TESTNAME.txt::::")
