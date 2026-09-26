"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"features","tiles"}:
        return False
    m,tiles = target["features"],target["tiles"]
    return (type(m) is int and m >= 0 and isinstance(tiles,list) and len(tiles) >= 1
            and all(isinstance(tile,list)
                    and all(type(f) is int and 0 <= f < m for f in tile)
                    and len(tile) == len(set(tile)) for tile in tiles))


def initial_masks(target):
    return tuple(sum(1 << f for f in tile) for tile in target["tiles"])


def move(masks,current,next_tile):
    if current == next_tile:
        return None
    common = masks[current] & masks[next_tile]
    if not common:
        return None
    updated = list(masks)
    updated[current] &= ~common
    updated[next_tile] &= ~common
    return tuple(updated)


def direct_path(target,path):
    n = len(target["tiles"])
    if (not isinstance(path,list) or not path
            or any(type(tile) is not int or not 0 <= tile < n for tile in path)):
        return False
    masks = initial_masks(target)
    for current,next_tile in zip(path,path[1:]):
        masks = move(masks,current,next_tile)
        if masks is None:
            return False
    return not any(masks)


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal Tiles instance")
    outputs = []
    seen_failures = set()

    def search(current,masks,path):
        if len(outputs) >= limit:
            return True
        if not any(masks):
            outputs.append({"path":path})
            return True
        key = current,masks
        if key in seen_failures:
            return False
        found = False
        for next_tile in range(len(masks)):
            new_masks = move(masks,current,next_tile)
            if new_masks is not None:
                found = search(next_tile,new_masks,path+[next_tile]) or found
        if not found:
            seen_failures.add(key)
        return found

    masks = initial_masks(target)
    for start in range(len(masks)):
        search(start,masks,[start])
        if len(outputs) >= limit:
            break
    for output in outputs:
        assert direct_path(target,output["path"])
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"path"} and direct_path(target,output["path"])


def breadth_first_exists(target):
    masks = initial_masks(target)
    frontier = {(start,masks) for start in range(len(masks))}
    visited = set(frontier)
    while frontier:
        if any(not any(state) for _,state in frontier):
            return True
        following = set()
        for current,state in frontier:
            for next_tile in range(len(state)):
                new_state = move(state,current,next_tile)
                pair = next_tile,new_state
                if new_state is not None and pair not in visited:
                    following.add(pair)
                    visited.add(pair)
        frontier = following
    return False


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    import random
    yes,no = 0,0
    for seed in range(150):
        rng = random.Random(seed)
        m,n = rng.randint(0,4),rng.randint(1,5)
        tiles = [[f for f in range(m) if rng.randrange(2)] for _ in range(n)]
        target = {"features":m,"tiles":tiles}
        answer = solve_target(target)
        exists = breadth_first_exists(target)
        assert ("path" in answer) == exists
        assert valid_target(target,answer)
        yes += exists
        no += not exists
    print(f"Self-test passed: {len(cases)} source formulas and {yes} YES/{no} NO target puzzles")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
