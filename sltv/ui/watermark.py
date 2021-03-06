# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
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
import gtk
import save_button
from sltv.settings import UI_DIR
import pip_widget

class WaterMarkUI:

    def __init__(self, ui, sltv):
        self.ui = ui
        self.sltv = sltv

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/watermark.ui")
        self.widget = self.interface.get_object("table1")
        self.button = self.interface.get_object("filechooserbutton")
        self.resize_checkbutton = self.interface.get_object("resize_checkbutton")
        self.size_label = self.interface.get_object("size_label")
        self.size_adjustment = gtk.Adjustment(1.0, 0, 1.0, 0.05)
        self.size_scale = gtk.HScale(self.size_adjustment)
        self.size_scale.set_property("digits", 2)
        self.widget.attach(self.size_scale, 0, 2, 4, 5)
        self.alpha_adjustment = gtk.Adjustment(1.0, 0, 1.0, 0.05)
        self.alpha_scale = gtk.HScale(self.alpha_adjustment)
        self.widget.attach(self.alpha_scale, 1, 2, 1, 2)

        self.location = None
        self.sltv.set_watermark_size(1.0)

        self._set_resize_sensitive()
        self.widget.show_all()

        self.button.connect("file-set", self._on_file_set)
        self.size_scale.connect("value-changed", self._on_size_changed)
        self.alpha_scale.connect("value-changed", self._on_alpha_changed)
        self.resize_checkbutton.connect(
                "toggled", self._on_resize_check_changed
        )
        self.sltv.connect("preplay", self._on_preplay)
        self.sltv.connect("stopped", self._on_stopped)

    def _on_resize_check_changed(self, button):
        self._set_resize_sensitive()
        enabled = self.resize_checkbutton.get_active()
        self.sltv.set_watermark_resize(enabled)

    def _set_resize_sensitive(self):
        sensitivity = self.resize_checkbutton.get_active()
        self.size_label.set_sensitive(sensitivity)
        self.size_scale.set_sensitive(sensitivity)

    def _on_preplay(self, sltv):
        self.resize_checkbutton.set_sensitive(False)
        self.size_scale.set_sensitive(False)
        self.size_label.set_sensitive(False)

    def _on_stopped(self, sltv):
        self.resize_checkbutton.set_sensitive(True)
        self.size_scale.set_sensitive(True)
        self.size_label.set_sensitive(True)

    def _on_file_set(self, button):
        self.sltv.set_watermark_location(self.button.get_filename())

    def _on_size_changed(self, adjustment):
        self.sltv.set_watermark_size(self.size_scale.get_value())

    def _on_alpha_changed(self, adjustment):
        self.sltv.set_watermark_alpha(self.alpha_scale.get_value())

    def get_widget(self):
        return self.widget
