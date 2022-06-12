import unittest
import os
from m3u_serializer import M3UDeserializer, M3USerializer, M3URecordEx


class TestSuite( unittest.TestCase ):
    def setUp(self) -> None:
        print( f"\nTest case: {self._testMethodName}" )
        if self._testMethodDoc is not None:
            print( f"Description: {self._testMethodDoc}" )

        return

    def test_load_filename( self ):
        """This test opens a file and de-serialize the the M3U records

        """
        deserializer = M3UDeserializer( new_record = M3URecordEx )
        deserializer.readFrom( os.path.abspath( os.path.join( 'data', 'input-data.m3u' ) ) )
        for channel in deserializer:
            print( f'Read: {channel}' )
            self.assertIn( channel.Duration, ( '-1', '1.45' ) )
            self.assertIn( channel.Name, ( "NPO 1", "NPO 2" ) )
            self.assertEqual( "Nederland SD", channel.Group )
            self.assertIn( channel.Link, ( "http://iptv.example.org/some/route/channel",
                                           'http://iptv.example.org/some/route/channel2' ) )

        return

    def test_load_filename_invalid_format( self ):
        """This test when a file is missing the directive #EXTM3U

        """
        deserializer = M3UDeserializer( new_record = M3URecordEx )
        deserializer.readFrom( os.path.abspath( os.path.join( 'data', 'input-invalid-format.m3u' ) ) )
        for channel in deserializer:
            print( f'Read: {channel}' )
            self.assertEqual( '-1', channel.Duration )
            self.assertEqual( "NPO 1", channel.Name )
            self.assertEqual( "Nederland SD", channel.Group )
            self.assertEqual( "http://iptv.example.org/some/route/channel", channel.Link )

        return

    def test_load_url( self ):
        """This test opens a URL and de-serialize the the M3U records

        """
        url = 'https://raw.githubusercontent.com/pe2mbs/m3u_serializer/main/tests/data/test.m3u'
        with M3UDeserializer( new_record = M3URecordEx ).open( url ) as deserializer:
            for channel in deserializer:
                print( f'Read: {channel}' )
                self.assertEqual( '-1', channel.Duration )
                self.assertEqual( "NPO 1", channel.Name )
                self.assertEqual( "Nederland SD", channel.Group )
                self.assertEqual( "http://iptv.example.org/some/route/channel", channel.Link )

        return

    def test_save_filename( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer().create( os.path.abspath( os.path.join( 'data', 'test-copy.m3u' ) ) ) as stream:
            channel = M3URecordEx()
            channel.set( -1, 'group-title="Nederland SD"', 'NPO 1', 'http://iptv.example.org/some/route/channel' )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_save_filename_without_attr( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer().create( os.path.abspath( os.path.join( 'data', 'test-wo-attr.m3u' ) ) ) as stream:
            channel = M3URecordEx()
            channel.set( -1, 'NPO 1', 'http://iptv.example.org/some/route/channel' )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_save_filename_with_kw_attr( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer().create( os.path.abspath( os.path.join( 'data', 'test-with-attr.m3u' ) ) ) as stream:
            channel = M3URecordEx()
            attrs = {
                'tgv-id': 'www.npo1.nl',
                'tgv-name': 'NPO 1 HD',
                'tgv-logo': 'www.npo1.nl',
                'group-title': 'Nederland SD'
            }
            channel.set( -1, 'NPO 1', 'http://iptv.example.org/some/route/channel', **attrs )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_save_filename_with_kw_attr_ex( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer().create( os.path.abspath( os.path.join( 'data', 'test-with-attr-ex.m3u' ) ) ) as stream:
            channel = M3URecordEx()
            attrs = {
                'tgv-id': 'www.npo1.nl',
                'tgv-name': 'NPO 1 HD',
                'tgv-logo': 'www.npo1.nl',
                'group-title': 'Nederland SD',
                'tgv-subtitles': 'https://www.npo1.nl/subtitle',
                'program-name': 'Zomer gasten',
            }
            channel.set( -1, 'NPO 1', 'http://iptv.example.org/some/route/channel', **attrs )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_copy( self ):
        """Copy M3U records based on group-title

        """
        groups = [ 'Nederland SD' ]
        m3uReader = M3UDeserializer( os.path.abspath( os.path.join( 'data', 'input-data.m3u' ) ) )
        m3uwriter = M3USerializer( os.path.abspath( os.path.join( 'data', 'test-copy-output.m3u' ) ) )
        with m3uwriter.create() as out_stream:
            for channel in m3uReader:
                # do some filtering
                if channel.Group in groups:
                    print( f'Copy {channel}' )
                    out_stream.write( channel )
