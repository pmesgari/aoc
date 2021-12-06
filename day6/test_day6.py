from day6.day6 import LanternFishSchool


def test_after_one_cycle():
    school = LanternFishSchool([3, 4, 3, 1, 2])

    assert set(school.next()) == {2, 3, 2, 0, 1}
    assert set(school.next()) == {1, 2, 1, 6, 0, 8}
    assert set(school.next()) == {0, 1, 0, 5, 6, 7, 8}


def test_after_a_few_days():
    school = LanternFishSchool([3, 4, 3, 1, 2])

    for i in range(5):
        school.next()
        print(f"After {i} days: {','.join([str(timer) for timer in school.fishes])}")

