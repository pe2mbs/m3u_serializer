import re
import requests
import logging
from m3u_serializer.record import M3uItemType, M3URecord

log = logging.getLogger( 'M3U-Deserializer' )


class M3UDeserializer( object ):
    __RE_ITEM         = re.compile( r"(?:^|\n)#EXTINF:((?:-)\d+(\.\d+)?)([^,]+)?,([A-Z].*?)[\r\n]+(.*)" )
    __RE_ATTRIBUTE    = re.compile( r"(\w*-\w*)=([\"'].*?[\"'])" )
    __RE_SERIE        = re.compile( r'([\w\s&!-_]+)(([Ss]\d{1,2})([ -]+|)([EeXx]\d{1,2}))' )

    def __init__( self, url_filename, store_filename = None, media_files = None, **kwargs ):
        self.__DATA             = ''
        self.__MEDIA_FILES      = [ '.mp4', '.avi', '.mkv', '.flv' ]
        self.__store_filename   = store_filename
        self.__kwargs           = kwargs
        if isinstance( media_files, ( list, tuple ) ):
            for item in media_files:
                if item not in self.__MEDIA_FILES:
                    self.__MEDIA_FILES.append( item )

        if url_filename.startswith( ( 'http://', 'https://' ) ):
            self.__downloadUrl( url_filename )

        elif url_filename.startswith( 'file://' ):
            self.__openFile( url_filename[ 7: ] )

        else:
            self.__openFile( url_filename )

        return

    def __openFile( self, filename ):
        log.info( f'Loading FILE {filename}' )
        self.__DATA = open( filename, 'r' ).read()
        log.info( f'Size of loaded data {len(self.__DATA)}' )
        return

    def __downloadUrl( self, url ):
        log.info( f'Downloading URL {url}' )
        r = requests.get( url )
        if r.status_code == 200:
            log.info( f'Size of downloaded data {len(r.text)}' )
            self.__DATA = r.text
            if isinstance( self.__store_filename, str ):
                with open( self.__store_filename, 'w' ) as stream:
                    stream.write( self.__DATA  )

        else:
            log.error( f'Download error {r.status_code}' )

        return

    def newRecord( self ):
        return M3URecord()

    def __iter__(self):
        """This iterate through the M3U data, and yields ( <type>, <title>, <record> )
        where
            <type>      M3uItemType
            <title>     str
            <record>    dict

        :return:
        """
        # Conversion needed as enswith() only accepts str or tuple
        record = self.newRecord()
        for item in self.__RE_ITEM.findall( self.__DATA ):
            record.clear()
            record.set( item )
            log.debug( f'{record.TypeStr} :: {record}' )
            yield record

        return
