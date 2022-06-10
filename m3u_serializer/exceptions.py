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

class MissingFilenameUrl( Exception ):
    pass


class DownloadError( Exception ):
    def __init__( self, status_code ):
        super( DownloadError, self ).__init__( f'Download error {status_code}' )
        return


class AlreadyOpened( Exception ):
    pass


class NotOpened( Exception ):
    pass


class MissingFilename( Exception ):
    pass


class NoDataAvailable( Exception ):
    pass


class InvalidParameter( Exception ):
    pass

