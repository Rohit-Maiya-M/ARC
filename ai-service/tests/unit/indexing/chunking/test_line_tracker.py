from app.indexing.chunking.line_tracker import LineTracker


def test_single_line():

    tracker = LineTracker()

    text = "hello world"

    offsets = [
        (0, 5),
        (6, 11),
    ]

    start, end = tracker.get_line_range(
        text,
        offsets,
        0,
        2,
    )

    assert start == 1
    assert end == 1


def test_multiple_lines():

    tracker = LineTracker()

    text = "one\ntwo\nthree"

    offsets = [
        (0, 3),
        (4, 7),
        (8, 13),
    ]

    start, end = tracker.get_line_range(
        text,
        offsets,
        0,
        3,
    )

    assert start == 1
    assert end == 3