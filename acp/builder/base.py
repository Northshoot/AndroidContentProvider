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
# Created on 2/24/16.


from jinja2 import FileSystemLoader, Environment
from ..utils.logger import logger as Log
from ..utils.tools import write_to_file
from jinja2.exceptions import TemplateNotFound


class TemplateWriter:
    def __init__(self, **kwargs):
        key = ""
        try:
            for key in ('build_path', 'file_name', 'tmpl_data'):
                setattr(self, key, kwargs[key])
        except KeyError:
            raise KeyError("Missing argument in template object %s"
                           % key)

    @property
    def render_string(self):
        """
        OBS! all templates must use data dict!
        :return: rendered sring
        """
        try:
            return self.tmpl.render(data=self.tmpl_data)
        except TemplateNotFound:
            raise TemplateNotFound("Ca't find template: %s" % self.tmpl_name)

    def render_file(self):
        Log.debug(">>Rendering to file %s in path %s." % (self.file_name,
                                                          self.build_path))
        write_to_file(self.build_path + '/' + self.file_name,
                      self.render_string)


class FileObject(TemplateWriter):
    """
    files object serve as a container for component
    the components gives write path, template, and data to the file object
    file object renders the string and provides method to write to the file

    FileObject( write_path=,
                file_name=,
                tmpl_path=,
                tmpl_name=,
                tmpl_data=)

    """

    def __init__(self, **kwargs):
        # set mandatory keywords
        super().__init__(**kwargs)
        key = None
        try:
            for key in ('tmpl_path', 'tmpl_name'):
                setattr(self, key, kwargs[key])
        except KeyError:
            raise KeyError("Missing argument in FileObject %s" % key)
        # set or create additional
        if 'tmpl_render' in kwargs:
            self.tmpl_render = kwargs['tmpl_render']
        else:
            self.tmpl_render = Environment(loader=FileSystemLoader([
                self.tmpl_path]), lstrip_blocks=True, trim_blocks=True)
        if 'tmpl' in kwargs:
            self.tmpl = kwargs['tmpl']
        else:
            self.tmpl = self.tmpl_render.get_template(self.tmpl_name)
