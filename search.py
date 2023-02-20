import heapq
from typing import List, Tuple, Callable
import math


def is_goal(state, target):
    return state.state[-1] == target

def parse_file(filename):
    with open(filename, "r") as file:
        text = file.read()
    pitchers, target = text.split("\n")
    pitchers = [int(b) for b in pitchers.split(",")]
    target = int(target)
    return tuple(pitchers + [None]), target

class State:
    def __init__(self, state: Tuple[int], capacities: Tuple[int], path: List=None):
        self._state = state
        self.capacities = capacities
        if path is None:
            path = []
        self.path = path
        self.cost = len(self.path)
    
    @property
    def state(self):
        return self._state
    
    def __repr__(self):
        return {self._state}

    def __lt__(self, other):
        return self._state < other._state

    def get_next_states(self, seen = set()):
        next_states = []
        states = get_next_states(self._state, self.capacities)
        for state in states:
            if state in seen:
                continue
            path = list(self.path)
            path.append(self._state)
            next_states.append(State(state, self.capacities, path))
        return next_states


class InformedSearch:
    def __init__(self, capacities: Tuple[int], target: int = None, heuristic: Callable = None):
        self.capacities = tuple(sorted([cap for cap in capacities if cap is not None]) + [None])
        self.target = target
        self.heuristic = heuristic
        self.visited = set()
        self.pq = []
        heapq.heappush(self.pq, (0, State((0,) * len(capacities), self.capacities)))
        self.solution_state = None
        self.shortest_path = None

    def __repr__(self):
        return f"<InformedSearch{self.solution_state or ''}>"
        
    def solution_possible(self, capacities, target):
        gcd = capacities[0]
        
        for i in range(1, len(capacities) -1):
            gcd = math.gcd(gcd, capacities[i])
            if target % gcd == 0:
                return True
            
        if target % gcd == 0:
            return True
        
        return False
    
    def a_star_search(self, heuristic = None, target = None, check_admissible = True):
        # if no solution possible then return -1
        if not self.solution_possible(self.capacities, self.target):
            return -1
        
        # if target not specified
        if self.target is None and target is None :
            raise AttributeError("No target value specified. Pass the `target` argument to the search method.")
        
        if heuristic is None:
            heuristic = self.heuristic
            
        elif self.heuristic is None:
            self.heuristic = heuristic
            
        target = target or self.target
        solution = -1
        
        while self.pq:
            state = heapq.heappop(self.pq)[1]
            # final state reached
            if is_goal(state, target):
                solution = state.cost
                self.solution_state = state
                break

            self.calc_cost(heuristic, state, target, check_admissible)
            self.visited.add(state.state)
        
        # check if heuristoc is admissible while still perofrming the search            
        if solution != -1 and check_admissible:
            self.check_admissibility(self.solution_state, heuristic, solution)
            
        self.shortest_path = solution
        return solution

    def get_heuristic(state: Tuple[int], capacities: Tuple[int], target: int):
        h = abs(target - state[-1])
        space_available = [capacity - pitcher for capacity, pitcher in zip(capacities[:-1], state[:-1])]
        
        # target state
        if h == 0: 
            return 0
        
        # there is a pitcher with exact amount of water to reach the target state
        if h in state[:-1]:
            return 1
        
        # the infinite pitcher has more water than the target
        if h < 0:
            if h not in space_available: 
                return 2
            return 1

        pitcher_fills_to_repeat_state = len([pitcher for pitcher in state[:-1] if pitcher != 0])
        current_volumetric_potential = sum(state[:-1])
        closest_capacity_to_h = min(capacities[:-1], key = lambda x:abs(x-h))
        steps_to_repeat_state = pitcher_fills_to_repeat_state * 2 - 1

        # only full pitcher poured into the infinite pitcher
        if current_volumetric_potential == 0:
            return max(2*(h/closest_capacity_to_h), 2)
        
        return max(h/current_volumetric_potential * steps_to_repeat_state, 1)
            
    @classmethod
    def from_file(cls, filename, heuristic = None):
        capacities, target = parse_file(filename)
        return cls(capacities = capacities, target = target, heuristic = heuristic)

    def check_admissibility(self, state, heuristic, solution):
        # inadmissible heuristic
        if heuristic(state.state, self.capacities, self.target) != 0:
            return False
        
        for st in state.path:
            value = heuristic(st, self.capacities, self.target)
            # inadmissible heuristic
            if value > solution:
                return False
            # print("Heuristic seems admissible")
        return True

    def calc_cost(self, heuristic, state, target, check_admissible):
        for st in state.get_next_states():
            if not st.state in self.visited:
                if is_goal(state, target) and check_admissible:
                    self.check_admissibility(state, heuristic, st.cost)
                self.visited.add(st.state)
                h = heuristic(st.state, self.capacities, target)
                cost = h + st.cost
                heapq.heappush(self.pq, (cost, st))
        
    def h_is_admissible(self):
        return self.check_admissibility(self.solution_state, self.heuristic, self.shortest_path)
    
    def print_problem(self):
        print('='*40)
        print(f"Capacities: {self.capacities[:-1]}")
        print(f"Target: {self.target}")
        

# generate child states from a given state
def get_next_states(state: Tuple[int], capacities = Tuple[int]):
    next_states = []
    seen_next_states = {state}
    
    for ix, bx in enumerate(state):
        
        # empty the pitcher
        if bx != 0 or capacities[ix] is None:
            tmp_state = list(state)
            tmp_state[ix] = 0
            tmp_state = tuple(tmp_state)
            if not tmp_state in seen_next_states:
                seen_next_states.add(tmp_state)
                next_states.append(tmp_state)
    
        # fill the pitcher
        if capacities[ix] is not None and bx < capacities[ix]:
            tmp_state = list(state)
            tmp_state[ix] = capacities[ix]
            tmp_state = tuple(tmp_state)
            if not tmp_state in seen_next_states:
                seen_next_states.add(tmp_state)
                next_states.append(tmp_state)
    
        # skip the pitcher
        if bx == 0:
            continue
    
        calc_pitcher_combos(state, capacities,  next_states, seen_next_states, ix, bx)
    return next_states

# generate states to pour from one pitcher to another
def calc_pitcher_combos(state, capacities,  next_states, seen_next_states, ix, bx):
    for iy, by in enumerate(state): 
        # dont pour from and to the same pitcher
        if ix == iy: 
            continue
    
        capacity_y = capacities[iy]
        y_remaining = capacity_y - by if capacity_y is not None else bx 
        
        # add upto the capacity for the by pitcher
        delta = min(y_remaining, bx)
    
        # pitcher y can take capaciyt_y - by from the bx pitcher
        if capacity_y is None or by < capacity_y:
            tmp_state = list(state)
            tmp_state[ix] = tmp_state[ix] - delta
            tmp_state[iy] = tmp_state[iy] + delta
            tmp_state = tuple(tmp_state)
            if not tmp_state in seen_next_states:
                seen_next_states.add(tmp_state)
                next_states.append(tmp_state)