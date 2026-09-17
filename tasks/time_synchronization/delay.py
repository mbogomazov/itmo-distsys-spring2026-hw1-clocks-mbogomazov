from typing import final

from tasks.time_synchronization.ticks import advance_ticks_mcs

class NetworkDelayProvider():
  def __init__(self):
    pass

  def run_request(self):
    pass

  def run_response(self):
    pass


@final
class NetworkStaticDelayProvider(NetworkDelayProvider):

  _network_request_delay_ticks: float
  _network_response_delay_ticks: float

  def __init__(
      self,
      network_request_delay_ticks = 0.0,
      network_response_delay_ticks = 0.0,
  ):
    super().__init__()
    self._network_request_delay_ticks = network_request_delay_ticks
    self._network_response_delay_ticks = network_response_delay_ticks

  def run_request(self):
    advance_ticks_mcs(self._network_request_delay_ticks)

  def run_response(self):
    advance_ticks_mcs(self._network_response_delay_ticks)