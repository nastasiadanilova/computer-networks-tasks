"""
Задание 34. Симулятор TCP-контроля перегрузки (Tahoe).

Алгоритм Tahoe: slow start + congestion avoidance + fast retransmit.
При потере: ssthresh = cwnd/2, cwnd = 1, переход в slow start.
"""

import math


class TCPTahoe:
    """
    Симулятор управления перегрузкой TCP Tahoe (пораундовый).

    Алгоритм:
      Slow Start:          cwnd удваивается каждый RTT (cwnd *= 2)
      Congestion Avoidance: cwnd растет на 1 каждый RTT (cwnd += 1)
      Потеря:             ssthresh = max(cwnd // 2, 1); cwnd = 1; -> slow start
    """

    def __init__(self, ssthresh: int = 64):
        self.cwnd: int = 1          # начальное окно - 1 сегмент
        self.ssthresh: int = ssthresh
        self.phase: str = "slow_start"

    def step(self, loss: bool = False) -> int:
        """
        Выполняет один RTT-раунд.

        Args:
            loss: True, если в этом раунде произошла потеря пакета

        Returns:
            Новое значение cwnd (после обработки потери или роста)
        """
        if loss:
            # Реакция на потерю: сброс к slow start
            self.ssthresh = max(self.cwnd // 2, 1)
            self.cwnd = 1
            self.phase = "slow_start"
        else:
            # Рост в зависимости от фазы
            if self.phase == "slow_start":
                self.cwnd *= 2
                if self.cwnd >= self.ssthresh:
                    # Не превышаем ssthresh, переходим в congestion avoidance
                    self.cwnd = self.ssthresh
                    self.phase = "congestion_avoidance"
            else:  # congestion_avoidance
                self.cwnd += 1

        return self.cwnd


if __name__ == "__main__":
    tcp = TCPTahoe(ssthresh=8)
    for rtt in range(12):
        loss = (rtt == 6)
        cwnd = tcp.step(loss=loss)
        print(f"RTT {rtt:2d}: cwnd={cwnd:3d}, ssthresh={tcp.ssthresh}, phase={tcp.phase}")
