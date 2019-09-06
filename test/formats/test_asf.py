from test.picardtestcase import (
    PicardTestCase,
    create_fake_png,
)

from picard.formats import (
    asf,
    ext_to_format,
)

from .common import (
    CommonTests,
    load_metadata,
    load_raw,
    save_metadata,
    save_raw,
    skipUnlessTestfile,
)
from .coverart import CommonCoverArtTests


# prevent unittest to run tests in those classes
class CommonAsfTests:

    class AsfTestCase(CommonTests.TagFormatsTestCase):

        def test_supports_tag(self):
            fmt = ext_to_format(self.testfile_ext[1:])
            self.assertTrue(fmt.supports_tag('copyright'))
            self.assertTrue(fmt.supports_tag('compilation'))
            self.assertTrue(fmt.supports_tag('bpm'))
            self.assertTrue(fmt.supports_tag('djmixer'))
            self.assertTrue(fmt.supports_tag('discnumber'))
            self.assertTrue(fmt.supports_tag('lyrics:lead'))
            self.assertTrue(fmt.supports_tag('~length'))
            for tag in self.replaygain_tags.keys():
                self.assertTrue(fmt.supports_tag(tag))

        @skipUnlessTestfile
        def test_ci_tags_preserve_case(self):
            # Ensure values are not duplicated on repeated save and are saved
            # case preserving.
            tags = {
                'Replaygain_Album_Peak': '-6.48 dB'
            }
            save_raw(self.filename, tags)
            loaded_metadata = load_metadata(self.filename)
            loaded_metadata['replaygain_album_peak'] = '1.0'
            save_metadata(self.filename, loaded_metadata)
            raw_metadata = load_raw(self.filename)
            self.assertIn('Replaygain_Album_Peak', raw_metadata)
            self.assertEqual(raw_metadata['Replaygain_Album_Peak'][0], loaded_metadata['replaygain_album_peak'])
            self.assertEqual(1, len(raw_metadata['Replaygain_Album_Peak']))
            self.assertNotIn('REPLAYGAIN_ALBUM_PEAK', raw_metadata)


class ASFTest(CommonAsfTests.AsfTestCase):
    testfile = 'test.asf'
    supports_ratings = True
    expected_info = {
        'length': 92,
        '~channels': '2',
        '~sample_rate': '44100',
        '~bitrate': '128.0',
    }


class WMATest(CommonAsfTests.AsfTestCase):
    testfile = 'test.wma'
    supports_ratings = True
    expected_info = {
        'length': 139,
        '~channels': '2',
        '~sample_rate': '44100',
        '~bitrate': '64.0',
    }


class AsfUtilTest(PicardTestCase):
    def test_pack_and_unpack_image(self):
        mime = 'image/png'
        image_data = create_fake_png(b'x')
        image_type = 4
        description = 'testing'
        tag_data = asf.pack_image(mime, image_data, image_type, description)
        expected_length = 5 + 2 * len(mime) + 2 + 2 * len(description) + 2 + len(image_data)
        self.assertEqual(tag_data[0], image_type)
        self.assertEqual(len(tag_data), expected_length)
        self.assertEqual(image_data, tag_data[-len(image_data):])

        unpacked = asf.unpack_image(tag_data)
        self.assertEqual(mime, unpacked[0])
        self.assertEqual(image_data, unpacked[1])
        self.assertEqual(image_type, unpacked[2])
        self.assertEqual(description, unpacked[3])


class AsfCoverArtTest(CommonCoverArtTests.CoverArtTestCase):
    testfile = 'test.asf'


class WmaCoverArtTest(CommonCoverArtTests.CoverArtTestCase):
    testfile = 'test.wma'