import unittest
import os
from m3u_serializer import M3UDeserializer, M3USerializer, M3URecordEx



class TestSuite( unittest.TestCase ):
    def test_load_filename( self ):
        """This test opens a file and de-serialize the the M3U records

        """
        deserializer = M3UDeserializer( new_record = M3URecordEx )
        deserializer.open( os.path.abspath( os.path.join( 'data', 'test.m3u' ) ) )
        for channel in deserializer:
            self.assertEqual( -1, channel.Duration )
            self.assertEqual( "NPO 1", channel.Name )
            self.assertEqual( "Nederland SD", channel.Group )
            self.assertEqual( "http://iptv.example.org/some/route/channel", channel.Link )

        return

    def test_load_url( self ):
        """This test opens a URL and de-serialize the the M3U records

        """
        deserializer = M3UDeserializer( new_record = M3URecordEx )
        deserializer.open( 'https://github.com/pe2mbs/m3u_serializer/tests/data/test.m3u' )
        for channel in deserializer:
            self.assertEqual( -1, channel.Duration )
            self.assertEqual( "NPO 1", channel.Name )
            self.assertEqual( "Nederland SD", channel.Group )
            self.assertEqual( "http://iptv.example.org/some/route/channel", channel.Link )

        return

    # def test_save_filename( self ):
    #     """This test create a file and serialize a M3U record.
    #
    #     """
    #     serializer = M3USerializer()
    #     serializer.open( os.path.join( 'tests', 'data', 'test-copy.m3u' ) )
    #     rec = M3URecordEx()
    #     rec.set( ( -1, None, 'group-title="Netherlands "', 'NPO 1', 'http://iptv.example.com/some/route/npo1' ) )
    #     serializer.write( rec )
    #     return
    #
