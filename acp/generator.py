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

from .utils.tools import get_file_names
from .app import Application
from .model.model import DataModel

class Generator:
    def __init__(self, args):
        self.args = args
        self._files = get_file_names(args.path)
        self.config_file_name = self._files[0] #fist one is config
        self.models_file_names = self._files[1:] #the rest are models
        self.app = Application(args.path, args.output, self.config_file_name)
        self.models = []
        for mf in self.models_file_names:
            self.models.append(DataModel(file_name=mf))

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
