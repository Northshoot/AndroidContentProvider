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
# Created on 3/9/16.


class SqlBuilder:
    CONCAT = "res.tablesWithJoins += "
    HAS_COLUMNS = ".hasColumns(projection)"
    OPEN_BRACE = ") {"
    CLOSE_BRACE = "}"
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
    NEW_LINE = "\n"
    CHAR_SEMICOLON = ";"
    CHAR_DOT = "."

    @classmethod
    def add_all_joined_clauses(cls, model, alias):
        ret = ""
        for field in model.fields:
            foreign_key = field.foreign_key
            if foreign_key:
                continue
            ret += SqlBuilder.NEW_LINE
            ret += SqlBuilder.INDENT1
            ret += SqlBuilder.IF

            ret += SqlBuilder.column_clauses(foreign_key.model)
            ret += SqlBuilder.OPEN_BRACE
            ret += SqlBuilder.NEW_LINE
            ret += SqlBuilder.INDENT2
            ret += SqlBuilder.CONCAT
            ret += SqlBuilder.LEFT_OUTER_JOIN
            ret += SqlBuilder.PLUS

            ret += field.foreign_key.model.name_camel_case
            ret += SqlBuilder.COLUMNS
            ret += SqlBuilder.TABLE_NAME
            ret += SqlBuilder.PLUS
            ret += SqlBuilder.AS
            ret += SqlBuilder.PLUS
            ret += SqlBuilder.prefix(model, foreign_key)
            ret += SqlBuilder.PLUS
            ret += SqlBuilder.ON
            ret += SqlBuilder.PLUS
            ret += SqlBuilder.column_name(model, field, alias)

            ret += SqlBuilder.PLUS
            ret += SqlBuilder.EQUALS
            ret += SqlBuilder.PLUS

            ret += SqlBuilder.prefix(model, foreign_key)
            ret += SqlBuilder.PLUS
            ret += SqlBuilder.DOT
            ret += SqlBuilder.PLUS
            ret += foreign_key.model.name_camel_case
            ret += SqlBuilder.COLUMNS
            ret += SqlBuilder.CHAR_DOT
            ret += foreign_key.model.name_camel_case
            ret += SqlBuilder.SEMICOLON
            ret += SqlBuilder.NEW_LINE
            ret += SqlBuilder.INDENT1
            ret += SqlBuilder.CLOSE_BRACE
            ret += SqlBuilder.add_all_joined_clauses(foreign_key.model,
                                                      cls.table_prefix(model,
                                                                      foreign_key))
        return ret

    @classmethod
    def table_prefix(cls, model, field):
        ret = model.name_camel_case
        ret += SqlBuilder.COLUMNS
        ret += SqlBuilder.PREFIX
        ret += field.model.name_upper_case
        return ret

    @classmethod
    def column_clauses(cls, model):
        ret = model.name_camel_case
        ret += SqlBuilder.COLUMNS
        ret += SqlBuilder.HAS_COLUMNS

        for field in model.fields:
            foreign_key = field.foreign_key
            if foreign_key:
                continue
            ret += SqlBuilder.OR
            ret += cls.column_clauses(foreign_key.model)
        return ret

    @classmethod
    def column_name(cls, model, field, alias):
        ret = ""
        if alias:
            ret += alias
            ret += SqlBuilder.PLUS
        else:
            ret += model.name_camel_case
            ret += SqlBuilder.COLUMNS
            ret += SqlBuilder.TABLE_NAME
            ret += SqlBuilder.PLUS

        ret += SqlBuilder.DOT
        ret += SqlBuilder.PLUS
        ret += model.name_camel_case
        ret += SqlBuilder.COLUMNS
        ret += SqlBuilder.CHAR_DOT
        ret += field.name_upper_case
        return ret

