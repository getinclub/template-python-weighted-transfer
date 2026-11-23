"""Public contract tests; expected costs are computed without the search algorithm."""
import copy
import itertools
import random
import unittest
from transfer import cheapest_cost


def oracle(nodes, edges):
    d = {(a,b): (0 if a == b else None) for a in nodes for b in nodes}
    for a,b,w in edges:
        if d[a,b] is None or w < d[a,b]: d[a,b] = w
    for k in nodes:
        for a in nodes:
            for b in nodes:
                if d[a,k] is not None and d[k,b] is not None:
                    candidate = d[a,k]+d[k,b]
                    if d[a,b] is None or candidate < d[a,b]: d[a,b] = candidate
    return d


class TransferTests(unittest.TestCase):
    def test_fixture(self):
        self.assertEqual(cheapest_cost(['ingest','relay','archive'], [('ingest','archive',90),('ingest','relay',15),('relay','archive',20)],'ingest','archive'),35)
    def test_unreachable(self):
        self.assertIsNone(cheapest_cost(['a','b'], [], 'a','b'))
    def test_direction(self):
        self.assertIsNone(cheapest_cost(['a','b'], [('a','b',3)],'b','a'))
    def test_self_route(self):
        self.assertEqual(cheapest_cost(['a'], [('a','a',9)],'a','a'),0)
    def test_parallel(self):
        self.assertEqual(cheapest_cost(['a','b'], [('a','b',99),('a','b',2)],'a','b'),2)
    def test_zero_cycle(self):
        self.assertEqual(cheapest_cost(['a','b','c'], [('a','b',0),('b','a',0),('b','c',0)],'a','c'),0)
    def test_revised_cost(self):
        self.assertEqual(cheapest_cost(['a','b','c','d'], [('a','b',10),('a','c',1),('c','b',1),('b','d',1),('c','d',20)],'a','d'),3)
    def test_large_integer(self):
        n=10**300
        self.assertEqual(cheapest_cost(['a','b','c'], [('a','c',n+3),('a','b',n),('b','c',1)],'a','c'),n+1)
    def test_input_preserved(self):
        nodes=['b','a','c']; edges=[('a','b',4),('b','c',7)]
        before=copy.deepcopy((nodes,edges))
        for source in nodes:
            for target in nodes: cheapest_cost(nodes,edges,source,target)
        self.assertEqual((nodes,edges),before)
    def test_calls_independent(self):
        self.assertEqual(cheapest_cost(['a','b'], [('a','b',2)],'a','b'),2)
        self.assertIsNone(cheapest_cost(['a','b'], [],'a','b'))
    def test_edge_order(self):
        nodes=['a','b','c']; edges=[('a','c',7),('a','b',1),('b','c',2),('a','b',8)]
        for order in itertools.permutations(edges):
            self.assertEqual(cheapest_cost(nodes,list(order),'a','c'),3)
    def test_invalid_nodes(self):
        for nodes in [None,{},('a',),[],[''],['a','a'],['a',False],['a',[]],['a',1]]:
            with self.subTest(nodes=nodes),self.assertRaises(ValueError): cheapest_cost(nodes,[],'a','a')
    def test_invalid_endpoints(self):
        for s,t in [('x','a'),('a','x'),(True,'a'),('a',None),([], 'a')]:
            with self.subTest(source=s,target=t),self.assertRaises(ValueError): cheapest_cost(['a'],[],s,t)
    def test_invalid_edge_container(self):
        for edges in [None,{},(),iter([]), '']:
            with self.subTest(edges=edges),self.assertRaises(ValueError): cheapest_cost(['a'],edges,'a','a')
    def test_invalid_edges(self):
        for edge in [None,[],['a','b',1],('a','b'),('a','b',1,2),('a','x',1),([], 'b',1),('a','b',True),('a','b',-1),('a','b',1.0),('a','b','1')]:
            with self.subTest(edge=edge),self.assertRaises(ValueError): cheapest_cost(['a','b'],[edge],'a','b')
    def test_validate_before_self_return(self):
        with self.assertRaises(ValueError): cheapest_cost(['a','b'],[('b','b',-1)],'a','a')
    def test_validate_disconnected_edges(self):
        with self.assertRaises(ValueError): cheapest_cost(['a','b','c'],[('a','b',1),('c','c',False)],'a','b')
    def test_random_oracle(self):
        rng=random.Random(131126)
        for case in range(300):
            nodes=[str(i) for i in range(rng.randrange(1,9))]
            edges=[(rng.choice(nodes),rng.choice(nodes),rng.randrange(0,31)) for _ in range(rng.randrange(0,45))]
            expected=oracle(nodes,edges)
            for (s,t),cost in expected.items():
                with self.subTest(case=case,source=s,target=t): self.assertEqual(cheapest_cost(nodes,edges,s,t),cost)
    def test_exhaustive_small_graphs(self):
        nodes=['a','b','c']; pairs=[(a,b) for a in nodes for b in nodes if a!=b]
        for weights in itertools.product([None,0,2], repeat=6):
            edges=[(a,b,w) for (a,b),w in zip(pairs,weights) if w is not None]
            expected=oracle(nodes,edges)
            for (s,t),cost in expected.items(): self.assertEqual(cheapest_cost(nodes,edges,s,t),cost)
    def test_sparse_smoke(self):
        nodes=[str(i) for i in range(6000)]
        edges=[(nodes[i],nodes[i+1],1) for i in range(5999)] + [(nodes[0],nodes[-1],9000)]
        self.assertEqual(cheapest_cost(nodes,edges,nodes[0],nodes[-1]),5999)

if __name__ == '__main__': unittest.main()
