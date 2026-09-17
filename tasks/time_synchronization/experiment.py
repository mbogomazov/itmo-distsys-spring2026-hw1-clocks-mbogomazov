from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from tasks.time_synchronization.ticks import reset_ticks
from tasks.time_synchronization.cristian import cristian_time_synchronize
from tasks.time_synchronization.clock import ClockWithNetworkDelay, LocalClock
from tasks.time_synchronization.delay import NetworkStaticDelayProvider

matplotlib.use("Agg")

@dataclass(frozen=True)
class ExperimentPoint:
	# Ratio defined as (request delay time) / (response delay time)
	asymmetry_ratio: float
	# Ratio defined as abs(local time after sync - remote time after sync / remote time after sync)
	relative_error: float

def run_single_point(
    # Ratio defined as (request delay) / (response delay)
	asymmetry_ratio: float,
	# Static response delay in ticks (Round-Trip-Time = request delay + response delay)
	network_response_delay_ticks: float,
	# Parameter for initial local clock skew in microseconds
	initial_skew_local_mcs: float,
	# Parameter for initial remote clock skew in microseconds
	initial_skew_remote_mcs: float,
) -> ExperimentPoint:
	# Каждая точка эксперимента начинается с нулевого реального времени
	reset_ticks()

	local_clock = LocalClock(initial_skew_mcs=initial_skew_local_mcs)
	remote_clock = ClockWithNetworkDelay(
		network_delay_provider=NetworkStaticDelayProvider(
			network_request_delay_ticks=network_response_delay_ticks * asymmetry_ratio,
			network_response_delay_ticks=network_response_delay_ticks,
		),
		initial_skew_mcs=initial_skew_remote_mcs,
	)

	cristian_time_synchronize(local_clock, remote_clock)

	# Читаем показания обоих часов в один и тот же момент реального времени.
	# remote_clock.get_time() не подходит: он сдвинул бы тики на сетевые задержки.
	# Поэтому эталон — часы с теми же параметрами, что у удаленных, но без сети
	# ("идеальный наблюдатель" рядом с сервером).
	reference_remote_clock = LocalClock(initial_skew_mcs=initial_skew_remote_mcs)
	local_time: int = local_clock.get_time()
	remote_time: int = reference_remote_clock.get_time()

	return ExperimentPoint(
		asymmetry_ratio=asymmetry_ratio,
		relative_error=abs((local_time - remote_time) / remote_time),
	)


def run_experiment(
	asymmetry_ratios: np.ndarray,
	network_response_delay_ticks: float = 100.0,
	initial_skew_local_mcs: float = 1000.0,
	initial_skew_remote_mcs: float = 2000.0,
) -> list[ExperimentPoint]:
	return [
		run_single_point(
			asymmetry_ratio=float(ratio),
			network_response_delay_ticks=network_response_delay_ticks,
			initial_skew_local_mcs=initial_skew_local_mcs,
			initial_skew_remote_mcs=initial_skew_remote_mcs,
		)
		for ratio in asymmetry_ratios
	]

def draw_plot(
		points: list[ExperimentPoint],
		output_path: Path,
		title: str,
) -> None:
	x = np.array([point.asymmetry_ratio for point in points], dtype=float)
	y = np.array([point.relative_error for point in points], dtype=float)

	plt.figure(figsize=(9, 5))
	plt.plot(x, y, marker="o", linewidth=1.8, markersize=4, label="Measured relative error")
	plt.xscale("log")
	plt.xlabel("Channel asymmetry coefficient (request delay / response delay)")
	plt.ylabel("Relative synchronization error")
	plt.title(title)
	plt.grid(True, which="both", alpha=0.3)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_path, dpi=160)
	plt.close()


def main() -> None:
	asymmetry_ratios = np.logspace(0, 3.0, 100)
	points = run_experiment(asymmetry_ratios=asymmetry_ratios)

	output_path = Path(__file__).with_name("experiment.png")
	draw_plot(points, output_path, title="Cristian algorithm: channel asymmetry ratio vs. relative synchronization error")

if __name__ == "__main__":
	main()
