#!/usr/bin/env python

from distutils.core import setup

setup( name             = 'M3U_serializer',
       version           = '0.1.0',
       description       = 'M3U serializer/deserializer',
       author            = 'Marc Bertens-Nguyen',
       author_email      = 'm.bertens@pe2mbs.nl',
       url               = 'https://www.pe2mbs.nl/M3U_Serializer/',
       packages          = ['m3u_serializer' ],
       install_requires  = [
             'requests'
       ]
)

