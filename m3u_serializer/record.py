import re
from enum import Enum


class M3uItemType( Enum ):
    NONE            = 0
    IPTV_CHANNEL    = 1
    SERIE_EPISODE   = 2
    MOVIE           = 3


""" Translate
    'EX YU', 'EX-YU'    => 'YU'
    'CA-FR'             => 'FR'
    'NL H265'           => 'NL'
    'NL HEVC'           => 'NL'
    'SE VIP'            => 'SE'
    'NO VIP'            => 'NO'
    'PL VIP'            => 'PL'
    'RO(L)'             => 'RO'
"""


class M3URecord( object ):
    __RE_ATTRIBUTE  = re.compile( r"(\w*-\w*)=([\"'].*?[\"'])" )
    __RE_SERIE      = re.compile( r'([\W\w\s\d&!-_]+)(([Ss]\d{1,2})([ -]+|)([EeXx]\d{1,2}))', re.UNICODE )
    __COUNTRY_CODES = [ 'UK', 'FR', 'PL', 'US', 'NL', 'BE', 'DE', 'SE', 'DK', 'ES', 'NO', 'RO', 'PT', 'TR', 'IN', 'AR', 'IE', 'IT', 'AF', 'CA', 'AL',
                        'GR', 'HU', 'BG', 'YU', 'FI', 'PK', 'RU', 'PB' ]
    def __init__( self, media_files = None, detect_media = True ):
        self.__detect_media = detect_media
        self.__type         = M3uItemType.NONE
        self.__MEDIA_FILES  = [ '.mp4', '.avi', '.mkv', '.flv' ]
        self.__duration     = -1
        self.__name         = ''
        self.__link         = ''
        self.__season       = ''
        self.__episode      = ''
        self.__group        = ''
        self.__genre        = ''
        self.__attributes   = {}
        self.__tvg_id       = ''
        self.__tvg_logo     = ''
        self.__tvg_name     = ''
        self.__country      = ''
        if isinstance( media_files, ( list, tuple ) ):
            for item in media_files:
                if item not in self.__MEDIA_FILES:
                    self.__MEDIA_FILES.append( item )

        return

    def clear( self ):
        self.__type         = M3uItemType.NONE
        self.__duration     = -1
        self.__name         = ''
        self.__link         = ''
        self.__season       = ''
        self.__episode      = ''
        self.__group        = ''
        self.__genre        = ''
        self.__attributes   = {}
        self.__tvg_id       = ''
        self.__tvg_logo     = ''
        self.__tvg_name     = ''
        self.__country      = ''
        return

    def set( self, data: list ):
        self.__duration     = int( data[ 0 ].strip() )
        self.__name         = data[ 3 ].strip()
        self.__link         = data[ 4 ].strip()
        for label, value in self.__RE_ATTRIBUTE.findall( data[ 2 ] ):
            value = value.replace( '"', '' ).strip()
            if label == 'tvg-id':
                self.__tvg_id   = value

            elif label == 'tvg-logo':
                self.__tvg_logo = value

            elif label == 'tvg-name':
                self.__tvg_name = value

            elif label == 'group-title':
                self.__group    = value

            else:
                self.__attributes[ label.strip() ] = value

        if self.__detect_media:
            result = self.__RE_SERIE.search( self.__name )
            if result:
                self.__type     = M3uItemType.SERIE_EPISODE
                groups = result.groups()
                self.__season   = groups[ 2 ].strip()
                self.__episode  = groups[ 4 ].strip()
                self.__genre    = self.__group
                self.__group    = groups[ 0 ].strip()

            else:
                self.__type     = M3uItemType.MOVIE if self.__link.endswith( tuple( self.__MEDIA_FILES ) ) else M3uItemType.IPTV_CHANNEL
                self.__genre    = self.__group
                if self.__type == M3uItemType.MOVIE:
                    self.__group    = f'Movies: {self.__group}'

        for char in ( '|', ':', '-' ):
            self.__name, country = self.ripCountryCode( self.__name, char )
            if country is not None:
                self.__country = country
                break

        return

    def ripCountryCode( self, name, char ):
        country = None
        names = [ item.strip() for item in name.split( char, 1 ) ]
        if len( names ) > 1:
            prefix, suffix = names
            if len( prefix ) == 2 and prefix in self.__COUNTRY_CODES:
                name = suffix
                country = prefix

            elif len( suffix ) == 2 and suffix in self.__COUNTRY_CODES:
                name = prefix
                country = suffix

        return ( name, country )

    def __repr__(self):
        return f"<M3URecord name='{self.__name}' group='{self.__group}' link='{self.__link}'>"

    @property
    def Type( self ) -> M3uItemType:
        return self.__type

    @property
    def TypeStr( self ) -> str:
        return str( self.__type )

    @property
    def Duration( self ) -> int:
        return self.__duration

    @property
    def Name( self ) -> str:
        return self.__name

    @property
    def Group( self ) -> str:
        return self.__group

    @property
    def Genre( self ) -> str:
        return self.__genre

    @property
    def Link( self ) -> str:
        return self.__link

    @property
    def TvgId( self ):
        return self.__tvg_id

    @property
    def TvgLogo( self ):
        return self.__tvg_logo

    @property
    def TvgName( self ):
        return self.__tvg_name

    def attribute( self, key ):
        return self.__attributes.get( key )

    @staticmethod
    def matchList( ilist: list, data: str ):
        for item in ilist:
            if re.match( item, data, re.IGNORECASE ) is not None:
                return True

        return False
