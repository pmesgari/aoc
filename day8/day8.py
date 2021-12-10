import sys, enum


DIGIT_TO_SEGMENTS = {
    0: {"TH", "BH", "RTV", "RBV", "LTV", "LBV"},
    1: {"RTV", "RBV"},
    2: {"TH", "RTV", "MH", "LBV", "BH"},
    3: {"TH", "RTV", "MH", "RBV", "BH"},
    4: {"LTV", "MH", "RTV", 'RBV'},
    5: {'TH', 'LTV', 'MH', 'RBV', 'BH'},
    6: {'TH', 'LTV', 'LBV', 'MH', 'BH', 'RBV'},
    7: {'TH', 'RTV', 'RBV'},
    8: {'TH', 'MH', 'BH', 'LTV', 'LBV', 'RTV', 'RBV'},
    9: {'TH', 'MH', 'BH', 'RTV', 'RBV', 'LTV'},
}


def diff(a, b):
    return list(set(a) - set(b))


def signals_to_segments(configuration, signals):
    segments = []
    for sig in signals:
        segment = [configuration.get(c) for c in sig]
        segments.append(segment)
    return segments


def segments_to_digits(segments):
    digits = []
    for seg in segments:
        for key, value in DIGIT_TO_SEGMENTS.items():
            if set(value) == set(seg):
                digits.append(key)

    return digits


def decode(signals):
    configuration = {}
    patterns = {}
    six_digits = []
    five_digits = []
    for sig in signals:
        if len(sig) == 2:
            patterns["1"] = sig
        elif len(sig) == 3:
            patterns["7"] = sig
        elif len(sig) == 4:
            patterns["4"] = sig
        elif len(sig) == 7:
            patterns["8"] = sig
        elif len(sig) == 6:
            six_digits.append(sig)
        elif len(sig) == 5:
            five_digits.append(sig)

    three = ''
    for sig in five_digits:
        if len(set(sig).intersection(patterns["1"])) == 2:
            three = sig

    six = ''
    for sig in six_digits:
        if len(set(sig).intersection(patterns["7"])) == 2:
            six = sig

    remaining_six_digits = [d for d in six_digits if d != six]

    TH = diff(patterns["7"], patterns["1"])[0]
    configuration[TH] = "TH"

    MH = list(set(diff(three, patterns["7"])).intersection(three, patterns["4"]))[0]
    configuration[MH] = "MH"

    BH = list(set(diff(three, patterns["7"])).difference(MH))[0]
    configuration[BH] = "BH"

    LTV = list(set(diff(patterns["4"], patterns["7"])).difference(MH))[0]
    configuration[LTV] = "LTV"

    RTV = list(set(diff(remaining_six_digits[0], six)))[0]
    configuration[RTV] = "RTV"

    RBV = list(set(diff(patterns["1"], RTV)))[0]
    configuration[RBV] = "RBV"

    LBV = list(set(diff("abcdefg", ''.join([key for key, _ in configuration.items()]))))[0]
    configuration[LBV] = "LBV"

    return configuration


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        data = [(x.split(' | ')[0].split(' '), x.split(' | ')[1].rstrip('\n').split(' ')) for x in f.readlines()]

    count = 0
    for d in data:
        for dig in d[1]:
            if len(dig) in [2, 3, 4, 7]:
                count += 1
    print(count)

    # configuration = decode(["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"])
    # segments = signals_to_segments(configuration, ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'])
    # digits = segments_to_digits(segments)

    digits = []
    for d in data:
        configuration = decode(d[0])
        segments = signals_to_segments(configuration, d[1])
        digits.append(int(''.join([str(x) for x in segments_to_digits(segments)])))

    print(sum(digits))

    from itertools import *

    _digits = {
        7: "acf"
    }

    for p in permutations(list(range(8))):
        D = {}
        for i in range(8):
            D[chr(ord('a') + i)] = chr(ord('a') + p[i])
        for w in ["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"]:
            w_perm = ''
            for c in w:
                w_perm += D[c]
            w_perm = ''.join(sorted(w_perm))

            ok = False
            if w_perm in _digits.values():
                ok = True

        if ok:
            print(D)