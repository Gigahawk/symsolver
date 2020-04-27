from sympy import Eq, solve, Expr

from symsolver.errors import UnsolveableException


class EqTree:
    def __init__(self, expr: Expr, parent=None):
        self.__expr = expr
        self.__parent = parent
        self.__children = set()
    
    def add_child(self, expr: Expr) -> bool:
        """Add a child expression to the node

        Returns:
            bool: True if a unique expression was added
        """
        # children must be unique from the parent
        if self.parent and self.parent.expr == expr:
            return False
        l = len(self.__children)
        self.__children.add(expr)
        return l < len(self.__children)

    @property
    def expr(self):
        return self.__expr
    
    @property
    def parent(self):
        return self.__parent
    
    @property
    def children_exprs(self):
        return self.__children
    
    @property
    def children(self):
        return (EqTree(expr, parent=self) for expr in self.children_exprs)


class SymSolver:
    def __init__(self, relations=set(), wanted_symbols=set()):
        self.relations = relations
        self.wanted_symbols = wanted_symbols
        self.__found_expressions = set()
    
    def solve(self, expr: Expr) -> Expr:
        self.__found_expressions = set()
        print(f"Solving expression {expr}")
        if self._solved(expr):
            print(f"Got solution {expr}")
            return expr
        root_node = EqTree(expr)
        if solution := self._propagate_tree(root_node):
            print(f"Got solution {solution}")
            return solution
        raise UnsolveableException("No solutions found")

    def _propagate_tree(self, node: EqTree):
        for child_eq in self._get_node_children(node):
            print(f"Got child expression {child_eq}")
            if self._solved(child_eq):
                return child_eq
            if child_eq in self.__found_expressions:
                print(f"Expression was a duplicate")
                continue
            self.__found_expressions.add(child_eq)
            node.add_child(child_eq)
        
        # Sort children by most promising and shortest
        sorted_children = sorted(
            sorted(node.children, key=lambda x: len(x.expr.free_symbols)),
            key=lambda x: len(set.intersection(x.expr.free_symbols, self.wanted_symbols)),
            reverse=True)
        for child in sorted_children:
            if solution := self._propagate_tree(child):
                return solution
        return None
    
    def _get_node_children(self, node: EqTree):
        expr = node.expr
        expr_syms = expr.free_symbols
        # print(f"Getting children for {expr}")
        intersections = map(
            lambda x: (x, set.intersection(expr_syms, x.free_symbols)), self.relations)
        intersections = filter(lambda x: x[1], intersections)
        for i in intersections:
            # print(f"Found intersection {i}")
            rel_expr = i[0]
            rel_expr_syms = i[1]
            for sym in rel_expr_syms:
                solved_rel_expr = solve(rel_expr, sym)[0]
                # print(f"Substituting {sym} in {expr} with {solved_rel_expr}")
                yield expr.subs(sym, solved_rel_expr)
    
    def _solved(self, expr: Expr) -> bool:
        """Returns True if expr contains only wanted_symbols"""
        return not set.difference(expr.free_symbols, self.wanted_symbols)
        