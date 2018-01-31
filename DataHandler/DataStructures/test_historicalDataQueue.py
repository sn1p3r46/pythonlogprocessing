from historicalDataQueue import HistoricalDataQueue as HDQ
import numpy as np
from random import randint, sample
import pytest
import warnings


def test_empty_queue():
    hdq = HDQ(iterable=(), maxlen=0)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 0
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 0


def test_nan_not_full_queue():
    hdq = HDQ(iterable=([np.nan]*5), maxlen=6)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 5
    assert len(hdq) == 5


def test_num_not_full_queue():
    hdq = HDQ(iterable=(range(5)), maxlen=6)
    assert hdq.sum == 10
    assert hdq.sqr_sum == 30
    assert hdq.maxlen == 6
    assert not np.isnan(hdq.mean)
    assert not np.isnan(hdq.std)
    assert hdq.NaNCounter == 0
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert len(hdq) == 5


def test_nan_full_queue():
    hdq = HDQ(iterable=([np.nan]*5), maxlen=5)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 5
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 5
    assert len(hdq) == 5


def test_num_full_queue():
    hdq = HDQ(iterable=(range(5)), maxlen=5)
    assert hdq.sum == 10
    assert hdq.sqr_sum == 30
    assert hdq.maxlen == 5
    assert not np.isnan(hdq.mean)
    assert not np.isnan(hdq.std)
    assert hdq.NaNCounter == 0
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert len(hdq) == 5


def test_nan_full_queue_exceed():
    hdq = HDQ(iterable=([np.nan]*10), maxlen=5)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 5
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 5
    assert len(hdq) == 5


def test_num_full_queue_exceed():
    hdq = HDQ(iterable=(range(10)), maxlen=5)
    assert hdq.sum == 35
    assert hdq.sqr_sum == 255
    assert hdq.maxlen == 5
    assert not np.isnan(hdq.mean)
    assert not np.isnan(hdq.std)
    assert hdq.NaNCounter == 0
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert len(hdq) == 5


def test_nan_filling_queue_appendleft():
    hdq = HDQ(iterable=([np.nan]*5), maxlen=6)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 5
    assert len(hdq) == 5

    hdq.appendleft(np.nan)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 6
    assert len(hdq) == 6

    hdq.appendleft(np.nan)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 6
    assert len(hdq) == 6


def test_num_filling_queue_appendleft():
    hdq = HDQ(iterable=range(5), maxlen=6)
    assert hdq.sum == 10
    assert hdq.sqr_sum == 30
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 5

    hdq.appendleft(5)
    assert hdq.sum == 15
    assert hdq.sqr_sum == 55
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 6

    hdq.appendleft(6)
    assert hdq.sum == 17
    assert hdq.sqr_sum == 75
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 6


def test_nan_filling_queue_append():
    hdq = HDQ(iterable=([np.nan]*5), maxlen=6)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 5
    assert len(hdq) == 5

    hdq.append(np.nan)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert hdq.maxlen == 6
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.NaNCounter == 6
    assert len(hdq) == 6

    hdq.append(np.nan)
    assert np.isnan(hdq.sum)
    assert np.isnan(hdq.sqr_sum)
    assert np.isnan(hdq.mean)
    assert np.isnan(hdq.std)
    assert hdq.maxlen == 6
    assert hdq.NaNCounter == 6
    assert len(hdq) == 6


def test_num_filling_queue_append():
    hdq = HDQ(iterable=range(5), maxlen=6)
    assert hdq.sum == 10
    assert hdq.sqr_sum == 30
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 5

    hdq.append(5)
    assert hdq.sum == 15
    assert hdq.sqr_sum == 55
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 6

    hdq.append(6)
    assert hdq.sum == 21
    assert hdq.sqr_sum == 91
    assert hdq.maxlen == 6
    assert hdq.mean == np.nanmean(hdq)
    assert hdq.std == np.nanstd(hdq)
    assert hdq.NaNCounter == 0
    assert len(hdq) == 6


def test_nan_filling_queue_nan_from_len0_appendleft():
    hdq = HDQ(iterable=(), maxlen=5)
    for i in range(5):
        hdq.appendleft(np.nan)
        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert np.isnan(hdq.mean)
        assert np.isnan(hdq.std)
        assert hdq.maxlen == 5
        assert len(hdq) == i+1
        assert hdq.NaNCounter == i+1


def test_num_filling_queue_num_from_len0_appendleft():
    hdq = HDQ(iterable=(), maxlen=5)
    for i in range(5):
        hdq.appendleft(i)
        assert hdq.sum == sum(range(i+1))
        assert hdq.sqr_sum == sum([x**2 for x in range(i+1)])
        assert hdq.mean == np.nanmean(hdq)
        assert hdq.std == np.nanstd(hdq)
        assert hdq.maxlen == 5
        assert len(hdq) == i+1
        assert hdq.NaNCounter == 0


def test_nan_filling_queue_from_0_append():
    hdq = HDQ(iterable=(), maxlen=5)
    for i in range(5):
        hdq.append(np.nan)
        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert np.isnan(hdq.mean)
        assert np.isnan(hdq.std)
        assert hdq.maxlen == 5
        assert hdq.NaNCounter == i+1
        assert len(hdq) == i+1


def test_num_filling_queue_from_0_append():
    hdq = HDQ(iterable=(), maxlen=5)
    for i in range(5):
        hdq.append(i)
        assert hdq.sum == sum(range(i+1))
        assert hdq.sqr_sum == sum([x**2 for x in range(i+1)])
        assert hdq.mean == np.nanmean(hdq)
        assert hdq.std == np.nanstd(hdq)
        assert hdq.maxlen == 5
        assert len(hdq) == i+1
        assert hdq.NaNCounter == 0


def test_mixed_not_full():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.mean == 2
    assert hdq.std == 0
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 1
    assert len(hdq) == 3


def test_mixed_not_full_random():
    hdq = HDQ(iterable=(randint(0, 9999999) if x % 2 == 0 else
              np.nan for x in range(3)), maxlen=5)
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 1
    assert len(hdq) == 3


def test_mixed_almost_full():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(4)),
              maxlen=5)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.mean == 2
    assert hdq.std == 0
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 4


def test_mixed_almost_full_random():
    hdq = HDQ(iterable=(randint(0, 9999999) if x % 2 == 0 else
              np.nan for x in range(4)), maxlen=5)
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 4


def test_mixed_full():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)
    assert hdq.sum == 6
    assert hdq.sqr_sum == 12
    assert hdq.mean == 2
    assert hdq.std == 0
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 5


def test_mixed_full_random():
    hdq = HDQ(iterable=(randint(0, 9999999) if x % 2 == 0 else
              np.nan for x in range(5)), maxlen=5)
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 5


def test_mixed_non_full_append_nan():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)

    hdq.append(np.nan)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert hdq.mean == 2
    assert hdq.std == 0
    assert len(hdq) == 4


def test_mixed_random_non_full_append_nan():
    hdq = HDQ(iterable=(randint(0, 9999999) if x % 2 == 0 else
              np.nan for x in range(3)), maxlen=5)

    hdq.append(np.nan)
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 4


def test_mixed_non_full_append_random():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)
    hdq.append(randint(0, 9999999))
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 1
    assert len(hdq) == 4


def test_mixed_non_full_appendleft_nan():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)

    hdq.appendleft(np.nan)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert hdq.mean == 2
    assert hdq.std == 0
    assert len(hdq) == 4


def test_mixed_non_full_appendleft_random():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)
    hdq.appendleft(randint(0, 9999999))
    assert hdq.sum == np.nansum(hdq)
    assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 1
    assert len(hdq) == 4


def test_mixed_non_full_appendleft_num():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(3)),
              maxlen=5)
    hdq.appendleft(2)
    assert hdq.sum == 6
    assert hdq.sqr_sum == 12
    assert hdq.NaNCounter == 1
    assert hdq.std == 0
    assert hdq.mean == 2
    assert hdq.maxlen == 5
    assert len(hdq) == 4


def test_mixed_full_append_nan():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)

    hdq.append(np.nan)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 3
    assert hdq.mean == 2
    assert hdq.std == 0
    assert len(hdq) == 5


def test_mixed_full_append_random():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)
    hdq.append(randint(0, 999999))
    assert hdq.sum == np.nansum(hdq)
    assert np.isclose(hdq.sqr_sum, np.nansum([x**2 for x in hdq]))
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 5


def test_mixed_full_append_num():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)
    hdq.append(2)
    assert hdq.sum == 6
    assert hdq.sqr_sum == 12
    assert hdq.NaNCounter == 2
    assert hdq.std == 0
    assert hdq.mean == 2
    assert hdq.maxlen == 5
    assert len(hdq) == 5


def test_mixed_full_appendleft_nan():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)

    hdq.appendleft(np.nan)
    assert hdq.sum == 4
    assert hdq.sqr_sum == 8
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 3
    assert hdq.mean == 2
    assert hdq.std == 0
    assert len(hdq) == 5


def test_mixed_full_appendleft_random():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)
    hdq.appendleft(randint(0, 99999))
    assert hdq.sum == np.nansum(hdq)
    assert np.isclose(hdq.sqr_sum, np.nansum([x**2 for x in hdq]))
    assert hdq.mean == np.nanmean(hdq)
    assert np.isclose(hdq.std, np.nanstd(hdq))
    assert hdq.maxlen == 5
    assert hdq.NaNCounter == 2
    assert len(hdq) == 5


def test_mixed_full_appendleft_num():
    hdq = HDQ(iterable=(2 if x % 2 == 0 else np.nan for x in range(5)),
              maxlen=5)
    hdq.appendleft(2)
    assert hdq.sum == 6
    assert hdq.sqr_sum == 12
    assert hdq.NaNCounter == 2
    assert hdq.std == 0
    assert hdq.mean == 2
    assert hdq.maxlen == 5
    assert len(hdq) == 5


def test_pop_empty():
    hdq = HDQ(iterable=(), maxlen=None)
    with pytest.raises(IndexError) as error:
        hdq.pop()
    assert 'pop from an empty deque' in str(error.value)


def test_pop_nan_full_nan():
    hdq = HDQ([np.nan]*5, maxlen=5)
    for i in range(5):

        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert hdq.NaNCounter == 5 - i
        assert np.isnan(hdq.std)
        assert np.isnan(hdq.mean)
        assert hdq.maxlen == 5
        assert len(hdq) == 5 - i

        assert np.isnan(hdq.pop())


def test_popleft_nan_full_nan():
    hdq = HDQ([np.nan]*5, maxlen=5)
    for i in range(5):

        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert hdq.NaNCounter == 5 - i
        assert np.isnan(hdq.std)
        assert np.isnan(hdq.mean)
        assert hdq.maxlen == 5
        assert len(hdq) == 5 - i

        assert np.isnan(hdq.popleft())


def test_pop_nan_non_full_nan():
    hdq = HDQ([np.nan]*3, maxlen=5)
    for i in range(3):

        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert hdq.NaNCounter == 3 - i
        assert np.isnan(hdq.std)
        assert np.isnan(hdq.mean)
        assert hdq.maxlen == 5
        assert len(hdq) == 3 - i

        assert np.isnan(hdq.pop())


def test_popleft_nan_non_full_nan():
    hdq = HDQ([np.nan]*3, maxlen=5)
    for i in range(3):

        assert np.isnan(hdq.sum)
        assert np.isnan(hdq.sqr_sum)
        assert hdq.NaNCounter == 3 - i
        assert np.isnan(hdq.std)
        assert np.isnan(hdq.mean)
        assert hdq.maxlen == 5
        assert len(hdq) == 3 - i

        assert np.isnan(hdq.popleft())


def test_pop_random_non_full_num():
    hdq = HDQ(iterable=(randint(0, 999999) for _ in range(3)), maxlen=5)

    for i in range(3):

        assert hdq.sum == np.nansum(hdq)
        assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
        assert hdq.mean == np.nanmean(hdq)
        assert np.isclose(hdq.std, np.nanstd(hdq))
        assert hdq.maxlen == 5
        assert hdq.NaNCounter == 0
        assert len(hdq) == 3 - i

        hdq.pop()


def test_popleft_random_non_full_num():
    hdq = HDQ(iterable=(randint(0, 999999) for _ in range(3)), maxlen=5)

    for i in range(3):
        assert hdq.sum == np.nansum(hdq)
        assert hdq.sqr_sum == np.nansum([x**2 for x in hdq])
        assert hdq.mean == np.nanmean(hdq)
        assert np.isclose(hdq.std, np.nanstd(hdq))
        assert hdq.maxlen == 5
        assert hdq.NaNCounter == 0
        assert len(hdq) == 3 - i

        hdq.popleft()


def test_random_random():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        my_set = set([1, 2, 3, 4, np.nan])
        for i in range(5555):
            mg = [sample(my_set, 1)[0] for _ in range(5)]
            hdq = HDQ(mg, 5)
            for i in range(10):
                hdq.append(sample(my_set, 1)[0])

                if not (np.isnan(hdq.sqr_sum)
                        and np.isnan(np.nansum([x**2 for x in hdq]))):

                    assert np.isclose(hdq.sqr_sum,
                                      np.nansum([x**2 for x in hdq])) or\
                                      np.nansum([x**2 for x in hdq]) == 0.0\
                                      and (hdq.sqr_sum == 0.0 or np.isnan(
                                           hdq.sqr_sum))
                else:
                    assert (np.isnan(hdq.sqr_sum)
                            and np.isnan(np.nansum([x**2 for x in hdq])))

                cond = np.isnan(np.nanmean(hdq))

                if not (np.isnan(hdq.mean)
                        and cond):
                    assert np.isclose(hdq.mean, np.nanmean(hdq))
                else:
                    cond = np.isnan(np.nanmean(hdq))
                    assert (np.isnan(hdq.mean)
                            and cond)

                if not (np.isnan(hdq.std)
                        and np.isnan(np.nanstd(hdq))):
                    assert np.isclose(hdq.std, np.nanstd(hdq))
                else:
                    assert (np.isnan(hdq.std)
                            and np.isnan(np.nanstd(hdq)))

            assert hdq.maxlen == 5
            assert hdq.NaNCounter == hdq.count(np.nan)
            assert len(hdq) == 5
