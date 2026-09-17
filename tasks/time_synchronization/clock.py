from typing import final

from tasks.time_synchronization.delay import NetworkDelayProvider
from tasks.time_synchronization.ticks import get_current_tick_mcs

"""
Clock is an abstract class representing a real time clock with drift and skew.
Clock provides time via `get_time` method and enables synchronization via `add_offset` method.
"""
class Clock():
    _initial_skew_mcs: float
    _drift_mcs_per_tick: float
    _offset: float
    
    def __init__(
            self,
            initial_skew_mcs: float = 0.0,
            drift_mcs_per_tick: float = 1.0,
    ):
        self._initial_skew_mcs = initial_skew_mcs
        self._drift_mcs_per_tick = drift_mcs_per_tick
        self._offset = 0.0

    def get_time(self) -> int:
        return self._get_real_time()

    @final
    def add_offset(self, offset: float) -> None:
        self._offset += offset

    @final
    def _get_real_time(self) -> int:
        return int(self._drift_mcs_per_tick * get_current_tick_mcs() + self._initial_skew_mcs + self._offset)
    
"""
LocalClock is a delay-free implementation of Clock.
"""
class LocalClock(Clock):

    invocation_counter = 0

    def __init__(
            self,
            initial_skew_mcs: float = 0.0,
            drift_mcs_per_tick: float = 1.0,
    ):
        super().__init__(initial_skew_mcs, drift_mcs_per_tick)

    @final
    def get_time(self) -> int:
        self.invocation_counter += 1
        timestamp = super().get_time()
        return timestamp

"""
ClockWithNetworkDelay is an implementation of Clock with static network delays.
"""
class ClockWithNetworkDelay(Clock):

    invocation_counter = 0

    def __init__(
            self,
            network_delay_provider: NetworkDelayProvider,
            initial_skew_mcs: float = 0.0,
            drift_mcs_per_tick: float = 1.0,
    ):
        super().__init__(initial_skew_mcs, drift_mcs_per_tick)
        self._network_delay_provider = network_delay_provider

    @final
    def get_time(self) -> int:
        self._network_delay_provider.run_request()
        timestamp = super().get_time()
        self._network_delay_provider.run_response()
        self.invocation_counter += 1
        return timestamp