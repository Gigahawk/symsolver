from sympy import Eq, symbols
from symsolver.symsolver import SymSolver
from symsolver.errors import UnsolveableException


def test_no_solution():
    x, y, z = symbols("x y z")
    solver = SymSolver(wanted_symbols=(x, z))
    eq = Eq(x, y)
    try:
        solver.solve(eq)
        assert False
    except UnsolveableException:
        pass
    
