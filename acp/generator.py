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
import json
import os
from .utils.tools import get_file_names
from .app import Application
from .utils.logger import logger as Log
from .model import JsonRepresentation as Json, Models, DataModel
from .model import Action, ForeignKey, __ALL__FIELDS__, Constraint
from .builder.base import FileObject


class Generator:
    def __init__(self, args):
        self.args = args
        self._files = get_file_names(args.path)
        self.config_file_name = self._files[0]  # fist one is config
        self.models_file_names = self._files[1:]  # the rest are models
        Log.debug("Model to load: " + str(self._files))
        self.app = Application(args.path, args.output, self.config_file_name)
        self.tmpl_path = os.path.dirname(os.path.realpath(__file__)) + \
                         "/templates/"
        self.output_dir = self.args.output
        self.models = []
        self.config = dict()
        self.config['header'] = Application.__DEF__HEADER__

    def load_models(self):
        # load files
        for mFile in self.models_file_names:
            Log.debug("Model path: " + self.args.path + mFile)
            model_name = mFile.split('.json')[0]
            Log.debug("Model name: " + model_name)
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
                # TODO: supported for autoincreament
                isAutoIncrement = False
                if not isIndex:
                    isIndex = False
                defaultValue = field.get(Json.DEFAULT_VALUE)
                defaultValueLegacy = field.get(Json.DEFAULT_VALUE_LEGACY)
                enumName = field.get(Json.ENUM_NAME)
                enumValuesJson = field.get(Json.ENUM_VALUES)
                # TODO: fix enums
                enumValues = []
                if enumValuesJson:
                    enumValues = []
                    for eVal in enumValuesJson:
                        pass

                foreign_key_json = field.get(Json.FOREIGN_KEY)
                foreign_key = None
                isId = False
                if foreign_key_json:
                    table = foreign_key_json.get(Json.FOREIGN_KEY_TABLE)
                    on_delete = Action.from_json_name(
                        Json.FOREIGN_KEY_ON_DELETE_ACTION)
                    foreign_key = ForeignKey(table, on_delete)

                model.add_field(__ALL__FIELDS__.get(field_type)(
                    model, name, documentation, isId, isIndex,
                    isNullable, isAutoIncrement, defaultValue, enumName,
                    enumValues, foreign_key
                )
                )
                # end field loop
            # TODO check id fied creation
            id_fields = json_model.get(Json.ID_FIELD)
            id_field_name = "_id"
            if id_fields:
                if len(id_fields) != 1:
                    raise ValueError("Invalid number of idField ")
                id_field_name = id_fields[0]
            if "_id" == id_field_name:
                name = id_field_name
                id_field_obj = __ALL__FIELDS__.get("Long")(
                    model, name, "Primary key.", True, False,
                    False, True, None, None, None, None
                )
                model.add_id_field(id_field_obj)
            else:
                id_field_obj = model.get_field_by_name(id_field_name)
                if not id_field_obj:
                    raise ValueError("No just ID field %s" % id_field_name)
                if id_field_obj.type not in ["Integer", "Long", "Date", "Enum"]:
                    raise ValueError(
                        "ID field must be of type Integer, Long, Date or Enum")

                if id_field_obj.is_nullable:
                    raise ValueError(
                        "ID Field %s can not be nullable" % id_field_name)
                if not id_field_obj.is_index:
                    raise ValueError(
                        "ID Field %s must be index" % id_field_name)
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
        Log.debug('*' * 80)

    def make_manifest(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['models'] = Models.ALL_DATA_MODELS
        file_name = "provider_manifest_data.txt"
        Log.info("Provider declaration to paste in the AndroidManifest.xml "
                 "file is located in the file: %s" % file_name)
        template = FileObject(build_path=self.app.output_path,
                              file_name=file_name,
                              tmpl_path=self.tmpl_path,
                              tmpl_name='manifest.tmpl',
                              tmpl_data=tmpl_data
                              )
        template.render_file()

    def make_table_columns(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['all_models'] = Models.get_models()
        for model in Models.get_models():
            tmpl_data['model'] = model
            template = FileObject(build_path=self.app.provider_dir +
                                             model.name_lower_case + "/",
                                  file_name=model.name_camel_case + "Columns.java",
                                  tmpl_path=self.tmpl_path,
                                  tmpl_name='columns.tmpl',
                                  tmpl_data=tmpl_data
                                  )
            template.render_file()

    def make_models(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['all_models'] = Models.get_models()
        for model in Models.get_models():
            tmpl_data['model'] = model
            template = FileObject(build_path=self.app.provider_dir +
                                             model.name_lower_case + "/",
                                  file_name=model.name_camel_case +
                                            "Model.java",
                                  tmpl_path=self.tmpl_path,
                                  tmpl_name='model.tmpl',
                                  tmpl_data=tmpl_data
                                  )
            template.render_file()

    def make_wrappers(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['all_models'] = Models.get_models()
        out_dir = self.app.provider_dir + "base/"
        # AbstractCursor
        template = FileObject(build_path=out_dir,
                              file_name="AbstractCursor.java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='abstractcursor.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

        # AbstractContentValuesWrapper
        template = FileObject(build_path=out_dir,
                              file_name="AbstractContentValues.java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='abstractcontentvalues.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

        # AbstractSelection
        template = FileObject(build_path=out_dir,
                              file_name="AbstractSelection.java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='abstractselection.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

        # BaseContentProvider
        template = FileObject(build_path=out_dir,
                              file_name="BaseContentProvider.java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='basecontentprovider.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

        # BaseModel
        template = FileObject(build_path=out_dir,
                              file_name="BaseModel.java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='abstractmodel.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

        # models
        for model in self.models:
            # Cursor wrapper
            model_name = model.name_camel_case
            tmpl_data['model'] = model
            out_dir = self.app.provider_dir + model.package_name + "/"
            template = FileObject(build_path=out_dir,
                                  file_name=model_name + "Cursor.java",
                                  tmpl_path=self.tmpl_path,
                                  tmpl_name='cursor.tmpl',
                                  tmpl_data=tmpl_data
                                  )

            template.render_file()
            # ContentValues wrapper
            template = FileObject(build_path=out_dir,
                                  file_name=model_name + "ContentValues.java",
                                  tmpl_path=self.tmpl_path,
                                  tmpl_name='contentvalues.tmpl',
                                  tmpl_data=tmpl_data
                                  )

            template.render_file()

            # Selection builder
            template = FileObject(build_path=out_dir,
                                  file_name=model_name + "Selection.java",
                                  tmpl_path=self.tmpl_path,
                                  tmpl_name='selection.tmpl',
                                  tmpl_data=tmpl_data
                                  )
            template.render_file()

            # enums appending to one file
            for field in model.fields:
                if field.is_enum:
                    tmpl_data['field'] = field
                    template = FileObject(build_path=out_dir,
                                          file_name=field.enum_name + ".java",
                                          tmpl_path=self.tmpl_path,
                                          tmpl_name='enum.tmpl',
                                          tmpl_data=tmpl_data
                                          )

                    template.render_file()

    def make_content_provider(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['models'] = Models.ALL_DATA_MODELS
        template = FileObject(build_path=self.app.provider_dir,
                              file_name=self.app.PROVIDER_CLASS_NAME + ".java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='contentprovider.tmpl',
                              tmpl_data=tmpl_data
                              )

        template.render_file()

    def make_sqlite_open_helper(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['models'] = Models.ALL_DATA_MODELS
        template = FileObject(build_path=self.app.provider_dir,
                              file_name=self.app.SQLITE_OPEN_HELPER_CLASS_NAME + ".java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='sqliteopenhelper.tmpl',
                              tmpl_data=tmpl_data
                              )
        template.render_file()

    def make_generate_sqlite_open_helper_callbacks(self):
        tmpl_data = dict()
        tmpl_data['config'] = self.app
        tmpl_data['models'] = Models.ALL_DATA_MODELS
        template = FileObject(build_path=self.app.provider_dir,
                              file_name=self.app.SQLITE_OPEN_HELPER_CALLBACKS_CLASS_NAME + ".java",
                              tmpl_path=self.tmpl_path,
                              tmpl_name='sqliteopenhelpercallbacks.tmpl',
                              tmpl_data=tmpl_data
                              )
        template.render_file()

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
        self.make_manifest()
        self.make_model_representations()
        self.make_model_representer()
        self.make_model_change_listner()
