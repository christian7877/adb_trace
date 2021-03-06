# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
# pylint: disable=W0212

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from pylib import android_commands
from pylib.device import device_utils
from pylib.perf import perf_control

class TestPerfControl(unittest.TestCase):
  def setUp(self):
    if not os.getenv('BUILDTYPE'):
      os.environ['BUILDTYPE'] = 'Debug'

    devices = android_commands.GetAttachedDevices()
    self.assertGreater(len(devices), 0, 'No device attached!')
    self._device = device_utils.DeviceUtils(
        android_commands.AndroidCommands(device=devices[0]))

  def testHighPerfMode(self):
    perf = perf_control.PerfControl(self._device)
    try:
      perf.SetPerfProfilingMode()
      for cpu in range(perf._num_cpu_cores):
        path = perf_control.PerfControl._CPU_ONLINE_FMT % cpu
        self.assertEquals('1',
                          self._device.ReadFile(path)[0])
        path = perf_control.PerfControl._SCALING_GOVERNOR_FMT % cpu
        self.assertEquals('performance',
                          self._device.ReadFile(path)[0])
    finally:
      perf.SetDefaultPerfMode()

if __name__ == '__main__':
  unittest.main()
