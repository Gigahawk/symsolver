from sympy import Eq, symbols
from symsolver.symsolver import SymSolver


def test_trivial_solution():
    x, y = symbols("x y")
    solver = SymSolver(wanted_symbols=(x, y))
    eq = Eq(x, y)
    assert solver.solve(eq) == eq
