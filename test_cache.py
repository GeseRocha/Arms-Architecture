import team18_project1

# def test_initial():
#     assert team18_project1.accessMem(1) == 2

# Tests R instructions
def test_rType_instructions():

    results = team18_project1.accessMem(-1, 0, 0, 0)

    assert results[0] == False
    assert results[1] == 0

    results = team18_project1.accessMem(-1, 1, 0, 0)

    assert results[0] == True
    assert team18_project1.cacheSets[0][0][3] == '10010001000000000001000000100001'
    assert team18_project1.cacheSets[0][0][4] == '10010001000000000001010001000010'

    results = team18_project1.accessMem(-1, 2, 0, 0)

    assert results[0] == False
    assert results[1] == 0

    results = team18_project1.accessMem(-1, 3, 0, 0)

    assert results[0] == True
    assert team18_project1.cacheSets[1][0][3] == '10001011000000100000000000100011'
    assert team18_project1.cacheSets[1][0][4] == '11001011000000100000000000100100'

    print team18_project1.cacheSets

# TODO test memory instructions




    