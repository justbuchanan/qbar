import unittest
from qbar.bspwm_status import *

class TestBspwmStatus(unittest.TestCase):
    def test_bspwm_status(self):
        example = "WMeDP1:O:f:f:f:f:f:LT:mDP1:f1:f2:f3:f4:F5:LT"
        result = parse_bspwm_status(example)

        expected = [
            Monitor("eDP1", True, [
                Desktop("", Desktop.State.FocusedOccupied),
                Desktop("", Desktop.State.Free),
                Desktop("", Desktop.State.Free),
                Desktop("", Desktop.State.Free),
                Desktop("", Desktop.State.Free),
                Desktop("", Desktop.State.Free)
            ]),
            Monitor("DP1", False, [
                Desktop("1", Desktop.State.Free),
                Desktop("2", Desktop.State.Free),
                Desktop("3", Desktop.State.Free),
                Desktop("4", Desktop.State.Free),
                Desktop("5", Desktop.State.FocusedFree)
            ])
        ]

        # print("expected: " + str(expected))
        # print("results: " + str(result))

        self.assertEqual(expected, result)
