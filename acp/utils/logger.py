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
# Created on 3/2/16.

import logging

# create logger
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
