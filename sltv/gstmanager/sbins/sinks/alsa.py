#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.sink import AudioSink

class AlsaSink(AudioSink):
    def __init__(self, sync=True, device_id=0): 
        self.description = "Alsa audio sink"
        self.type = "audio"
        sbin = "alsasink sync=%s device=hw:%s" %(sync, device_id)
        AudioSink.__init__(self, sbin)
