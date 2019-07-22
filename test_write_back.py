import team18_project1

# def test_initial():
#     assert team18_project1.accessMem(1) == 2
def test_alu():
    wb = team18_project1.writeBack()

    team18_project1.postAluBuff[0] = 100
    team18_project1.postAluBuff[1] = 0

    wb.run()

    assert team18_project1.reg[0] == 100

def test_mem():
    wb = team18_project1.writeBack()

    team18_project1.postMemBuff[0] = 100
    team18_project1.postMemBuff[1] = 0

    wb.run()

    assert team18_project1.reg[0] == 100

def test_alu_and_mem():

    wb = team18_project1.writeBack()

    team18_project1.postAluBuff[0] = 100
    team18_project1.postAluBuff[1] = 0

    team18_project1.postMemBuff[0] = 50
    team18_project1.postMemBuff[1] = 10

    wb.run()

    assert team18_project1.reg[0] == 100
    assert team18_project1.reg[10] == 50


def test_alu_and_mem_reset():

    wb = team18_project1.writeBack()

    team18_project1.postAluBuff[0] = 100
    team18_project1.postAluBuff[1] = 0

    team18_project1.postMemBuff[0] = 50
    team18_project1.postMemBuff[1] = 10

    wb.run()

    assert team18_project1.postAluBuff[0] == -1
    assert team18_project1.postAluBuff[1] == -1

    assert team18_project1.postMemBuff[0] == -1
    assert team18_project1.postMemBuff[1] == -1




