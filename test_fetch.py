import team18_project1

def test_cycle_two_buffer():
    fetch = team18_project1.fetchUnit()
    
    for i in range(2):
        fetch.run()

    firstInstruction = team18_project1.preIssueBuff[0]
    secondInstruction = team18_project1.preIssueBuff[1]
    thirdInstruction = team18_project1.preIssueBuff[2]
    fourthInstruction = team18_project1.preIssueBuff[3]
    
    assert firstInstruction == 0 and secondInstruction == 1 and thirdInstruction == -1 and fourthInstruction == -1

def test_cycle_two_cache():
    fetch = team18_project1.fetchUnit()
    
    for i in range(2):
        fetch.run()

    firstWord = team18_project1.cacheSets[0][0][3]
    secondWord = team18_project1.cacheSets[0][0][4]
    
    
    assert firstWord == '10010001000000000001000000100001' and secondWord == '10010001000000000001010001000010'


def test_one():

    testBool = True

    if 4 in team18_project1.preIssueBuff:
        testBool = True
    else:
        testBool = False

    assert testBool == False