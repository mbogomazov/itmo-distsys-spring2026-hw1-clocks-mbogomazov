from dataclasses import dataclass
from typing import Self

from tasks.time_synchronization.ticks import advance_ticks_mcs, get_current_tick_mcs, reset_ticks
from tasks.time_synchronization.cristian import cristian_time_synchronize
from tasks.time_synchronization.clock import Clock, ClockWithNetworkDelay, LocalClock
from tasks.time_synchronization.delay import NetworkStaticDelayProvider
from tasks.time_synchronization.experiment import run_single_point

@dataclass
class Context:
    ticks_mcs: float = 0.0
    local_time: int = 0
    remote_time: int = 0

    def set(self, local_clock: Clock, remote_clock: Clock) -> Self:
        self.ticks_mcs = get_current_tick_mcs()
        self.local_time = local_clock._get_real_time()
        self.remote_time = remote_clock._get_real_time()
        return self
    

def run_test(
    initial_skew_mcs_local: float = 0.0,
    initial_skew_mcs_remote: float = 0.0,
    drift_mcs_per_tick_local: float = 1.0,
    drift_mcs_per_tick_remote: float = 1.0,
    network_request_delay_ticks: float = 0.0,
    network_response_delay_ticks: float = 0.0,
):
    local_clock = LocalClock(
        initial_skew_mcs=initial_skew_mcs_local,
        drift_mcs_per_tick=drift_mcs_per_tick_local
    )

    remote_clock = ClockWithNetworkDelay(
        network_delay_provider=NetworkStaticDelayProvider(
            network_request_delay_ticks=network_request_delay_ticks,
            network_response_delay_ticks=network_response_delay_ticks
        ),
        initial_skew_mcs=initial_skew_mcs_remote,
        drift_mcs_per_tick=drift_mcs_per_tick_remote,
    )

    ctx_start = Context().set(local_clock, remote_clock)
    cristian_time_synchronize(local_clock, remote_clock)
    ctx_finish = Context().set(local_clock, remote_clock)

    assert local_clock.invocation_counter == 2, "Local clock must be polled twice in Cristian's algorithm"
    assert remote_clock.invocation_counter == 1, "Remote clock must be polled once in Cristian's algorithm"
    assert ctx_finish.ticks_mcs == ctx_start.ticks_mcs + network_request_delay_ticks + network_response_delay_ticks, "No ticks must have been advanced outside the network delay"

    local_clock_on_request_departure = ctx_start.local_time

    advance_ticks_mcs(-(network_response_delay_ticks))
    remote_clock_on_request_arrival = remote_clock._get_real_time()
    advance_ticks_mcs(+(network_response_delay_ticks))

    local_clock_on_response_arrival = ctx_finish.local_time - local_clock._offset

    assert local_clock._get_real_time() == int(remote_clock_on_request_arrival + float(local_clock_on_response_arrival - local_clock_on_request_departure) / 2), "Local clock should be synchronized to the estimated remote time"
    
    advance_ticks_mcs(-(network_request_delay_ticks + network_response_delay_ticks))
    assert ctx_start.remote_time == remote_clock._get_real_time(), "Remote clock should not be affected by synchronization"


def test_basic_synchronization_no_skew_no_network() -> None:
    run_test(
        initial_skew_mcs_local=100,
        initial_skew_mcs_remote=200,
        drift_mcs_per_tick_local=1.0,
        drift_mcs_per_tick_remote=1.0,
        network_request_delay_ticks=0.0,
        network_response_delay_ticks=0.0, 
    )

def test_basic_synchronization_no_skew_equal_network() -> None:
    run_test(
        initial_skew_mcs_local=100,
        initial_skew_mcs_remote=200,
        drift_mcs_per_tick_local=1.0,
        drift_mcs_per_tick_remote=1.0,
        network_request_delay_ticks=40.0,
        network_response_delay_ticks=40.0, 
    )

def test_basic_synchronization_small_skew_equal_network() -> None:
    run_test(
        initial_skew_mcs_local=101,
        initial_skew_mcs_remote=200,
        drift_mcs_per_tick_local=1.0,
        drift_mcs_per_tick_remote=1.00001,
        network_request_delay_ticks=40.0,
        network_response_delay_ticks=40.0, 
    )

def test_basic_synchronization_precision_equal_network() -> None:
    run_test(
        initial_skew_mcs_local=101,
        initial_skew_mcs_remote=102,
        drift_mcs_per_tick_local=1.0,
        drift_mcs_per_tick_remote=1.0,
        network_request_delay_ticks=40.0,
        network_response_delay_ticks=40.0, 
    )
    run_test(
        initial_skew_mcs_local=-101,
        initial_skew_mcs_remote=-102,
        drift_mcs_per_tick_local=1.0,
        drift_mcs_per_tick_remote=1.0,
        network_request_delay_ticks=40.0,
        network_response_delay_ticks=40.0, 
    )