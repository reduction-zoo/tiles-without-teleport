from check import legal_target,solve_target,valid_target


def test_hand_cases():
    pair = {"features":1,"tiles":[[0],[0]]}
    assert valid_target(pair,{"path":[0,1]})
    assert not valid_target(pair,{"path":[0,0]})
    assert solve_target({"features":1,"tiles":[[0]]}) == {"status":"NO-SOLUTION"}
    assert valid_target({"features":0,"tiles":[[]]},{"path":[0]})
    assert not legal_target({"features":1,"tiles":[[0,0]]})
    chain = {"features":2,"tiles":[[0],[0,1],[1]]}
    assert valid_target(chain,{"path":[0,1,2]})


if __name__ == "__main__":
    test_hand_cases()
