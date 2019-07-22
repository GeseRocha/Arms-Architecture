import team18_project1

# def test_initial():
#     assert team18_project1.accessMem(1) == 2

def test_addi():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 0

    alu.run()

    assert team18_project1.postAluBuff[0] == 4
    assert team18_project1.postAluBuff[1] == 0

def test_add():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 2
    team18_project1.reg[1] = 4
    team18_project1.reg[2] = 5

    alu.run()

    assert team18_project1.postAluBuff[0] == 9
    assert team18_project1.postAluBuff[1] == 2

def test_sub():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 3
    team18_project1.reg[1] = 4
    team18_project1.reg[2] = 5

    alu.run()

    assert team18_project1.postAluBuff[0] == -1
    assert team18_project1.postAluBuff[1] == 3

def test_and():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 4
    team18_project1.reg[1] = 4
    team18_project1.reg[2] = 5

    alu.run()

    assert team18_project1.postAluBuff[0] == 4
    assert team18_project1.postAluBuff[1] == 4

def test_orr():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 5
    team18_project1.reg[1] = 4
    team18_project1.reg[2] = 5

    alu.run()

    assert team18_project1.postAluBuff[0] == 5
    assert team18_project1.postAluBuff[1] == 5

def test_eor():
    
    alu = team18_project1.ALU()

    team18_project1.preAluBuff[0] = 6
    team18_project1.reg[1] = 4
    team18_project1.reg[2] = 5

    alu.run()

    

    assert team18_project1.postAluBuff[0] == 1
    assert team18_project1.postAluBuff[1] == 6