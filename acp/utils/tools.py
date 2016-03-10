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
# Created on 2/29/16.

import os
import sys
import os.path


def get_file_names(path, extension='.json'):
    """
    get a list of models and configuration from the given directory
    :param path: path to the directory containing files
    :param extension: extension of config files
    :return: alphabetically sorted list of file names
    """
    fn = os.listdir(path)
    l = []
    for f in fn:
        if f.endswith(extension, 4):
            l.append(f)
    l = sorted(l)
    return l


#
# CREDIT: http://wiki.geany.org/howtos/convert_camelcase
def camel_case_to_lower_case_underscore(string):
    """
    Split string by upper case letters.

    F.e. useful to convert camel case strings to underscore separated ones.

    @return words (list)
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(string):
        if char.isupper() and from_char_position < current_char_position:
            words.append(
                string[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(string[from_char_position:].lower())
    return '_'.join(words)


def lower_case_underscore_to_camel_case(string):
    """Convert string or unicode from lower-case underscore to camel-case"""
    splitted_string = string.split('_')
    # use string's class to work on the string to keep its type
    class_ = string.__class__
    return class_.join('', map(class_.capitalize, splitted_string))


def detect_conversion_method(data):
    if '_' in data:
        return lower_case_underscore_to_camel_case(data)
    else:
        return camel_case_to_lower_case_underscore(data)


def write_to_file(file_name, data):
    try:
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        open(file_name, 'wt').write(data)
    except IOError as e:
        eno, strerror = e.args
        print("Filename {0} resulted in I/O error({1}): {2}".format(file_name,
                                                                    eno,
                                                                    strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


if __name__ == '__main__':
    print(lower_case_underscore_to_camel_case("ledmodel"))
