from dataclasses import dataclass

from tasks.time_synchronization.ticks import get_current_tick_mcs, reset_ticks
from tasks.time_synchronization.experiment import run_single_point

def run_experiment_test(
    asymmetry_ratio=0.5,
    network_response_delay_ticks=100.0,
    initial_skew_local_mcs=100.0,
    initial_skew_remote_mcs=200.0,
) -> None:
    reset_ticks()
    assert get_current_tick_mcs() == 0.0

    experiment_point = run_single_point(
        asymmetry_ratio=asymmetry_ratio,
        network_response_delay_ticks=network_response_delay_ticks,
        initial_skew_local_mcs=initial_skew_local_mcs,
        initial_skew_remote_mcs=initial_skew_remote_mcs,
    )
    
    assert experiment_point.asymmetry_ratio == asymmetry_ratio, "Experiment point should have the same asymmetry ratio as the one passed to the experiment"
    assert abs(abs(network_response_delay_ticks * asymmetry_ratio - network_response_delay_ticks) / (2.0 * (initial_skew_remote_mcs + network_response_delay_ticks * asymmetry_ratio + network_response_delay_ticks)) - experiment_point.relative_error) < 0.001, "Experiment point should have the expected relative error"
    assert get_current_tick_mcs() == network_response_delay_ticks + network_response_delay_ticks * asymmetry_ratio, "Experiment should leave expected ticks passed after its execution"


def test_experiments_run() -> None:
    run_experiment_test(
        asymmetry_ratio=1.0,
        network_response_delay_ticks=100.0,
        initial_skew_local_mcs=200.0,
        initial_skew_remote_mcs=200.0,
    )
    run_experiment_test(
        asymmetry_ratio=2.0,
        network_response_delay_ticks=1000.0,
        initial_skew_local_mcs=200.0,
        initial_skew_remote_mcs=400.0,
    )
    run_experiment_test(
        asymmetry_ratio=10.0,
        network_response_delay_ticks=1000.0,
        initial_skew_local_mcs=300.0,
        initial_skew_remote_mcs=400.0,
    )
    run_experiment_test(
        asymmetry_ratio=100.0,
        network_response_delay_ticks=1000.0,
        initial_skew_local_mcs=350.0,
        initial_skew_remote_mcs=400.0,
    )
