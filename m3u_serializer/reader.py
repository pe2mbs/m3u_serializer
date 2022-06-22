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
from typing import Union, Optional
import re
import requests
import logging
import _io
from m3u_serializer.record import M3URecord
from m3u_serializer.exceptions import *
from contextlib import contextmanager

log = logging.getLogger( 'M3U-Deserializer' )


class M3UDeserializer( object ):
    """M3U deserializer for IPTV streams

    This deserializer uses Regular Expressions to get the streams from the M3U file. Both file and web address is supported.

    The Regular Expression gets duration, attributes, title and stream address from the data.
    Optional the data stream can be saved to a separate filename for later use, specially for http/https.

    By default the follewing extensions are are used to detect series and movies.
          .mp4, .avi, .mkv and .flv
    additional extensions maybe supplied via the 'media_files' parameter.

    the M3uRecord can be overriden for your own extra functionality, via the parameter 'new_record'

    Using the class iterator the records can be retrieved from the data stream.

    Only the directives #EXTM3U or #EXTINF are supported.

    """
    # __RE_ITEM         = re.compile( r"(?:^|\n)#EXTINF:([\w+.])([^,]+)?,([A-Z].*?)[\r\n]+(.*)" )
    __RE_ITEM         = re.compile( r"(?:^|\n)#EXTINF:([-+]?(?:\d*\.\d+|\d+))[. ]([^,]+)?,([A-Z].*?)[\r\n]+(.*)" )

    def __init__( self,
                  url_filename: Optional[str] = None,
                  store_filename: Optional[str] = None,
                  media_files: Union[list,tuple,None] = None,
                  new_record = M3URecord ):
        """The constructor of the deserializer

        :param url_filename:    maybe filename or webaddress, when supplied the stream is directly loaded.
        :param store_filename:  optional filename to store the data in a file. specially when using web address.
        :param media_files:     list/tuple with additional extensions for recognizing movies and series.
        :param new_record:      optional for overriding the default M3URecord class.

        """
        self.__DATA             = None
        self.__media_files      = [ '.mp4', '.avi', '.mkv', '.flv' ]
        self.__store_filename   = store_filename
        self.__new_record       = new_record
        if isinstance( media_files, ( list, tuple ) ):
            for item in media_files:
                if item not in self.__media_files:
                    self.__media_files.append( item )

        self.__url_filename = url_filename
        return

    def set( self, data: Union[str,_io.TextIOWrapper] ) -> None:
        """Sets external data to the data stream

        :ptype data:            str
        :param data:            M3U data string
        :return:                None
        """
        if isinstance( data, str ):
            self.__DATA             = data

        elif isinstance( data, _io.TextIOWrapper ):
            self.__DATA             = data.read()

        else:
            raise InvalidParameter( 'M3UDeserializer.set( data ) data must be str or stream' )

        return

    def open( self, url_filename:Optional[str] = None ) -> None:
        """Opens the url or filename and loads the data to internal memory

        :param url_filename:    maybe filename or webaddress, when supplied the stream is directly loaded.
        :return:                None
        """
        if self.__DATA is not None:
            raise AlreadyOpened()

        if isinstance( url_filename, str ):
            self.__url_filename = url_filename

        if self.__url_filename is None:
            raise MissingFilenameUrl()

        if self.__url_filename.startswith( ( 'http://', 'https://' ) ):
            self.__download_url( self.__url_filename )

        elif self.__url_filename.startswith( 'file://' ):
            self.__open_file( self.__url_filename[ 7: ] )

        else:
            self.__open_file( self.__url_filename )

        return

    def close( self ) -> None:
        """Deletes the allocted data.

        :return:                None
        """
        self.__DATA             = None
        self.__url_filename     = None
        return

    def __open_file( self, filename: str ) -> None:
        """Opens the `filename` and loads the data into memory.

        :param filename:        filename to be loaded into memory.
        :return:                None
        """
        log.info( f'Loading FILE {filename}' )
        with open( filename, 'r' ) as stream:
            self.__DATA = stream.read()

        log.info( f'Size of loaded data {len(self.__DATA)}' )
        return

    def __download_url( self, url ) -> None:
        """Opens the `url` and loads the data into memory.

        :param url:             URL to be loaded into memory.
        :return:                None
        """
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
            raise DownloadError( r.status_code )

        return

    def __iter__( self ):
        """This iterate through the M3U data, and yields `M3URecord` class

        :return:                None
        """
        # Conversion needed as endswith() only accepts str or tuple
        if not isinstance( self.__DATA, str ) or self.__DATA == '':
            raise NoDataAvailable()

        channelNumber = 1
        for item in self.__RE_ITEM.findall( self.__DATA ):
            record = self.__new_record( media_files = self.__media_files )
            record.set( *item, channel = channelNumber )
            log.debug( f'{record.Group} :: {record}' )
            yield record
            channelNumber += 1

        return

    def __enter__( self ):
        try:
            self.open( self.__url_filename )

        except:
            raise

        return self

    def __exit__( self, exc_type, exc_value, exc_traceback ):
        self.__DATA = ''
        return
