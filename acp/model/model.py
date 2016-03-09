# -*- coding: utf-8 -*-
#          _______  _______  _______  _______  _
# |\     /|(  ___  )(  ____ )(       )(  ___  )( (    /||\     /|
# | )   ( || (   ) || (    )|| () () || (   ) ||  \  ( |( \   / )
# | (___) || (___) || (____)|| || || || |   | ||   \ | | \ (_) /
# |  ___  ||  ___  ||     __)| |(_)| || |   | || (\ \) |  \   /
# | (   ) || (   ) || (\ (   | |   | || |   | || | \   |   ) (
# | )   ( || )   ( || ) \ \__| )   ( || (___) || )  \  |   | |
# |/     \||/     \||/   \__/|/     \|(_______)|/    )_)   \_/
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
from acp.utils.logger import logger as Log


class Models:

    ALL_DATA_MODELS = []
    HEADER = None

    def __init__(self):
        self.mHeader = None
        self.data_models = []

    @classmethod
    def add_model(cls, model):
        if isinstance(model, DataModel):
            cls.ALL_DATA_MODELS.append(model)
        else:
            Log.error("Trying to add model that is not instance of DataModel "
                      "but: %s" % model.__class__.__name__)
            raise TypeError("Expected obj of type DataModel, got: %s"
                            % model.__class__.__name__)

    @classmethod
    def set_header(cls, header):
        cls.HEADER = header

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

    def __init__(self, file_name=None,  **kwargs):

        self.mModel = None
        self._json_model = None
        self.mName = None
        try:
            self.mName = kwargs['name']
        except KeyError:
            Log.error("Model name is required")
            raise KeyError("Model name is required")

        self.mDocumentation = None
        try:
            self.mDocumentation = kwargs['documentation']
        except KeyError:
            pass

        self.mFields = []
        self.mConstraints = []
        #add self to global list
        DataModel.ALL_MODELS[self.mName] = self

    @classmethod
    def get_by_name(cls, mModelName):
        try:
            return cls.ALL_MODELS[mModelName]
        except KeyError:
            raise KeyError("No such model: %s" % mModelName)

    @property
    def fields(self): return self.mFields

    @classmethod
    def add_model(cls, model):
        #TODO: check the right type
        cls.MODELS_LIST.append(model)

    def add_id_field(self, field):
        self.mFields.insert(0, field)

    def add_field(self, field):
        self.mFields.append(field)

    def get_fields(self):
        return copy.deepcopy(self.mFields)

    @property
    def fields_including_joins(self): return self.get_fields_including_joins()

    def get_fields_including_joins(self, isForeign=False, path="",
                                   forceNullable=False):
        ret = []

        for field in self.mFields:
            if not field.is_id and isForeign:
                continue

            if isForeign:
                ret.append(field.asForeignField(path, forceNullable))
            else:
                ret.append(field)

            foreignKey = field.foreign_key
            if foreignKey:
                newPath = path + foreignKey.model.name_camel_case
                # If the field is nullable, all fields of the foreign (
                # joined) entity must also be nullable
                forceNullable = field.is_nullable
                # Recurse
                ret + foreignKey.model \
                    .get_fields_including_joins(True, newPath, forceNullable)

        print("LENGHT: " + str(len(ret)))
        return ret

    @property
    def joined_models(self): return self.get_joined_models()

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

    def add_constraint(self, constrain):
        self.mConstraints.append(constrain)

    @property
    def constrains(self): return self.mConstrains

    @property
    def name_camel_case(self):
        return word_tools.lower_case_underscore_to_camel_case(self.mName)

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

    def all_joined_table_names(self):
        # ret = self.name_camel_case
        # ret+=
        # ret +=
        # ret +=
        # ret +=
        # ret +=
        # ret +=
        # ret +=
        pass

    def add_all_joined_clauses(self):
        pass

    def __str__(self):
        return "Entity [mName=" + self.mName + ", mFields=" + \
        str(self.mFields) + ", mConstraints=" + str(self.mConstraints) + \
        ", mDocumentation=" + self.mDocumentation + "]";
