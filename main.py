import glob
from search import InformedSearch


results = {}
for file in glob.glob('data/*.txt'):
    print(file.split('/')[1])
    
    s = InformedSearch.from_file(file, heuristic = InformedSearch.get_heuristic)
    s.print_problem()
    steps = s.a_star_search()
    results[file] = steps

    print(f"Steps required: {steps}")
    print()
    print()

for file, steps in results.items():
    print(f"{file.split('/')[1]} = {steps}")