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
import logging
from typing import Optional
from m3u_serializer.record import M3URecord
from m3u_serializer.exceptions import MissingFilename, NotOpened, AlreadyOpened
from contextlib import contextmanager

log = logging.getLogger( 'M3U-Serializer' )


class M3USerializer( object ):
    """M3U serializer for IPTV streams

    This class writes the M3U file from the M3URecord class

    """
    def __init__( self, filename: Optional[str] = None ):
        """Contructor sets optional the filename for writing.

        :param filename:    optional output filename
        """
        self.__stream = None
        self.__filename = filename
        return

    def create( self, filename: Optional[str] = None ) -> None:
        """Opens the output file when the filename is passed to the function it shall use the supplied filename.

        when neither the filename in the constructor or this member function, an exception MissingFilename is raised

        :param filename:    optional output filename
        :return:            None
        """
        if isinstance( filename, str ):
            self.__filename = filename

        if not isinstance( self.__filename, str ):
            raise MissingFilename()

        log.info( f'Opening FILE {self.__filename}' )
        self.__stream = open( self.__filename, 'w' )
        # Write header of M3U file
        self.__stream.write( '#EXTM3U\n' )
        return

    def close( self ) -> None:
        """Closes the current stream when the stream is not open a NotOpened exception is raised.

        :return:        None
        """
        if self.__stream is None:
            raise NotOpened()

        self.__stream.close()
        self.__stream = None
        log.info( f'Closing FILE {self.__filename}' )
        self.__filename = None
        return

    def write( self, record: M3URecord ) -> None:
        """Writes the record to the M3U file

        :param record:      M3URecord or inherited class
        :return:            None
        """
        attrs_str = record.getAttributes()
        self.__stream.write( f'#EXTINF:{record.Duration} {attrs_str},{record.Name}\n{record.Link}\n' )
        log.debug( f'Writing::\n#EXTINF:{record.Duration} {attrs_str},{record.Name}\n{record.Link}' )
        return


    def __enter__( self ):
        self.create()
        return self

    def __exit__( self, exc_type, exc_value, exc_traceback ):
        self.close()
        return
