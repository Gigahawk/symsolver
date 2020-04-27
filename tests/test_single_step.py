from sympy import symbols, Eq
from symsolver.symsolver import SymSolver


def test_single_step():
    x, y, z = symbols("x y z")
    expr = x + z
    relations = set((Eq(z, y), ))
    solver = SymSolver(relations=relations, wanted_symbols=(x, y))
    assert solver.solve(expr) == x + y
