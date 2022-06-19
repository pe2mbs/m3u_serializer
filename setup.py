#!/usr/bin/env python
# M3U Serializer - serialize/de-serialize M3U data streams special for IPTV
# Copyright (C) 2022  Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; only version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import sys
import setuptools
__version__ = ''
__author__ = ''
# Get the root path of the project
root_path = sys.argv[ 0 ].split( '/venv' )[ 0 ]
# Read the __version__ and __author__ inforrmation
with open( os.path.abspath( os.path.join( root_path, 'm3u_serializer', 'version.py' ) ) ) as f:
       exec( f.read() )



setuptools.setup( name             = 'm3u_serializer',
                  version          = __version__,
                  description      = 'M3U serializer/deserializer',
                  author           = __author__,
                  author_email     = 'm.bertens@pe2mbs.nl',
                  url              = 'https://www.pe2mbs.nl/M3U_Serializer/',
                  package_dir      = { "m3u_serializer": "m3u_serializer" },
                  install_requires = [
                     'requests'
                  ]
)

