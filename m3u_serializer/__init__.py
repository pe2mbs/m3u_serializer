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
"""M3U Serializer is special for reading/writing M#U for IPTV.
Currently the directives #EXTM3U and #EXTINF are supported.
Regular Expressions are used to deserialize the M3U data stream.
This is done for speed as IPTV M3U files are quite big.

"""
from m3u_serializer.version import __version__, __author__
from m3u_serializer.reader import M3UDeserializer
from m3u_serializer.record import M3URecord, M3URecordEx, M3uItemType
from m3u_serializer.writer import M3USerializer
