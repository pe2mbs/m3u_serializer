import unittest
import os
from m3u_serializer import M3UDeserializer, M3USerializer, M3URecordEx
from server import FlaskStub
import warnings

ROOT_PATH = os.path.abspath( os.path.join( os.path.dirname( __file__ ) ) )
DATA_PATH = os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'data' ) )


class TestSuite( unittest.TestCase ):
    """This unittest class contains only happy flow tests

    """
    @classmethod
    def setUpClass( cls ):
        warnings.filterwarnings( action = "ignore", message = "unclosed", category = ResourceWarning )
        cls.stub = FlaskStub()
        cls.stub.start()
        return

    def setUp(self) -> None:
        self.subTest()
        print( f"\nTest case: {self.id()}" )
        if self._testMethodDoc is not None:
            print( f"Description: {self.shortDescription()}" )

        return

    def test_load_filename( self ):
        """This test opens a file and de-serialize the the M3U records

        """
        deserializer = M3UDeserializer( new_record = M3URecordEx )
        deserializer.open( os.path.join( DATA_PATH, 'input-data.m3u' ) )
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
        deserializer.open( os.path.join( ROOT_PATH, 'data', 'input-invalid-format.m3u' ) )
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
        url = 'http://scuzzy:5000/m3u'
        url = 'http://localhost:5000'
        with M3UDeserializer( url, new_record = M3URecordEx ) as deserializer:
            for channel in deserializer:
                print( f'Read: {channel}' )
                self.assertIn( channel.Duration, ( '-1', '1.45' ) )
                self.assertIn( channel.Name, ( "NPO 1", "NPO 2" ) )
                self.assertEqual( "Nederland SD", channel.Group )
                self.assertIn( channel.Link, ( "http://iptv.example.org/some/route/channel",
                                               'http://iptv.example.org/some/route/channel2' ) )

        return

    def test_save_filename( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer( os.path.join( ROOT_PATH, 'data', 'test-copy.m3u' ) ) as stream:
            channel = M3URecordEx()
            channel.set( -1, 'group-title="Nederland SD"', 'NPO 1', 'http://iptv.example.org/some/route/channel' )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_save_filename_without_attr( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer( os.path.join( ROOT_PATH, 'data', 'test-wo-attr.m3u' ) ) as stream:
            channel = M3URecordEx()
            channel.set( -1, 'NPO 1', 'http://iptv.example.org/some/route/channel' )
            print( f'Writing: {channel}' )
            stream.write( channel )

        return

    def test_save_filename_with_kw_attr( self ):
        """This test create a file and serialize a M3U record.

        """
        with M3USerializer( os.path.join( ROOT_PATH, 'data', 'test-with-attr.m3u' ) ) as stream:
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
        with M3USerializer( os.path.join( ROOT_PATH, 'data', 'test-with-attr-ex.m3u' ) ) as stream:
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
        with M3USerializer( os.path.join( DATA_PATH, 'test-copy-output.m3u' ) ) as out_stream:
            with M3UDeserializer( os.path.join( DATA_PATH, 'input-data.m3u' ) ) as in_stream:
                for channel in in_stream:
                    # do some filtering
                    if channel.Group in groups:
                        print( f'Copy {channel}' )
                        out_stream.write( channel )
