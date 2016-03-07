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
# Created on 3/7/16.

import enum
from . import JsonRepresentation
from . import Log
sOnDeleteAction = dict()


class Action:
    def __init__(self, json_name):
        self.mJsonName = json_name
        sOnDeleteAction[self.mJsonName] = self
        Log.debug("Created: " + self.__str__())

    def __str__(self):
        return "Action: " + "[JsonName: " + self.mJsonName + "]"

    @property
    def sql_name(self):
        return sOnDeleteAction.get(self.mJsonName).replace('_', ' ')

    @classmethod
    def from_json_name(self, json_name):
        try:
            action = sOnDeleteAction.get(json_name)
            return action
        except KeyError:
            raise KeyError("No such action: %s" %json_name)


class OnDeleteAction(enum.Enum):
    """
    On delete action representation in android/sql
    """
    NO_ACTION = Action(JsonRepresentation.ON_DELETE_ACTION_NO_ACTION)
    RESTRICT = Action(JsonRepresentation.ON_DELETE_ACTION_RESTRICT)
    SET_NULL = Action(JsonRepresentation.ON_DELETE_ACTION_SET_NULL)
    SET_DEFAULT = Action(JsonRepresentation.ON_DELETE_ACTION_SET_DEFAULT)
    CASCADE = Action(JsonRepresentation.ON_DELETE_ACTION_CASCADE)
