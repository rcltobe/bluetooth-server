import unittest

from app.domain.models.device_state import DeviceState


class TestDeviceState(unittest.TestCase):
    def test_should_update_state(self):
        address = "00:00:00:00:00:00"

        # 状態が変化したときのみ、更新する。
        state_found = DeviceState(address, False)
        self.assertTrue(state_found.should_update_state(DeviceState(address, True)))
        self.assertFalse(state_found.should_update_state(DeviceState(address, False)))

        # 状態が変化したときのみ、更新する。
        state_not_found = DeviceState(address, True)
        self.assertFalse(state_not_found.should_update_state(DeviceState(address, True)))
        self.assertTrue(state_not_found.should_update_state(DeviceState(address, False)))

        # 前回の記録がなければ、更新する。
        self.assertFalse(None)

    def test_get_last_device_states(self):
        address = "00:00:00:00:00:00"

        prev_state = DeviceState(address, False, created_at=10)
        states = [
            prev_state,
            DeviceState(address, False, created_at=0),
            DeviceState("11:11:11:11:11:11", False, created_at=20),
        ]

        last_state = DeviceState.get_last_device_states(address, states)
        self.assertEqual(last_state.id, prev_state.id)
