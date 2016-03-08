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
from .utils.logger import logger as Log


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

    __DEF__HEADER__ = \
"""
/*
 * Copyright (C) 2016 Laurynas Riliskis
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

    """

    def __init__(self, path, output_path, config):
        self.path = path
        self.output_path = output_path
        self.header = Application.__DEF__HEADER__
        with open(config, encoding='utf-8') as data_file:
            self.config = json.loads(data_file.read())

        try:
            self.PROJECT_PACKAGE_ID = self.config["appPackageName"]
            self.PROVIDER_JAVA_PACKAGE = self.PROJECT_PACKAGE_ID + \
                                             "provider"

            try:
                self.PROVIDER_CLASS_NAME = self.config["providerClassName"]
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
            Log.debug("No such configuration key: " + str(e))
            Log.debug("Config Keys:")
            Log.debug(Application.__ALL__)

        self.provider_dir = self.output_path + \
                            self.PROVIDER_JAVA_PACKAGE.replace('.','/') + "/"

    def set_header(self, header):
        self.header = header

    # def __str__(self):
    #     _str = "Application: ["
    #     for key, val in self.__dict__:
    #         _str+=key + "=" + val
    #     return _str +"]"
