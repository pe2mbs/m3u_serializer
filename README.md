# Project description 
M3U serializer / deserializer a lightweight to write and read M3U medie files.

# Installing
Install and update using pip:

    $ pip install -U m3u_serializer

# A Simple Example

    #!/usr/bin/env python
    from m3u_serializer import M3UDeserializer    
    from m3u_serializer import M3USerializer

    groups = [ 'Channels UK', 'Channels NL' ]

    m3uReader = M3UDeserializer( 'input.m3u' )
    m3uwriter = M3USerializer( 'output.m3u' )
    for item in m3uReader:
        print( item )
        # do some filtering
        if item.Group in groups:
            m3uwriter.write( item )
        
    # all done

See form aore examples the tests/tests.py

# Links
* Documentation: https://github.com/pe2mbs/m3u_serializer/wiki
* PyPI Releases: https://pypi.org/project/m3u_serializer/
* Source Code: https://github.com/pe2mbs/m3u_serializer/
* Issue Tracker: https://github.com/pe2mbs/m3u_serializer/issues
