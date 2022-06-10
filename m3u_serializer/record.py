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
import re
from typing import Union, Optional
from enum import Enum


class M3uItemType( Enum ):
    NONE            = 0
    IPTV_CHANNEL    = 1
    SERIE_EPISODE   = 2
    MOVIE           = 3


class M3URecord( object ):
    """Contains the data elements of the M3U record

    """
    __RE_ATTRIBUTE      = re.compile( r"(\w*-\w*)=([\"'].*?[\"'])" )

    # Supported attributes by class
    __ATTR_TVG_ID       = 'tvg-id'
    __ATTR_TVG_LOGO     = 'tvg-logo'
    __ATTR_TVG_NAME     = 'tvg-name'
    __ATTR_GROUP_TITLE  = 'group-title'

    def __init__( self, *args, **kwargs ):
        """Constructor

        """
        self.__duration     = -1
        self.__name         = ''
        self.__link         = ''
        self.__group        = ''
        self.__attributes   = {}
        self.__tvg_id       = ''
        self.__tvg_logo     = ''
        self.__tvg_name     = ''
        return

    def clear( self ) -> None:
        """Clear all the internal data elements

        :return:            None
        """
        self.__duration     = -1
        self.__name         = ''
        self.__link         = ''
        self.__group        = ''
        self.__attributes   = {}
        self.__tvg_id       = ''
        self.__tvg_logo     = ''
        self.__tvg_name     = ''
        return

    def set( self, data: list ) -> None:
        """Sets the record object from a list of elements:
            0:      duration
            1:      duration-fraction
            2:      attributes
            3:      name (title)
            4:      stream link address

        :param data:            list of elements
        :return:                None
        """
        self.__duration     = int( data[ 0 ].strip() )
        self.__name         = data[ 3 ].strip()
        self.__link         = data[ 4 ].strip()
        for label, value in self.__RE_ATTRIBUTE.findall( data[ 2 ] ):
            value = value.replace( '"', '' ).strip()
            if label == self.__ATTR_TVG_ID:
                self.__tvg_id   = value

            elif label == self.__ATTR_TVG_LOGO:
                self.__tvg_logo = value

            elif label == self.__ATTR_TVG_NAME:
                self.__tvg_name = value

            elif label == self.__ATTR_GROUP_TITLE:
                self.__group    = value

            else:
                self.__attributes[ label.strip() ] = value

        return

    @property
    def Duration( self ) -> int:
        """Gets the duration of the stream

        :return:        Returns the duration of the stream, maybe -1
        """
        return self.__duration

    @property
    def Name( self ) -> str:
        """Gets the name (title) of the stream

        :return:
        """
        return self.__name

    @Name.setter
    def Name( self, value: str ):
        self.__name = value
        return

    @property
    def Group( self ) -> Optional[str]:
        """When available gets the group-title otherwise an empty string

        In case of a series this shall contain the series name

        :return:        the group-title or empty string.
        """
        return self.__group if self.__group is not None else ""


    @property
    def Link( self ) -> str:
        """The link of the stream

        :return:        link of the stream
        """
        return self.__link

    @property
    def TvgId( self ) -> Optional[str]:
        """When available gets the tvg-id otherwise an empty string

        :return:        the tvg-id or empty string.
        """
        return self.__tvg_id if self.__tvg_id is not None else ""

    @property
    def TvgLogo( self ) -> Optional[str]:
        """When available gets the tvg-logo otherwise an empty string

        :return:        the tvg-logo or empty string.
        """
        return self.__tvg_logo if self.__tvg_logo is not None else ""

    @property
    def TvgName( self ) -> Optional[str]:
        """When available gets the tvg-name otherwise an empty string

        :return:        the tvg-name or empty string.
        """
        return self.__tvg_name if self.__tvg_name is not None else ""

    def attribute( self, key ) -> Optional[str]:
        """Returns the attribute requested by key or None

        :param key:     name of the attribute
        :rtype:         str or None
        :return:        attribute value as a string
        """
        return self.__attributes.get( key )


class M3URecordEx( M3URecord ):
    """By default the following extensions are recognized as movie or serie. when in the name Sxx Exx is detected in the title
    the type is assigned to

    """
    __RE_SERIE      = re.compile( r'([\W\w\s\d&!-_]+)(([Ss]\d{1,2})([ -]+|)([EeXx]\d{1,2}))', re.UNICODE )
    __COUNTRY_CODES = [ 'UK', 'FR', 'PL', 'US', 'NL', 'BE', 'DE', 'SE', 'DK', 'ES', 'NO', 'RO', 'PT', 'TR', 'IN', 'AR', 'IE', 'IT', 'AF', 'CA', 'AL',
                        'GR', 'HU', 'BG', 'YU', 'FI', 'PK', 'RU', 'PB' ]
    __COUNTRY_TRANSLATES    = {
        'EX YU': 'YU',
        'EX-YU': 'YU',
        'CA-FR': 'FR',
        'NL H265': 'NL',
        'NL HEVC': 'NL',
        'SE VIP': 'SE',
        'NO VIP': 'NO',
        'PL VIP': 'PL',
        'RO(L)': 'RO'
    }

    def __init__( self, media_files: Optional[list] = None ):
        """

        :param media_files:     optional
        """
        super( M3URecordEx, self ).__init__()
        self.__type         = M3uItemType.NONE
        self.__MEDIA_FILES  = [ '.mp4', '.avi', '.mkv', '.flv' ]
        self.__season       = ''
        self.__episode      = ''
        self.__genre        = ''
        self.__country      = ''
        if isinstance( media_files, ( list, tuple ) ):
            for item in media_files:
                if item not in self.__MEDIA_FILES:
                    self.__MEDIA_FILES.append( item )

        return

    def clear( self ) -> None:
        """Clear all the internal data elements

        :return:            None
        """
        super( M3URecordEx, self ).clear()
        self.__type         = M3uItemType.NONE
        self.__season       = ''
        self.__episode      = ''
        self.__genre        = ''
        self.__country      = ''
        return

    def set( self, data: list ) -> None:
        """Sets the record object from a list of elements:
            0:      duration
            1:      duration-fraction
            2:      attributes
            3:      name (title)
            4:      stream link address

        And detects the series, movie or TV channel and sets the extra elements as Season, Episode, Genre.
        For series the group-title is set to the series name.
        for movie and TV channel the genre is set to group-title.

        :param data:            list of elements
        :return:                None
        """
        super( M3URecordEx, self ).set( data )
        result = self.__RE_SERIE.search( self.Name )
        if result:
            self.__type     = M3uItemType.SERIE_EPISODE
            groups = result.groups()
            self.__season   = groups[ 2 ].strip()
            self.__episode  = groups[ 4 ].strip()
            self.__genre    = self.Group
            self.__group    = groups[ 0 ].strip()

        else:
            self.__type     = M3uItemType.MOVIE if self.Link.endswith( tuple( self.__MEDIA_FILES ) ) else M3uItemType.IPTV_CHANNEL
            self.__genre    = self.Group
            if self.__type == M3uItemType.MOVIE:
                self.__group    = f'Movies: {self.__group}'

        for char in ( '|', ':', '-' ):
            self.Name, country = self._retrieve_country_code( self.Name, char )
            if country is not None:
                self.__country = country
                break

        return

    def _retrieve_country_code( self, name: str, char: str ):
        """This retrieve the country code from the 'name' string,

        :param name:        May be the title of the stream or the group-title
        :pẗype name:        str
        :param char:        character to be used to split the title and country code.
        :pẗype char:        str
        :rtype:             tuple
        :return:            tuple of two elements ( <title>, <country-code> ), where country-code maybe None when not found

        """
        country = None
        names = [ item.strip() for item in name.split( char, 1 ) ]
        if len( names ) > 1:
            prefix, suffix = names
            if prefix in self.__COUNTRY_TRANSLATES:
                prefix = self.__COUNTRY_TRANSLATES[ prefix ]

            if suffix in self.__COUNTRY_TRANSLATES:
                suffix = self.__COUNTRY_TRANSLATES[ suffix ]

            if len( prefix ) == 2 and prefix in self.__COUNTRY_CODES:
                name = suffix
                country = prefix

            elif len( suffix ) == 2 and suffix in self.__COUNTRY_CODES:
                name = prefix
                country = suffix

        return name, country

    def __repr__(self):
        return f"<M3URecordEx name='{self.Name}' group='{self.Group}' link='{self.Link}'>"

    @property
    def Type( self ) -> M3uItemType:
        """Type of M3U record

        :rtype:         M3uItemType
        """
        return self.__type

    @property
    def TypeStr( self ) -> str:
        """Type string of M3U record

        :rtype:         str
        :return:        returns string with 'NONE', 'IPTV_CHANNEL', 'SERIE_EPISODE' or 'MOVIE'
        """
        return str( self.__type )

    @property
    def Genre( self ) -> Optional[str]:
        """This is the same as group-title for series.

        :rtype:         str
        :return:        group-title for series.
        """
        return self.__genre if self.__genre is not None else ""

