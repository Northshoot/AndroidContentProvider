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

import ast
import json

class Application:
    """
    Class holding application level configuration
    """
    __ALL__ ="appPackageName\n" \
             "providerJavaPackage\n" \
             "providerClassName\n" \
             "authority\n" \
             "databaseFileName\n" \
             "databaseVersion\n" \
             "enableForeignKeys\n" \
             "useAnnotations\n" \

    def __init__(self, path, output_path, config):
        self.path = path
        self.output_path = output_path
        self.config = []
        print(config)
        with open(config, encoding='utf-8') as data_file:
            self.config = json.loads(data_file.read())

        print(self.config)
        try:
            self.PROJECT_PACKAGE_ID = self.config["appPackageName"]
            self.PROVIDER_JAVA_PACKAGE = self.PROJECT_PACKAGE_ID + \
                                             "provider"

            try:
                self.PROVIDER_CLASS_NAME = self.config[
                                             "appPackageName"]+"provider"
            except KeyError:
                self.PROVIDER_CLASS_NAME = "RavelProvider"
            try:
                self.SQLITE_OPEN_HELPER_CLASS_NAME = "sqliteOpenHelperClassName"
            except KeyError:
                self.SQLITE_OPEN_HELPER_CLASS_NAME = "RavelSQLiteOpenHelper"
            try:
                self.SQLITE_OPEN_HELPER_CALLBACKS_CLASS_NAME = self.config["sqliteOpenHelperCallbacksClassName"]
            except KeyError:
                self.SQLITE_OPEN_HELPER_CALLBACKS_CLASS_NAME = \
                    "RavelSQLiteOpenHelperCallbacks"
            try:
                self.AUTHORITY = self.config["authority"]
            except KeyError:
                self.AUTHORITY = self.PROVIDER_JAVA_PACKAGE

            try:
                self.DATABASE_FILE_NAME = "databaseFileName"
            except KeyError:
                self.DATABASE_FILE_NAME = "ravel.db"
            try:
                self.DATABASE_VERSION = "databaseVersion"
            except KeyError:
                self.DATABASE_VERSION = 2

            self.ENABLE_FOREIGN_KEY = "enableForeignKeys"
            self.USE_ANNOTATIONS = "useAnnotations"
        except KeyError as e:
            print("No such configuration key: " + str(e))
            print("Config Keys:")
            print(Application.__ALL__)

    # def __str__(self):
    #     _str = "Application: ["
    #     for key, val in self.__dict__:
    #         _str+=key + "=" + val
    #     return _str +"]"
