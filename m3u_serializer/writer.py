import logging
from m3u_serializer.record import M3URecord

log = logging.getLogger( 'M3U-Serializer' )


class M3USerializer( object ):
    def __init__( self, filename ):
        self.__stream = None
        self.__filename = filename
        return

    def open( self ):
        log.info( f'Writing to FILE {self.__filename}' )
        self.__stream = open( self.__filename, 'w' )
        self.__stream.write( '#EXTM3U\n' )
        return

    def close( self ):
        self.__stream.close()
        self.__stream = None
        log.info( f'Writing to FILE {self.__filename} done, closed' )
        return

    def write( self, record: M3URecord ):
        attrs_str = f'tvg-id="{record.TvgId}" tvg-name="{record.TvgName }" tvg-logo="{record.TvgLogo}" group-title="{record.Group}"'
        self.__stream.write( f'#EXTINF:{record.Duration} {attrs_str},{record.Name}\n{record.Link}\n' )
        log.debug( f'Writing::\n#EXTINF:{record.Duration} {attrs_str},{record.Name}\n{record.Link}' )
        return

