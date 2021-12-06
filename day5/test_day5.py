from day5.day5 import line_to_point, Board


def test_horizontal_line_to_points():
    line = [(0, 9), (5, 9)]
    expected_points = [
        (0, 9),
        (1, 9),
        (2, 9),
        (3, 9),
        (4, 9),
        (5, 9)
    ]

    assert set(line_to_point(line[0], line[1])) == set(expected_points)
    assert set(line_to_point(line[1], line[0])) == set(expected_points)


def test_vertical_line_to_points():
    line = [(1, 1), (1, 3)]
    expected_points = [
        (1, 1),
        (1, 2),
        (1, 3)
    ]
    assert set(line_to_point(line[0], line[1])) == set(expected_points)
    assert set(line_to_point(line[1], line[0])) == set(expected_points)


def test_diagonal_line_to_points():
    line = [(9, 7), (7, 9)]
    expected_points = [
        (9, 7),
        (8, 8),
        (7, 9)
    ]
    assert set(line_to_point(line[0], line[1])) == set(expected_points)
    assert set(line_to_point(line[1], line[0])) == set(expected_points)


def test_count_overlapping_lines():
    lines = [
        [(0, 9), (5, 9)],
        [(8, 0), (0, 8)],
        [(9, 4), (3, 4)],
        [(2, 2), (2, 1)],
        [(7, 0), (7, 4)],
        [(6, 4), (2, 0)],
        [(0, 9), (2, 9)],
        [(3, 4), (1, 4)],
        [(0, 0), (8, 8)],
        [(5, 5), (8, 2)]
    ]
    board = Board()

    for line in lines:
        points = line_to_point(line[0], line[1])
        for point in points:
            board.mark(point[0], point[1])

    overlap_count = board.overlap_count()
    assert overlap_count == 12