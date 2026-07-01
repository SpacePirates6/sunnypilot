from cereal import log
import cereal.messaging as messaging

DM_DISABLED = True

AlertLevel = log.DriverMonitoringState.AlertLevel
MonitoringPolicy = log.DriverMonitoringState.MonitoringPolicy


def get_driver_state_v2_packet(frame_id: int = 0, is_rhd: bool = False):
  dat = messaging.new_message('driverStateV2', valid=True)
  ds = dat.driverStateV2
  ds.frameId = frame_id
  for driver_data in (ds.leftDriverData, ds.rightDriverData):
    driver_data.faceOrientation = [0., 0., 0.]
    driver_data.faceOrientationStd = [0., 0., 0.]
    driver_data.facePosition = [0., 0.]
    driver_data.facePositionStd = [0., 0.]
    driver_data.faceProb = 1.0
    driver_data.leftEyeProb = 1.0
    driver_data.rightEyeProb = 1.0
    driver_data.leftBlinkProb = 0.0
    driver_data.rightBlinkProb = 0.0
    driver_data.sunglassesProb = 0.0
    driver_data.phoneProb = 0.0
    driver_data.sleepProb = 0.0
  ds.wheelOnRightProb = 1.0 if is_rhd else 0.0
  return dat


def get_driver_monitoring_state_packet(is_rhd: bool = False):
  dat = messaging.new_message('driverMonitoringState', valid=True)
  dm = dat.driverMonitoringState
  dm.lockout = False
  dm.alwaysOn = False
  dm.alwaysOnLockout = False
  dm.alertLevel = AlertLevel.none
  dm.activePolicy = MonitoringPolicy.vision
  dm.isRHD = is_rhd
  dm.visionPolicyState.awarenessPercent = 100
  dm.visionPolicyState.isDistracted = False
  dm.visionPolicyState.faceDetected = True
  dm.visionPolicyState.distractedTypes.pose = False
  dm.visionPolicyState.distractedTypes.eye = False
  dm.visionPolicyState.distractedTypes.phone = False
  dm.wheeltouchPolicyState.awarenessPercent = 100
  return dat
