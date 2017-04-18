from hachoir_core.cmd_line import unicodeFilename
from hachoir_core.error import HachoirError
from hachoir_core.stream import InputIOStream
from hachoir_metadata import config, extractMetadata
from hachoir_parser import guessParser


__all__ = ['MetadataException', 'extract']


class MetadataException(Exception):
    pass


class Metadata(dict):
    def __init__(self, file):
        data = dict([
            (data.key, data.values[0].value)
            for data in self.extract_metadata(file)
            if data.values
        ])
        super(Metadata, self).__init__(data)

    def extract_metadata(self, file):
        config.MAX_STR_LENGTH = float("inf")
        try:
            filename = file.name
            if not isinstance(filename, unicode):
                filename = unicodeFilename(filename)
            stream = InputIOStream(file, source="file:%s" % filename, tags=[], filename=filename)
            parser = guessParser(stream)
            return extractMetadata(parser)
        except (HachoirError, TypeError) as e:
            raise MetadataException(e)


def extract(file):
    return Metadata(file)
