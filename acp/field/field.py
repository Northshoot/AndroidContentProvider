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
# Created on 3/1/16.

from . import Json
from .type import Type
import acp.utils.tools as word_tools


class Field:
        def __init__(self, model,  name, documentation,  type,  isId,  isIndex,  isNullable,  isAutoIncrement,
             defaultValue,  enumName,  enumValues, foreignKey):
            self.type_name = dict()
            self.on_delete_action = dict()
            self.mEnumValues = []
            self.mModel = model
            self.mName = name
            self.mDocumentation = documentation
            self.mType = Type.fromJsonName(type)
            self.mIsId = isId
            self.mIsIndex = isIndex
            self.mIsNullable = isNullable
            self.mIsAutoIncrement = isAutoIncrement
            self.mDefaultValue = defaultValue
            self.mEnumName = enumName
            if enumValues:
                self.mEnumValues.addAll(enumValues)
            self.mForeignKey = foreignKey
            self.mIsAmbiguous = False

        def get_as_foreign_field(self, path, force_nullable):
            if force_nullable: self.mIsNullable = True
            res = Field(self.mEntity, self.mName, self.mDocumentation,
                        self.mType.mJsonName, self.mIsId, self.mIsIndex,
                        self.isNullable, self.mIsAutoIncrement,
                        self.mDefaultValue, self.mEnumName,
                        self.mEnumValues, self.mForeignKey)
            res.mIsForeign = True
            res.mOriginalField = self
            res.mPath = path
            return res

        @property
        def model(self): return self.mModel

        @property
        def name(self): return self.mName

        @property
        def name_upper_case(self): return self.name.upper()

        @property
        def name_lower_case(self): return self.name.lower()

        @property
        def name_camel_case(self):
            return word_tools.detect_conversion_method(self.mName)

        @property
        def name_camel_lower_case(self):
            return self.name_camel_case.lower()

        @property
        def enum_name(self): return self.mEnumName

        @property
        def enum_values(self): return self.mEnumValues

        @property
        def prefix_name(self):
            return self.model.name_lower_case + "__" + self.name_lower_case

        @property
        def name_or_prefix(self):
            if self.mIsAmbiguous: return self.prefix_name
            else: return self.mName

        @property
        def type(self): return self.type

        @property
        def is_id(self): return self.mIsId

        @property
        def is_index(self): return self.mIsIndex

        @property
        def is_auto_increment(self):
            return self.mIsAutoIncrement

        @property
        def has_default(self):
            if self.mDefaultValue:
                return True
            else:
                return False

        @property
        def sql_type(self): return self.mSqlType

        @property
        def has_not_nullable_java_type(self):
            return not self._mNullableJavaType == self._mNotNullableJavaType

        @property
        def nullable_java_type(self): return self._mNullableJavaType

        @property
        def not_nullable_java_type(self): return self._mNotNullableJavaType




"""
Particular field implementations
"""


class BooleanField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_BOOLEAN
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "String.class"
        self._mNotNullableJavaType = "String.class"
        super(BooleanField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        if self.mDefaultValue == "true":
            return "1"
        elif self.mDefaultValue == "false":
            return "0"
        else:
            raise ValueError("Models default value is not Boolean %s" %
                             self.mDefaultValue)


class IntegerField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_INTEGER
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Integer.class"
        self._mNotNullableJavaType = "int.class"
        super(IntegerField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not integer %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''


class LongField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_LONG
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Long.class"
        self._mNotNullableJavaType = "long.class"
        super(LongField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not long %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''


class DateField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_DATE
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Date.class"
        self._mNotNullableJavaType = "Date.class"
        super(DateField, self).__init__(*args, **kwargs)

    @property
    def default_value(self): return'\'' + self.mDefaultValue + '\''


class EnumField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_ENUM
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "null"
        self._mNotNullableJavaType = "null"
        super(EnumField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not ENUM %s" %
                             self.mDefaultValue)

    @property
    def has_not_nullable_java_type(self): return False


class FloatField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_FLOAT
        self.mSqlType = "REAL"
        self._mNullableJavaType = "Float.class"
        self._mNotNullableJavaType = "float.class"
        super(FloatField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not flaot %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''


class DoubleField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_DOUBLE
        self.mSqlType = "REAL"
        self._mNullableJavaType = "Double.class"
        self._mNotNullableJavaType = "double.class"
        super(DoubleField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''


class ByteArrayField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_BYTE_ARRAY
        self.mSqlType = "BLOB"
        self._mNullableJavaType = "byte[].class"
        self._mNotNullableJavaType = "byte[].class"
        super(DoubleField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''


class StringField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self._mJsonName = Json.TYPE_STRING
        self.mSqlType = "TEXT"
        self._mNullableJavaType = "String.class"
        self._mNotNullableJavaType = "String.class"
        super(DoubleField, self).__init__(*args, **kwargs)

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
        except ValueError:
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)
        return'\'' + self.mDefaultValue + '\''
