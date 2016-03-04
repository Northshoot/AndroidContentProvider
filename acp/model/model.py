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
import acp.utils.tools as word_tools
from . import Log


class Model:

    ALL_DATA_MODELS = []
    def __init__(self):
        self.mHeader = None
        self.data_models = []

    @classmethod
    def add_model(self, model):
        if isinstance(model, DataModel):
            self.data_models.append(model)
        else:
            Log.error("Trying to add model that is not instance of DataModel "
                      "but: %s" % model.__class__.__name__)
            raise TypeError("Expected obj of type DataModel, got: %s"
                            % model.__class__.__name__)

    def __str__(self):
        return self.ALL_DATA_MODELS.__str__()

    @classmethod
    def get_models(cls):
        return cls.ALL_DATA_MODELS

    @classmethod
    def flag_ambiguous_fields(cls):
        for m in cls.ALL_DATA_MODELS:
            m.flag_ambiguous_fields()

        for m in cls.ALL_DATA_MODELS:
            for f in m.get_fields():
                if f.is_ambiguous:
                    Log.info("\nNote: in the table '" + m.name_lower_case +
                             "', the column '" + f.name + "' will be named '" +
                             f.prefixed_name + "' to avoid ambiguities "
                             "when joining.\n")


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

    def __init__(self, file_name=None, **kwargs):

        self.mModel = None
        self._json_model = None
        self.mName = None
        if file_name:
            self._load_model_from_file(file_name)
            self.mName = file_name
        else:
            self.mName = kwargs['name']
        self.mFields = []
        self.mConstrains = []
        #add self to global list
        DataModel.ALL_MODELS[self.mName] = self

    @classmethod
    def get_by_name(cls, mModelName):
        try:
            return cls.ALL_MODELS[mModelName]
        except KeyError:
            raise KeyError("No such model: %s" % mModelName)



    @classmethod
    def add_model(cls, model):
        #TODO: check the right type
        cls.MODELS_LIST.append(model)

    def _load_model_from_file(self, file):
        with open(file, encoding='utf-8') as data_file:
            self._json_model = json.loads(data_file.read())

        Log.debug(self._json_model)

    def add_field(self, field, indx=None):
        if indx:
            self.mFields.insert(indx, field)
        else:
            self.mFields.append(field)

    def get_fields(self):
        return copy.deepcopy(self.mFields)

    def get_fields_including_joins(self, isForeign=False, path="",
                                   forceNullable=False):
        ret = []
        for field in self.mFields:
            if not field.getIsId() and not isForeign:
                return

            if isForeign:
                ret.append(field.asForeignField(path, forceNullable))
            else:
                ret.append(field)

            foreignKey = field.getForeignKey()
            if foreignKey:
                newPath = path + foreignKey.getEntity().getNameCamelCase()
                # If the field is nullable, all fields of the foreign (
                # joined) entity must also be nullable
                forceNullable = field.getIsNullable()
                # Recurse
                ret + foreignKey.getEntity()\
                    .getFieldsIncludingJoins(True, newPath, forceNullable)

        return ret

    def get_joined_models(self):
        ret = []
        for field in self.mFields:
            if field.foreign_key:
                ret.add(field.foreign_key.model)
                ret + field.foreign_key.model.get_joined_models()
        return ret

    def get_field_by_name(self, name):
        for field in self.mFields:
            if field.name_lower_case == name.lower():
                return field
        return None

    def add_constrain(self, constrain):
        self.mConstrains.append(constrain)

    @property
    def constrains(self): return self.mConstrains

    @property
    def name_camel_case(self):
        return word_tools.detect_conversion_method(self.mName)

    @property
    def package_name(self):
        return self.name_lower_case.replace("_", "")

    @property
    def name_lower_case(self): return self.mName.lower()

    @property
    def name_upper_case(self):
        return self.mName.upper()

    def flag_ambiguous_fields(self):
        all_j_fields = self.get_fields_including_joins()
        for f1 in all_j_fields:
            for f2 in all_j_fields:
                if f1 == f2:
                    continue
                if f1.name_lower_case == f2.name_lower_case:
                    f1.mIsAmbiguous()
                    f2.mIsAmbiguous()
