import enum



class Monitor:
    def __init__(self, name, active, desktops):
        self._name = name
        self._active = active
        self._desktops = desktops
    @property
    def name(self):
        return self._name
    @property
    def active(self):
        return self._active
    @property
    def desktops(self):
        return self._desktops

    def __eq__(self, other):
        return self.name == other.name and self.active == other.active and self.desktops == other.desktops

    def __repr__(self):
        return "Monitor(" + self.name + ", " + str(self.active) + ", " + str(self.desktops) + ")"


class Desktop:
    class State(enum.Enum):
        FocusedOccupied = 1     # O
        FocusedFree = 2         # F
        FocusedUrgent = 3       # U
        Occupied = 4            # o
        Free = 5                # f
        Urgent = 6              # u

    def __init__(self, name, state):
        self._name = name
        self._state = state

    @property
    def name(self):
        return self._name
    @property
    def state(self):
        return self._state

    def __eq__(self, other):
        return self.name == other.name and self.state == other.state

    def __repr__(self):
        return "Desktop(" + self.name + ", " + str(self.state) + ")"



# TODO: unit test
def parse_bspwm_status(status):
    states_by_token = {
        'O': Desktop.State.FocusedOccupied,
        'F': Desktop.State.FocusedFree,
        'U': Desktop.State.FocusedUrgent,
        'o': Desktop.State.Occupied,
        'f': Desktop.State.Free,
        'u': Desktop.State.Urgent
    }

    # Remove the leading "W" and split on colons
    parts = status[1:].split(':')


    results = []

    mon_name = None
    mon_active = None
    mon_desktops = None

    for part in parts:
        if part[0] in ['M', 'm']:
            if mon_name != None:
                results += [Monitor(mon_name, mon_active, mon_desktops)]

            # TODO: push prev mon onto results
            mon_name = part[1:]
            mon_active = part[0] == "M"
            mon_desktops = []
        elif part in ["LT", "LM"]:
            # ignore layout info for now
            continue
        else:
            mon_desktops.append(Desktop(part[1:], states_by_token[part[0]]))


    if mon_name != None:
        results += [Monitor(mon_name, mon_active, mon_desktops)]

    return results
