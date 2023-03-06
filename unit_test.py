import unittest
from search import InformedSearch, get_next_states


class StateGenerator(unittest.TestCase):
    def test_state_generator(self):
        capacities = (2, 5, None)
        state = (0, 0, 0)
        known_states = [(2, 0, 0), (0, 5, 0)]
        self.assertEqual(set(known_states),set(get_next_states(state, capacities)))

        state = (0, 5, 0)
        known_states = [(2, 5, 0), (2, 3, 0), (0, 0, 5), (0, 0, 0)]
        self.assertEqual(set(known_states),set(get_next_states(state, capacities)))

        state = (2, 0, 0)
        known_states = [(0, 0, 0), (0, 2, 0), (0, 0, 2), (2, 5, 0)]
        self.assertEqual(set(known_states),set(get_next_states(state, capacities)))

        state = (2, 5, 0)
        known_states = [(0, 5, 0), (2, 0, 0), (0, 5, 2), (2, 0, 5)]
        self.assertEqual(set(known_states),set(get_next_states(state, capacities)))

        state = (2, 3, 5)
        known_states = [(0, 3, 5), (2, 0, 5), (2, 3, 0), (0, 5, 5), (0, 3, 7), (2, 0, 8), (2, 5, 3), (2, 5, 5)]
        self.assertEqual(set(known_states),set(get_next_states(state, capacities)))


class FileTest(unittest.TestCase):

    def test_1(self):
        s = InformedSearch.from_file('data/input1.txt', heuristic=InformedSearch.get_heuristic)
        result = s.a_star_search()
        s.print_problem()
        self.assertEqual(result, 7, "Should be 7")

    def test_2(self):
        s = InformedSearch.from_file('data/input2.txt', heuristic=InformedSearch.get_heuristic)
        s.print_problem()
        result = s.a_star_search()
        self.assertEqual(result, -1, "Should be no solution")

    def test_3(self):
        s = InformedSearch.from_file('data/input3.txt', heuristic=InformedSearch.get_heuristic)
        s.print_problem()
        result = s.a_star_search()
        self.assertEqual(result, -1, "Is no solution")

    def test_4(self):
        s = InformedSearch.from_file('data/input4.txt', heuristic=InformedSearch.get_heuristic)
        result = s.a_star_search()
        s.print_problem()
        self.assertEqual(result, 36, "Should be 36")
    
    def test_5(self):
        s = InformedSearch.from_file('data/input5.txt', heuristic=InformedSearch.get_heuristic)
        result = s.a_star_search()
        s.print_problem()
        self.assertEqual(result, 5, "Should be 5")
            
    def test_8(self):
        s = InformedSearch.from_file('data/input8.txt', heuristic=InformedSearch.get_heuristic)
        result = s.a_star_search()
        s.print_problem()
        self.assertEqual(result, 19, "Should be 19")
    

unittest.main()