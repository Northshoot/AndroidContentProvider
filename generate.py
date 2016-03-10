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

import argparse
import os
import sys
from acp.generator import Generator

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
    parser = argparse.ArgumentParser(description='Part of Ravel framework '
                                                 'that generates models and '
                                                 'DB fro Android.')
    parser.add_argument('-p', '--path', help='Directory where model and '
                                             'config files are store',
                        required=True)
    parser.add_argument('-o', '--output', help='Directory where the files will '
                                               'be writen, if non local gen/ '
                                               'will be created',
                        required=False)
    args = parser.parse_args()
    full_path = os.path.dirname(os.path.realpath(__file__))
    if args.path == '.':
        args.path = full_path

    if args.output == '.':
        args.output = args.path + '/gen/'

    Generator(args).go()
