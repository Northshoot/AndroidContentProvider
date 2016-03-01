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
# Created on 2/18/16.

import json
import copy

class AndroidModel:
    pass

class DataModel:
    """
    Class holding particular model information
    """
    CONCAT = "res.tablesWithJoins += "
    HAS_COLUMNS = ".hasColumns(projection)"
    OPEN_BRACE = ") {\n"
    IF = "if ("
    OR = " || "
    INDENT1 = "                "
    INDENT2 = "                    "
    PLUS = " + "
    COLUMNS = "Columns"
    TABLE_NAME = ".TABLE_NAME"
    LEFT_OUTER_JOIN = "\" LEFT OUTER JOIN \""
    ON = "\" ON \""
    EQUALS = "\"=\""
    DOT = "\".\""
    AS = "\" AS \""
    PREFIX = ".PREFIX_"
    ALL_MODELS = dict()

    def __init__(self, *args, file_name=None, **kwargs):

        self.model = None
        self._json_model = None
        self.name = None
        if file_name:
            self._load_model_from_file(file_name)
            self.name = file_name
        else:
            self.name = kwargs['name']
        DataModel.ALL_MODELS[self.name] = self
        self.fields = []

    def _load_model_from_file(self, file):
        with open(file, encoding='utf-8') as data_file:
            self._json_model = json.loads(data_file.read())

        print(self._json_model)

    def add_field(self, field):
        self.fields.append(field)

    def add_field(self, indx, field):
        self.fields.insert(indx, field)

    def get_fields(self):
        return copy.deepcopy(self.fields)

    def get_fields_including_joins(self):
        return self.get_fields_including_joins(False, "", False);

    def get_fields_including_joins(self, isForeign, path, forceNullable):
        ret = []
        for field in  self.fields:
            if not field.getIsId() and not isForeign:
                return

            if isForeign:
                ret.add(field.asForeignField(path, forceNullable));
            else:
                ret.add(field)

            ForeignKey foreignKey = field.getForeignKey();
            if (foreignKey == null) continue;

            String newPath = path + foreignKey.getEntity().getNameCamelCase();
            // If the field is nullable, all fields of the foreign (joined) entity must also be nullable
            forceNullable = field.getIsNullable();
            // Recurse
            res.addAll(foreignKey.getEntity().getFieldsIncludingJoins(true, newPath, forceNullable));


        return res;
