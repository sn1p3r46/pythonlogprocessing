import numpy as np

from collections import Counter, defaultdict


class KernelProcessor:

    n_slots = 1440

    def __init__(self, rtl, starting_slot=0):
        self._last_slot_seen = starting_slot
        self._starting_slot = starting_slot
        self._rtl = set(rtl)
        self._rtl_count = Counter()
        self._uid_rtl = {}
        # self._rtl_last_update = defaultdict(int)
        self._rtl_slots = defaultdict(lambda: np.zeros(
                                        KernelProcessor.n_slots, dtype=int))

    def _freeze(self, actual_slot=None):
        if actual_slot is None:
            actual_slot = self._last_slot_seen + 1
        for rtl in self._rtl_count:
            self._rtl_slots[rtl][self._last_slot_seen:actual_slot] =\
                                                        self._rtl_count[rtl]

    def get_raw_snapshot(self):
        self._freeze()
        return self._rtl_slots

    def get_status(self, tlid):
        return self._rtl_count[tlid]

    def get_averaged_status(self, tlid, past_slots):
        self._freeze()
        last = self._last_slot_seen - past_slots

        if last < 0:
            raise ValueError("Non valid past slots")

        current = self._last_slot_seen

        print(self._rtl_slots[tlid][last:current])
        return np.mean(self._rtl_slots[tlid][last:current])

    def reset(self, rtl=None, starting_slot=None):

        res = self.get_raw_snapshot()

        if starting_slot is None:
            starting_slot = self._starting_slot

        if rtl:
            self.__init__(rtl, starting_slot)
        else:
            self.__init__(self._rtl, starting_slot)

        return res

    def log_digest(self, tlid, hour, mins, uid):
        actual_slot = hour*60 + mins
        if actual_slot > self._last_slot_seen:
            self._freeze(actual_slot)
            self._last_slot_seen = actual_slot

        if actual_slot == self._last_slot_seen:
            if tlid not in self._rtl and uid in self._uid_rtl:
                # decrease the highway specific tower counter
                self._rtl_count[self._uid_rtl[uid]] -= 1
                # remove the user from the highways
                del self._uid_rtl[uid]
            # else if the tower is in the highway
            elif tlid in self._rtl:
                    # if the user was already in the highway
                    if uid in self._uid_rtl:
                        # decrease the counter of the previous tower
                        self._rtl_count[self._uid_rtl[uid]] -= 1
                    # set the user in the new tower
                    self._uid_rtl[uid] = tlid
                    # increase the counter
                    self._rtl_count[tlid] += 1

        else:
            raise ValueError("Received log from the past (non ordered logs)!")
