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

from .utils.tools import get_file_names
from .app import Application
from .model.model import DataModel
from .utils.logger import logger as Log
from .model import JsonRepresentation as Json, Models, DataModel
from .model import Action, ForeignKey, __ALL__FIELDS__, Constraint
import json


class Generator:
    def __init__(self, args):
        self.args = args
        self._files = get_file_names(args.path)
        self.config_file_name = self._files[0] #fist one is config
        self.models_file_names = self._files[1:] #the rest are models
        Log.debug("Model to load: " + str(self._files))
        self.app = Application(args.path, args.output, self.config_file_name)
        self.models = []
        # for mf in self.models_file_names:
        #     self.models.append(DataModel(file_name=mf))


    def load_models(self):
        # load files
        for mFile in self.models_file_names:
            Log.debug("Model path: " + self.args.path + mFile)
            model_name =mFile.split('.json')[0]
            Log.debug("Model name: " + model_name)
            json_model = None
            with open(mFile, encoding='utf-8') as data_file:
                json_model = json.loads(data_file.read())
                Log.debug("json_model=" + str(json_model))
            if not json_model:
                Log.error("Can't load Json model")
                raise ValueError("json error")

            mode_documentation = json_model.get(Json.DOCUMENTATION)
            model = DataModel(name=model_name, documentation=mode_documentation)
            self.models.append(model)
            json_fields = json_model.get(Json.FIELDS)
            # create fields and add to the model

            for field in json_fields:
                try:
                    name = field[Json.NAME]
                    field_type = field[Json.TYPE]
                except KeyError:
                    # we deliberately brake here if mandatory fields are not in
                    raise KeyError("Mandatory fields are not defines")

                documentation = field.get(Json.DOCUMENTATION)
                isIndex = field.get(Json.INDEX)
                if not isIndex:
                    isIndex = False
                isNullable = field.get(Json.NULLABLE)
                if not isNullable:
                    isNullable = True
                #TODO: supported for autoincreament
                isAutoIncrement = False
                if not isIndex:
                    isIndex = False
                defaultValue = field.get(Json.DEFAULT_VALUE)
                defaultValueLegacy = field.get(Json.DEFAULT_VALUE_LEGACY)
                enumName = field.get(Json.ENUM_NAME)
                enumValuesJson = field.get(Json.ENUM_VALUES)
                #TODO: fix enums
                enumValues = []
                if enumValuesJson:
                    enumValues = []
                    for eVal in enumValuesJson:
                        pass

                foreign_key_json = field.get(Json.FOREIGN_KEY)
                foreign_key= None
                isId = False
                if foreign_key_json:
                    table = foreign_key_json.get(Json.FOREIGN_KEY_TABLE)
                    on_delete = Action.from_json_name(Json.FOREIGN_KEY_ON_DELETE_ACTION)
                    foreign_key = ForeignKey(table, on_delete)

                model.add_field(__ALL__FIELDS__.get(field_type)(
                                model, name, documentation, isId, isIndex,
                                isNullable, isAutoIncrement, defaultValue, enumName,
                                enumValues, foreign_key
                                          )
                                )
                # end field loop
            #TODO check id fied creation
            id_fields = json_model.get(Json.ID_FIELD)
            id_field_name = "_id"
            id_field_obj = None
            if id_fields:
                if len(id_fields) != 1:
                    raise ValueError("Invalid number of idField ")
                id_field_name = id_fields[0]

            if "_id" == id_field_name:
                name = id_field_name
                id_field_obj = __ALL__FIELDS__.get("Long")(
                              model, name, "Primary key.",  True, False,
                              False, True, None, None, None, None
                )
                model.add_field(id_field_obj, 0)
            else:
                id_field_obj = model.get_field_by_name(id_field_name)
                if not id_field_obj:
                    raise ValueError("No just ID field %s" %id_field_name)
                if id_field_obj.type not in ["Integer", "Long", "Date", "Enum"]:
                    raise ValueError("ID field must be of type Integer, Long, Date or Enum")

                if id_field_obj.is_nullable:
                    raise ValueError("ID Field %s can not be nullable" %id_field_name)
                if not id_field_obj.is_index:
                    raise ValueError("ID Field %s must be index" %id_field_name)
                id_field_obj.set_is_id()

            # Constraints
            constraints_json = json_model.get(Json.CONSTRAINTS)
            if constraints_json:
                for constrain in constraints_json:
                    Log.debbug("constraintJson=" + str(constrain))
                    name = constrain.get(Constraint.Json.NAME)
                    definition = constrain.get(Constraint.Json.DEFINITION)
                    model.add_constrain(Constraint(name, definition))

        Models.add_model(model)
        Log.debug("Model created")
        Log.debug(model)
        Log.debug('*'*80)

    def make_manifest(self):
        pass

    def make_table_columns(self):
        pass

    def make_models(self):
        pass

    def make_wrappers(self):
        #AbstractCursor

        #AbstractContentValuesWrapper

        #AbstractSelection

        #BaseContentProvider

        #BaseModel

        #models
        for model in self.models:
            # Cursor wrapper

            # ContentValues wrapper

            # Selection builder

            # enums appending to one file
            pass

    def make_content_provider(self):
        pass

    def make_sqlite_open_helper(self):
        pass

    def make_generate_sqlite_open_helper_callbacks(self):
        pass

    def make_model_representations(self):
        pass

    def make_model_representer(self):
        pass

    def make_model_change_listner(self):
        pass

    def go(self):
        self.load_models()
        self.make_table_columns()
        self.make_table_columns()
        self.make_models()
        self.make_wrappers()
        self.make_content_provider()
        self.make_sqlite_open_helper()
        self.make_generate_sqlite_open_helper_callbacks()
        self.make_model_representations()
        self.make_model_representer()
        self.make_model_representer()
        self.make_model_change_listner()
