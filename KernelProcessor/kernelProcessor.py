import numpy as np

from collections import Counter, defaultdict


class KernelProcessor:

    # The number of sampling rate
    n_slots = 1440

    def __init__(self, rtl, starting_slot=0):
        # slot of the last digested entry
        self._last_slot_seen = starting_slot
        # starting slot just if the day starts from other than midnight
        self._starting_slot = starting_slot
        # set of relevant tower locations
        self._rtl = set(rtl)
        # counter of number of users recorded in a specific location
        self._rtl_count = Counter()
        # Ductionary containing for each user the last recorded location
        self._uid_rtl = {}
        # self._rtl_last_update = defaultdict(int)
        # Dict containing the number of users for each slot
        self._rtl_slots = defaultdict(lambda: np.zeros(
                                        KernelProcessor.n_slots, dtype=int))

    # theoretically called every time a we get into a new slot
    def _freeze(self, actual_slot=None):
        # case exactly when one minute has passed no need of actual_slot
        if actual_slot is None:
            actual_slot = self._last_slot_seen + 1
        # we store the counters for each relevant tower location seen
        for rtl in self._rtl_count:
            # In case the number of slot passed is more than one we fill
            # all the slots passed with the same values (no changes on counter)
            self._rtl_slots[rtl][self._last_slot_seen:actual_slot] =\
                                                        self._rtl_count[rtl]

    # returs all the slots and their values for each rtl encountered
    def get_raw_snapshot(self):
        self._freeze()
        return self._rtl_slots

    # Returns the actual slot counter for a specific tower location id
    def get_status(self, tlid):
        return self._rtl_count[tlid]

    # Returns the average of the slot counter for a specific tower location id
    def get_averaged_status(self, tlid, past_slots):
        assert past_slots > 0
        self._freeze()
        last = self._last_slot_seen - past_slots

        if last < 0:
            raise ValueError("Non valid past slots")

        current = self._last_slot_seen

        print(self._rtl_slots[tlid][last:current])
        return np.nanmean(self._rtl_slots[tlid][last:current])

    # To be called at the end of the day re-initialize the KernelProcessor
    def reset(self, rtl=None, starting_slot=None):
        # We store the reference to the generated data in order to store it
        res = self.get_raw_snapshot()  # copy.deepcopy(self.get_raw_snapshot())

        if starting_slot is None:
            starting_slot = self._starting_slot

        if rtl:
            self.__init__(rtl, starting_slot)
        else:
            self.__init__(self._rtl, starting_slot)
        # we return the observed data in the past
        return res

    # To be called every time a new log comes in
    def log_digest(self, tlid, hour, mins, uid):
        actual_slot = hour*60 + mins
        # Case a minute (or more) has passed
        if actual_slot > self._last_slot_seen:
            # we sore the value of the slots
            self._freeze(actual_slot)
            # updates the last slot seen with the one of the new entry
            self._last_slot_seen = actual_slot
        # in any case
        if actual_slot == self._last_slot_seen:
            # if the tlid is not in relevant twrs and user was in relevant twrs
            if tlid not in self._rtl and uid in self._uid_rtl:
                # Decrease the specific tower counter
                self._rtl_count[self._uid_rtl[uid]] -= 1
                # Remove the user from the specific uid -> rtl dictionary
                del self._uid_rtl[uid]
            # Else if the tower is in the highway:
            # TODO optimize: if the user last location is the same as
            # the one contained in the log entry then skip the operation
            elif tlid in self._rtl:
                    # if the user was already in a relevant tower
                    if uid in self._uid_rtl:
                        # decrease the counter of the previous tower
                        self._rtl_count[self._uid_rtl[uid]] -= 1
                    # set the user in the new tower
                    self._uid_rtl[uid] = tlid
                    # increase the counter
                    self._rtl_count[tlid] += 1

        else:
            # it means that we received a log from the pas.. time backwards!
            raise ValueError("Received log from the past (non ordered logs)!")
