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

from . import JsonRepresentation
import acp.utils.tools as word_tools
from acp.utils.logger import logger as Log




class Field:
        def __init__(self, model,  name, documentation,  isId,  isIndex,
                     isNullable,  isAutoIncrement, defaultValue,  enumName,
                     enumValues, foreign_key):
            self.mEnumValues = []
            self.mModel = model
            self.mName = name
            self.mDocumentation = documentation
            self.mIsId = isId
            self.mIsIndex = isIndex
            self.mIsNullable = isNullable
            self.mIsAutoIncrement = isAutoIncrement
            self.mDefaultValue = defaultValue
            self.mEnumName = enumName
            self.mIsForeign = False
            if enumValues:
                self.mEnumValues + enumValues
            self.mForeignKey = foreign_key
            self.mIsAmbiguous = False

        def get_as_foreign_field(self, path, force_nullable):
            if force_nullable:
                self.mIsNullable = True
            res = Field(self.mModel, self.mName, self.mDocumentation,
                        self.mType.mJsonName, self.mIsId, self.mIsIndex,
                        self.mIsNullable, self.mIsAutoIncrement,
                        self.mDefaultValue, self.mEnumName,
                        self.mEnumValues, self.mForeignKey)
            res.mIsForeign = True
            res.mOriginalField = self
            res.mPath = path
            return res

        def __str__(self):
            return "Field [mName=" + str(self.mName) + ", " \
                   "mDocumentation=" + str(self.mDocumentation) + \
                   ", mType=" + str(self.mType) + ", mIsId=" + str(self.mIsId) + ", " \
                   "mIsIndex=" + str(self.mIsIndex) + \
                   ", mIsNullable=" + str(self.mIsNullable) + \
                   ", mIsAutoIncrement=" + str(self.mIsAutoIncrement) + \
                   ", mDefaultValue=" + str(self.mDefaultValue) + \
                   ", mEnumName=" + str(self. mEnumName) + \
                   ", mEnumValues=" + str(self.mEnumValues) + \
                   ", mForeignKey=" + str(self.mForeignKey) + "]"



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
            return word_tools.lower_case_underscore_to_camel_case(self.mName)

        @property
        def name_camel_lower_case(self):
            return self.name_camel_case.lower()

        @property
        def enum_name(self): return self.mEnumName

        @property
        def enum_values(self): return self.mEnumValues

        @property
        def prefix_name(self):
            return self.model.name_lower_case + "_" + self.name_lower_case

        @property
        def name_or_prefix(self):
            if self.mIsAmbiguous:
                return self.prefix_name
            else:
                return self.mName

        @property
        def type(self): return self.mType

        @property
        def is_ambiguous(self): return self.mIsAmbiguous

        @property
        def is_id(self): return self.mIsId

        def set_is_id(self): self.mIsId = True

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
        def is_nullable(self): return self.mIsNullable

        @property
        def has_not_nullable_java_type(self):
            return not self._mNullableJavaType == self._mNotNullableJavaType

        @property
        def nullable_java_type(self): return self._mNullableJavaType

        @property
        def not_nullable_java_type(self): return self._mNotNullableJavaType

        @property
        def simple_java_name(self):
            if self.mIsNullable:
                return self.nullable_java_type
            if not self.mIsNullable:
                return self.not_nullable_java_type

        @property
        def foreign_key(self): return self.mForeignKey

        @property
        def is_foreign_key(self): return self.mIsForeign

        def set_is_ambiguous(self, val=True):
            self.mIsAmbiguous = val

        @property
        def function_cursor_get_or_null(self):
            return "get"+self._mNullableJavaType + "OrNull"


class BooleanField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)
        self.mType = "BOOLEAN"
        self._mJsonName = JsonRepresentation.TYPE_BOOLEAN
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Boolean"
        self._mNotNullableJavaType = "boolean"
        Log.debug("Created: " + self.__str__())

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
        self.mType = "INTEGER"
        self._mJsonName = JsonRepresentation.TYPE_INTEGER
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Integer"
        self._mNotNullableJavaType = "int"
        super(IntegerField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not integer %s" %
                             self.mDefaultValue)


class LongField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "LONG"
        self._mJsonName = JsonRepresentation.TYPE_LONG
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Long"
        self._mNotNullableJavaType = "long"
        super(LongField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not long %s" %
                             self.mDefaultValue)


class DateField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "DATE"
        self._mJsonName = JsonRepresentation.TYPE_DATE
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "Date"
        self._mNotNullableJavaType = self._mNullableJavaType
        super(DateField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self): return'\'' + self.mDefaultValue + '\''


class EnumField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "ENUM"
        self._mJsonName = JsonRepresentation.TYPE_ENUM
        self.mSqlType = "INTEGER"
        self._mNullableJavaType = "null"
        self._mNotNullableJavaType = "null"
        super(EnumField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            int(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not ENUM %s" %
                             self.mDefaultValue)

    @property
    def has_not_nullable_java_type(self): return False

    @property
    def simple_java_name(self): return "null"


class FloatField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "FLOAT"
        self._mJsonName = JsonRepresentation.TYPE_FLOAT
        self.mSqlType = "REAL"
        self._mNullableJavaType = "Float"
        self._mNotNullableJavaType = "float"
        super(FloatField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not float %s" %
                             self.mDefaultValue)


class DoubleField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "DOUBLE"
        self._mJsonName = JsonRepresentation.TYPE_DOUBLE
        self.mSqlType = "REAL"
        self._mNullableJavaType = "Double"
        self._mNotNullableJavaType = "double"
        super(DoubleField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)


class ByteArrayField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "BYTE_ARRAY"
        self._mJsonName = JsonRepresentation.TYPE_BYTE_ARRAY
        self.mSqlType = "BLOB"
        self._mNullableJavaType = "byte[]"
        self._mNotNullableJavaType = "byte[]"
        super(ByteArrayField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)


class StringField(Field):
    """

    """

    def __init__(self, *args, **kwargs):
        self.mType = "STRING"
        self._mJsonName = JsonRepresentation.TYPE_STRING
        self.mSqlType = "TEXT"
        self._mNullableJavaType = "String"
        self._mNotNullableJavaType = "String"
        super(StringField, self).__init__(*args, **kwargs)
        Log.debug("Created: " + self.__str__())

    @property
    def default_value(self):
        try:
            float(self.mDefaultValue)
            return'\'' + self.mDefaultValue + '\''
        except ValueError:
            Log.error("Error in getting default value from: " + self.__str__())
            raise ValueError("Models default value is not double %s" %
                             self.mDefaultValue)


class EnumValue(Field):
    """

    """
    def __init__(self, name, documentation):
        super(StringField, self).__init__(name, documentation)
        Log.debug("Created: " + self.__str__())
        self.mName = name
        self.mDocumentation = documentation


    @property
    def name(self): return self.mName

    @property
    def get_documentation(self): return self.mDocumentation

