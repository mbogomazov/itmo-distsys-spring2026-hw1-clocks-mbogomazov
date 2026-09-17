from tasks.time_synchronization.clock import Clock

"""
Implement Cristian's algorithm for clock synchronization here.
Use only public interface of the Clock class.
"""
def cristian_time_synchronize(local_clock: Clock, remote_clock: Clock) -> None:
    # T0: момент отправки запроса по локальным часам
    request_sent_local: int = local_clock.get_time()
    # T_s: время сервера (внутри get_time проходят задержки запроса и ответа)
    server_time: int = remote_clock.get_time()
    # T1: момент получения ответа по локальным часам
    response_received_local: int = local_clock.get_time()

    round_trip_time: int = response_received_local - request_sent_local
    # Считаем канал симметричным: ответ летел RTT / 2, значит сейчас на сервере T_s + RTT / 2
    estimated_server_time_now: float = server_time + round_trip_time / 2
    local_clock.add_offset(estimated_server_time_now - response_received_local)
