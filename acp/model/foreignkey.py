# -*- coding: utf-8 -*-
#  _________.__    .__       .__       .___                     __
#  /   _____/|  |__ |__| ____ |  |    __| _/______  ____  __ ___/  |_  ____
#  \_____  \ |  |  \|  |/ __ \|  |   / __ |\_  __ \/  _ \|  |  \   __\/ __ \
#  /        \|   Y  \  \  ___/|  |__/ /_/ | |  | \(  <_> )  |  /|  | \  ___/
# /_______  /|___|  /__|\___  >____/\____ | |__|   \____/|____/ |__|  \___  >
#         \/      \/        \/           \/                               \/
#
# Copyright (C) 2016 Laurynas Riliskis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Created on 2/29/16.

from .model import DataModel


class ForeignKey:
    """

    """

    def __init__(self, model_name, on_delete_action):
        self.mModelName = model_name
        self.mOnDeleteAction = on_delete_action

    def __str__(self):
        return "ForeignKey [mModelName=" + self.mModelName + ", " \
                "mOnDeleteAction= " + self.mOnDeleteAction + "]"

    @property
    def model_name(self): return self.mModelName

    @property
    def model(self): return DataModel.get_by_name(self.mModelName)

    @property
    def on_delete_action(self): return self.mOnDeleteAction
