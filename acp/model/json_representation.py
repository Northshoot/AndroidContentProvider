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
# Created on 3/7/16.


class JsonRepresentation:
    NAME = "name"
    TYPE = "type"
    CONSTRAINTS = "constraints"
    DOCUMENTATION = "documentation"
    FIELDS = "fields"
    ID_FIELD = "idField"
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
