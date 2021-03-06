# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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

REGISTRY_INPUT = "input"
REGISTRY_OUTPUT = "output"
REGISTRY_VIDEO_CONVERTER = "videoconverter"
REGISTRY_ENCODING = "encoding"
REGISTRY_AUDIO = "audio"

class Registry:

    def __init__(self):
        self.factories = {
            REGISTRY_INPUT: [], REGISTRY_OUTPUT: [],
            REGISTRY_VIDEO_CONVERTER: [], REGISTRY_ENCODING: [],
            REGISTRY_AUDIO: []
        }

    def get_factory_by_id(self, type, id):
        for factory in self.factories[type]:
            if factory.get_id() == id:
                return factory
        return None

    def get_factories(self, type):
        return self.factories[type]

    def register_factory(self, type, factory):
        self.factories[type].append(factory)

registry = Registry()
