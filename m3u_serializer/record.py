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

    def __init__( self, *args, **kwargs ):
        """Constructor

        """
        self.__duration     = '-1'
        self.__name         = ''
        self.__link         = ''
        self.__attributes   = {}
        return

    def clear( self ) -> None:
        """Clear all the internal data elements

        :return:            None
        """
        self.__duration     = '-1'
        self.__name         = ''
        self.__link         = ''
        self.__attributes   = {}
        return

    ARG_DURATION    = 0
    ARG_ATTRIBUTES  = 1
    ARG_NAME        = 2
    ARG_LINK        = 3
    FULL_ARGS       = 4

    def set( self, *args, **kwargs ) -> None:
        """Sets the record object from a list of elements:
            0:      duration (str,int or float)
            1:      attributes (str or dict) [optional]
            2:      name (title)
            3:      stream link address

        :param data:            list of elements
        :return:                None
        """
        self.__duration     = args[ self.ARG_DURATION ]
        if len( args ) == self.FULL_ARGS:
            if isinstance( args[ self.ARG_ATTRIBUTES ], str ):
                for label, value in self.__RE_ATTRIBUTE.findall( args[ self.ARG_ATTRIBUTES ] ):
                    value = value.replace( '"', '' ).strip()
                    self.__attributes[ label.strip() ] = value

            elif isinstance( args[ self.ARG_ATTRIBUTES ], dict ):
                for attr, value in args[ self.ARG_ATTRIBUTES ].items():
                    self.__attributes[ attr ] = value

            offset = self.ARG_NAME

        else:
            offset = self.ARG_ATTRIBUTES

        self.__name         = args[ offset ].strip()
        offset += 1
        self.__link         = args[ offset ].strip()
        return

    @property
    def Duration( self ) -> str:
        """Gets the duration of the stream

        :return:        Returns the duration of the stream, maybe -1
        """
        return self.__duration

    @Duration.setter
    def Duration( self, value: Union[str,int,float] ):
        """Gets the duration of the stream

        :return:        Returns the duration of the stream, maybe -1
        """
        if isinstance( value, str ):
            value = value.strip()
            try:
                self.__duration = str( float( value ) )

            except:
                try:
                    self.__duration = str( int( value ) )

                except:
                    raise ValueError( 'M3URecord::Duration as string must contain a int or float' )

        elif isinstance( value, int ):
            self.__duration = str( value )

        elif isinstance( value, float ):
            self.__duration = str( value )

        else:
            self.__duration = '-1'

        return

    @property
    def Name( self ) -> str:
        """Gets the name (title) of the stream

        :return:
        """
        return self.__name

    @Name.setter
    def Name( self, value: str ):
        """Sets the name of the stream

        :param value:   string with value
        :return:        None
        """
        if isinstance( value, str ):
            self.__name = value
            return

        raise ValueError( 'M3URecord::Name must contain a string' )

    @property
    def Group( self ) -> Optional[str]:
        """When available gets the group-title otherwise an empty string

        In case of a series this shall contain the series name

        :return:        the group-title or empty string.
        """
        return self.__attributes.get( 'group-title', '' )

    @Group.setter
    def Group( self, value: str ) -> None:
        """Sets the group-title attribute

        :param value:   string with attribute value
        :return:        None
        """
        if isinstance( value, str ):
            self.__attributes[ 'group-title' ] = value
            return

        raise ValueError( 'M3URecord::Group must contain a string' )

    @property
    def Link( self ) -> str:
        """The link of the stream

        :return:        link of the stream
        """
        return self.__link

    @Link.setter
    def Link( self, value: str ) -> None:
        """Sets the link value

        :param value:   string with attribute value
        :return:        None
        """
        if isinstance( value, str ):
            self.__link = value
            return

        raise ValueError( 'M3URecord::Link must contain a string' )

    @property
    def TvgId( self ) -> Optional[str]:
        """When available gets the tvg-id otherwise an empty string

        :return:        the tvg-id or empty string.
        """
        return self.__attributes.get( 'tvg-id', '' )

    @TvgId.setter
    def TvgId( self, value: str ) -> None:
        """Sets the tvg-id attribute

        :param value:   string with attribute value
        :return:        None
        """
        if isinstance( value, str ):
            self.__attributes[ 'tvg-id' ] = value
            return

        raise ValueError( 'M3URecord::TvgId must contain a string' )

    @property
    def TvgLogo( self ) -> Optional[str]:
        """When available gets the tvg-logo otherwise an empty string

        :return:        the tvg-logo or empty string.
        """
        return self.__attributes.get( 'tvg-logo', '' )

    @TvgLogo.setter
    def TvgLogo( self, value: str ) -> None:
        """Sets the tvg-logo attribute

        :param value:   string with attribute value
        :return:        None
        """
        if isinstance( value, str ):
            self.__attributes[ 'tvg-logo' ] = value
            return

        raise ValueError( 'M3URecord::TvgLogo must contain a string' )

    @property
    def TvgName( self ) -> Optional[str]:
        """When available gets the tvg-name otherwise an empty string

        :return:        the tvg-name or empty string.
        """
        return self.__attributes.get( 'tvg-name', '' )

    @TvgName.setter
    def TvgName( self, value: str ) -> None:
        """Sets the tvg-name attribute

        :param value:   string with attribute value
        :return:        None
        """
        if isinstance( value, str ):
            self.__attributes[ 'tvg-name' ] = value
            return

        raise ValueError( 'M3URecord::TvgName must contain a string' )

    def attribute( self, key, value: Optional[str] = None ) -> Optional[str]:
        """Returns the attribute requested by key or None

        :param key:     name of the attribute
        :rtype:         str or None
        :return:        attribute value as a string
        """
        if value is None:
            return self.__attributes.get( key )

        if isinstance( value, str ):
            self.__attributes[ key ] = value
            return

        raise ValueError( f'M3URecord::attribute( {key}, value ) must contain a string' )

    def getAttributes( self ) -> str:
        """This member functions returns a string with attributes and values for writing.

        :return:    string
        """
        result = []
        for attr, value in self.__attributes.items():
            result.append( f'{attr}="{value}"' )

        return ' '.join( result )

    def __repr__(self):
        return f'<M3URecord name="{self.__name}", link="{self.__link}">'


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
        self.__number       = 9999
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
        self.__number       = 9999
        return

    def set( self, *args, **kwargs ) -> None:
        """Sets the record object from a list of elements:
            0:      duration (str,int or float)
            1:      attributes (str or dict) [optional]
            2:      name (title)
            3:      stream link address

        And detects the series, movie or TV channel and sets the extra elements as Season, Episode, Genre.
        For series the group-title is set to the series name.
        for movie and TV channel the genre is set to group-title.

        :param data:            list of elements
        :return:                None
        """
        super( M3URecordEx, self ).set( *args, **kwargs )
        result = self.__RE_SERIE.search( self.Name )
        if result:
            self.__type     = M3uItemType.SERIE_EPISODE
            groups = result.groups()
            self.__season   = groups[ 2 ].strip()
            self.__episode  = groups[ 4 ].strip()
            self.__genre    = self.Group
            self.Group      = groups[ 0 ].strip()

        else:
            self.__type     = M3uItemType.MOVIE if self.Link.endswith( tuple( self.__MEDIA_FILES ) ) else M3uItemType.IPTV_CHANNEL
            self.__genre    = self.Group
            if self.__type == M3uItemType.MOVIE:
                self.Group  = f'Movies: {self.Group}'

        for char in ( '|', ':', '-' ):
            self.Name, country = self._retrieve_country_code( self.Name, char )
            if country is not None:
                self.__country = country
                break

        for key, value in kwargs.items():
            if key == 'country':
                self.__country = value

            elif key == 'season':
                self.__season = value

            elif key == 'episode':
                self.__episode = value

            elif key == 'genre':
                self.__genre = value

            elif key == 'type':
                self.__type = value

            elif key == 'number':
                self.__number = value

            else:
                self.attribute( key, value )

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
    def ChannelNumber( self ) -> int:
        return self.__number

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

    @property
    def Season( self ) -> str:
        return self.__season

    @property
    def Episode( self ) -> str:
        return self.__episode

    @property
    def Country( self ) -> str:
        return self.__country