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
# Licensed under the Apache License, Version 2.0 (the "License")
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


from .foreignkey import ForeignKey
from .field import *
import enum


class Json:
        NAME = "name"
        TYPE = "type"
        DOCUMENTATION = "documentation"
        INDEX = "index"
        NULLABLE = "nullable"
        DEFAULT_VALUE = "defaultValue"
        DEFAULT_VALUE_LEGACY = "default_value"
        ENUM_NAME = "enumName"
        ENUM_VALUES = "enumValues"
        FOREIGN_KEY = "foreignKey"
        FOREIGN_KEY_TABLE = "table"
        FOREIGN_KEY_ON_DELETE_ACTION = "onDelete"

        TYPE_STRING = "String"
        TYPE_INTEGER = "Integer"
        TYPE_LONG = "Long"
        TYPE_FLOAT = "Float"
        TYPE_DOUBLE = "Double"
        TYPE_BOOLEAN = "Boolean"
        TYPE_DATE = "Date"
        TYPE_BYTE_ARRAY = "byte[]"
        TYPE_ENUM = "enum"

        ON_DELETE_ACTION_NO_ACTION = "NO ACTION"
        ON_DELETE_ACTION_RESTRICT = "RESTRICT"
        ON_DELETE_ACTION_SET_NULL = "SET NULL"
        ON_DELETE_ACTION_SET_DEFAULT = "SET DEFAULT"
        ON_DELETE_ACTION_CASCADE = "CASCADE"

sOnDeleteAction = dict()


class Action:
    def __init__(self, json_name):
        self.mJsonName = json_name
        sOnDeleteAction[self.mJsonName] = self

    @property
    def sql_name(self):
        return sOnDeleteAction.get(self.mJsonName).replace('_', ' ')

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
    NO_ACTION = Action(Json.ON_DELETE_ACTION_NO_ACTION)
    RESTRICT = Action(Json.ON_DELETE_ACTION_RESTRICT)
    SET_NULL = Action(Json.ON_DELETE_ACTION_SET_NULL)
    SET_DEFAULT = Action(Json.ON_DELETE_ACTION_SET_DEFAULT)
    CASCADE = Action(Json.ON_DELETE_ACTION_CASCADE)



