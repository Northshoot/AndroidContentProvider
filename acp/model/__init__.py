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


from acp.utils.logger import logger as Log
from .json_representation import JsonRepresentation
from .constraint import Constraint
from .delete_action import Action, sOnDeleteAction, OnDeleteAction
from .foreignkey import ForeignKey
from .field import *

__ALL__FIELDS__ = {
    "String": StringField,
    "Integer": IntegerField,
    "Long": LongField,
    "Float": FloatField,
    "Double": DoubleField,
    "Boolean": BooleanField,
    "Date ": DateField,
    "byte[]": ByteArrayField,
    "enum": EnumField
}

from .model import DataModel, Models














