from pytoolkit.datatypes.lrucachedict import LRUCacheOrderedDict


def test_lrucacheordereddict():
    maxsize = 1024
    d = LRUCacheOrderedDict(maxsize)
    assert len(d) == 0, d

    d[0] = 9
    assert d[0] == 9
    assert len(d) == 1

    assert d.pop(0) == 9, d

    assert len(d) == 0
    for n in range(maxsize):
        d[n] = n

    for n in range(maxsize, maxsize * 3):
        d[n] = n
        assert len(d) == maxsize
