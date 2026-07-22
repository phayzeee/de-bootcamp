from week01.practice.translations import squares, initials

def test_square():
    assert squares() == [4, 16, 36, 64, 100]

def test_get_squares_length():
    assert len(squares()) == 5

def test_initials_two_words():
    assert initials("John Doe") == "JD"