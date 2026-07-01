#!/usr/bin/env python3
import cereal.messaging as messaging
from openpilot.common.params import Params
from openpilot.common.realtime import config_realtime_process, Ratekeeper, DT_DMON
from openpilot.selfdrive.monitoring.dm_stub import get_driver_monitoring_state_packet, get_driver_state_v2_packet


def dmonitoringd_thread():
  config_realtime_process([0, 1, 2, 3], 5)

  params = Params()
  pm = messaging.PubMaster(['driverStateV2', 'driverMonitoringState'])
  rk = Ratekeeper(1 / DT_DMON, print_delay_threshold=None)
  frame_id = 0

  while True:
    is_rhd = params.get_bool("IsRhdDetected")
    pm.send('driverStateV2', get_driver_state_v2_packet(frame_id, is_rhd))
    pm.send('driverMonitoringState', get_driver_monitoring_state_packet(is_rhd))
    frame_id += 1
    rk.keep_time()


def main():
  dmonitoringd_thread()


if __name__ == '__main__':
  main()
