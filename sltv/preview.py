# -*- coding: utf-8 -*-
# Copyright (C) 2009 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import gobject
import pygst
pygst.require("0.10")
import gst
import gtk

class Preview(gst.Bin):

    __gsignals__ = {
        "prepare-xwindow-id" : (
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.type_from_name("GstElement"),)
        )
    }

    def __init__(self, sltv):
        gobject.GObject.__init__(self)
        sltv.connect("sync-message", self.on_sync_message)
        self.sink = gst.element_factory_make("autovideosink", "sink")
        self.add(self.sink)
        self.colorspace = gst.element_factory_make(
            "ffmpegcolorspace", "colorspace"
        )
        self.add(self.colorspace)
        self.videoscale = gst.element_factory_make("videoscale")
        self.add(self.videoscale)
        gst.element_link_many(self.colorspace, self.videoscale, self.sink)
        sink_pad = gst.GhostPad(
            "sink_ghost_pad", self.colorspace.sink_pads().next()
        )
        self.add_pad(sink_pad)

    def on_sync_message(self, sltv, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            previewsink = message.src
            if previewsink.get_parent() == self.sink:
                previewsink.set_property("sync", False)
                previewsink.set_property("force-aspect-ratio", True)
                self.emit("prepare-xwindow-id", previewsink)

gobject.type_register(Preview)
