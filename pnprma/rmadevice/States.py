import pickle
import time
from copy import deepcopy


states_ref = {"FETCH_CONFIG": {"timestamp": "", "progress": "NOT_STARTED", "msg":""},
          "WAITING_FOR_NEW_DEVICE": {"timestamp": "", "progress": "NOT_STARTED","msg":""},
          "PROVISION_NEW_DEVICE": {"timestamp": "", "progress": "NOT_STARTED","msg":""}}

class States():
    def putState(self, serial_number, state, progress, msg=None):
        states = deepcopy(states_ref)
        try:
            with open('states.pickle', 'rb') as handle:
                b = pickle.load(handle)
                if serial_number in b:
                    states=b[serial_number]
        except FileNotFoundError:
            pass
        for s in states:
            if(s == state):
                states[s]["timestamp"]=time.ctime()
                states[s]["progress"] = progress
                if msg:
                    states[s]["msg"] = msg
        a = {serial_number: states}
        print(serial_number + " => " + state)
        with open('states.pickle', 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def getState(self, serial_number):
        try:
            with open('states.pickle', 'rb') as handle:
                b = pickle.load(handle)
                if serial_number in b:
                    return b[serial_number]
        except FileNotFoundError:
            return states_ref
        return states_ref