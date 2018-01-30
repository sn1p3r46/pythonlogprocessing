from collections import Counter
import kernelProcessor as kp
import numpy as np
import pytest


rtl = [str(i) for i in range(5)]


def test_counter_increase_decrease():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('1', 0, 0, 'mario')
    KP.log_digest('1', 0, 0, 'maria')
    KP.log_digest('1', 0, 0, 'mara')
    assert KP._rtl_count['1'] == 3
    KP.log_digest('12', 0, 0, 'mario')
    KP.log_digest('12', 0, 0, 'maria')
    assert KP._rtl_count['1'] == 1


def test_back_to_empty():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 0, 'mario')
    KP.log_digest('12', 0, 0, 'mario')
    assert KP._rtl_count['0'] == 0


def test_moove():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 0, 'mario')
    assert KP._rtl_count['0'] == 1
    assert KP._rtl_count['1'] == 0
    assert KP._rtl_count['2'] == 0
    KP.log_digest('1', 0, 0, 'mario')
    assert KP._rtl_count['0'] == 0
    assert KP._rtl_count['1'] == 1
    assert KP._rtl_count['2'] == 0
    KP.log_digest('2', 0, 0, 'mario')
    assert KP._rtl_count['0'] == 0
    assert KP._rtl_count['1'] == 0
    assert KP._rtl_count['2'] == 1


def test_number_of_slots():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'mario')
    KP.log_digest('1', 0, 2, 'mario')
    KP.log_digest('2', 0, 3, 'mario')
    assert len(KP._rtl_slots) == 2


def test_len_of_slots():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'mario')
    KP.log_digest('1', 0, 2, 'mario')
    KP.log_digest('1', 0, 2, 'maria')
    KP.log_digest('0', 0, 5, 'mario')
    KP.log_digest('3', 0, 5, 'mario')

    assert len(KP._rtl_slots['0']) == 1440
    assert len(KP._rtl_slots['1']) == 1440


def test_values_of_slots():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'u0')

    KP.log_digest('1', 0, 2, 'u0')
    KP.log_digest('1', 0, 2, 'maria')

    KP.log_digest('0', 0, 4, 'u0')
    KP.log_digest('1', 0, 4, 'u1')

    KP.log_digest('3', 0, 6, 'u0')

    x0 = [0, 1, 0, 0, 1, 1]
    x1 = [0, 0, 2, 2, 2, 2]

    for index in range(6):
        assert KP._rtl_slots['0'][index] == x0[index]
    for index in range(6):
        assert KP._rtl_slots['1'][index] == x1[index]

    assert len(KP._rtl_slots['1']) == 1440


def test_raise_ValueError():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'u0')
    KP.log_digest('1', 0, 2, 'u0')
    with pytest.raises(ValueError):
        KP.log_digest('0', 0, 1, 'u0')


def test_get_raw_snapshot():
        KP = kp.KernelProcessor(rtl)
        KP.log_digest('0', 0, 1, 'u0')
        KP.log_digest('1', 0, 2, 'u0')
        KP.log_digest('1', 0, 2, 'maria')
        KP.log_digest('0', 0, 4, 'u0')
        KP.log_digest('1', 0, 4, 'u1')
        KP.log_digest('3', 0, 6, 'u0')

        assert set(KP.get_raw_snapshot().keys()) == set(['0', '1', '3'])


def test_reset():
        KP = kp.KernelProcessor(rtl, 1)
        KP.log_digest('0', 0, 1, 'u0')
        KP.log_digest('1', 0, 2, 'u0')
        KP.log_digest('1', 0, 2, 'maria')
        KP.log_digest('0', 0, 4, 'u0')
        KP.log_digest('1', 0, 4, 'u1')
        KP.log_digest('3', 0, 6, 'u0')

        assert set(KP.reset().keys()) == set(['0', '1', '3'])
        assert KP._rtl_count == Counter()
        assert KP._rtl == set(rtl)
        assert KP._uid_rtl == {}
        assert KP._last_slot_seen == 1


def test_get_status():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'u0')
    KP.log_digest('1', 0, 2, 'u0')
    KP.log_digest('1', 0, 2, 'maria')
    KP.log_digest('0', 0, 4, 'u0')
    KP.log_digest('1', 0, 4, 'u1')
    KP.log_digest('2', 0, 6, 'u0')

    assert KP.get_status('0') == 0
    assert KP.get_status('1') == 2
    assert KP.get_status('2') == 1


def test_get_averaged_status():
    KP = kp.KernelProcessor(rtl)
    KP.log_digest('0', 0, 1, 'u0')
    KP.log_digest('1', 0, 2, 'u0')
    KP.log_digest('1', 0, 2, 'maria')
    KP.log_digest('0', 0, 4, 'u0')
    KP.log_digest('1', 0, 4, 'u1')
    KP.log_digest('2', 0, 6, 'u0')

    x0 = [0, 1, 0, 0, 1, 1]
    x1 = [0, 0, 2, 2, 2, 2]
    x3 = [0, 0, 0, 0, 0, 0]

    assert KP.get_averaged_status('0', 3) == np.mean(x0[-3:])
    assert KP.get_averaged_status('1', 3) == np.mean(x1[-3:])
    assert KP.get_averaged_status('2', 1) == np.mean(x3[-1:])
