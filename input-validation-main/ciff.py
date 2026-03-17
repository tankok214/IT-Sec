import struct


class CIFF:
    """
    Holds data of a CIFF image
    """

    def __init__(
            self,
            magic_chars="CIFF",
            header_size_long=0,
            content_size_long=0,
            width_long=0,
            height_long=0,
            caption_string="",
            tags_list=None,
            pixels_list=None
    ):
        """
        Constructor for CIFF images

        :param magic_chars: the magic "CIFF" characters
        :param header_size_long: size of the header in bytes (8-byte-long int)
        :param content_size_long: size of content in bytes 8-byte-long int)
        :param width_long: width of the image (8-byte-long int)
        :param height_long: height of the image (8-byte-long int)
        :param caption_string: caption of the image (string)
        :param tags_list: list of tags in the image
        :param pixels_list: list of pixels to display
        """
        self._magic = magic_chars
        self._header_size = header_size_long
        self._content_size = content_size_long
        self._width = width_long
        self._height = height_long
        self._caption = caption_string
        if tags_list is None:
            self._tags = []
        else:
            self._tags = tags_list
        if pixels_list is None:
            self._pixels = []
        else:
            self._pixels = pixels_list
        self._is_valid = True

    #
    # Properties
    #

    @property
    def is_valid(self):
        """
        A flag indicating whether the the CIFF image conforms
        with the specification or not

        :return: boolean
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value):
        self._is_valid = value

    @property
    def magic(self):
        """
        The parsed magic characters

        :return: str
        """
        return self._magic

    @magic.setter
    def magic(self, value):
        self._magic = value

    @property
    def header_size(self):
        """
        The parsed header size

        :return: int
        """
        return self._header_size

    @header_size.setter
    def header_size(self, value):
        self._header_size = value

    @property
    def content_size(self):
        """
        The parsed content size

        :return: int
        """
        return self._content_size

    @content_size.setter
    def content_size(self, value):
        self._content_size = value

    @property
    def width(self):
        """
        The parsed width of the image

        :return: int
        """
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """
        The parsed height of the image

        :return: int
        """
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def caption(self):
        """
        The parsed image caption

        :return: str
        """
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def tags(self):
        """
        The parsed list of tags

        :return: list of strings
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def pixels(self):
        """
        The parsed pixels

        :return: list
        """
        return self._pixels

    @pixels.setter
    def pixels(self, value):
        self._pixels = value

    #
    # Static methods
    #

    @staticmethod
    def parse_ciff_file(file_path):
        """
        Parses a CIFF file and constructs the corresponding object

        TODO: make sure that malformed input cannot crash the parsing method

        :param file_path: path the to file to be parsed (string)
        :return: the parsed CIFF object
        """
        new_ciff = CIFF()
        bytes_read = 0
        # the following code can throw Exceptions at multiple lines
        try:
            with open(file_path, "rb") as ciff_file:
                # read the magic bytes
                magic = ciff_file.read(4)
                # read may not return the requested number of bytes
                # magic must contain 4 bytes. If not, raise Exception
                if len(magic) != 4:
                         raise Exception("Invalid magic length: expected 4 bytes")
                bytes_read += 4
                # decode the bytes as 4 characters
                new_ciff.magic = magic.decode('ascii')
                # the magic must be "CIFF". If not, raise Exception
                if new_ciff.magic != "CIFF":
                         raise Exception(f"Invalid magic value: expected 'CIFF', got {new_ciff.magic!r}")

                # read the header size
                h_size = ciff_file.read(8)
                # h_size must contain 8 bytes. If not, raise Exception
                if len(h_size) != 8:
                         raise Exception("Invalid header_size length: expected 8 bytes")
                bytes_read += 8
                # interpret the bytes as an 8-byte-long integer
                # CIFF numeric fields are stored as little-endian unsigned 64-bit integers
                new_ciff.header_size = struct.unpack("<Q", h_size)[0]
                # the header size must be in [38, 2^64 - 1]
                # check the value range. If not in range, raise Exception
                if new_ciff.header_size < 38 \
                       or new_ciff.header_size > 18446744073709551615:
                   raise Exception(f"Invalid header_size value: {new_ciff.header_size} (expected >= 38)")

                # read the content size
                c_size = ciff_file.read(8)
                # c_size must contain 8 bytes. If not, raise Exception
                if len(c_size) != 8:
                    raise Exception("Invalid content_size length: expected 8 bytes")
                bytes_read += 8
                # interpret the bytes as an 8-byte-long integer
                new_ciff.content_size = struct.unpack("<Q", c_size)[0]
                # the content size must be in [0, 2^64 - 1]
                # check the value range. If not in range, raise Exception
                # Question: is this check necessary?
                if new_ciff.content_size < 0 or \
                       new_ciff.content_size > 18446744073709551615:
                   raise Exception(f"Invalid content_size value: {new_ciff.content_size} (expected >= 0)")

                # read the width
                width = ciff_file.read(8)
                # check if width contains 8 bytes
                if len(width) != 8:
                    raise Exception("Invalid width length: expected 8 bytes")
                bytes_read += 8
                # interpret the bytes as an 8-byte-long integer
                new_ciff.width = struct.unpack("<Q", width)[0]
                # the width must be in [0, 2^64 - 1]
                # check the value range. If not in range, raise Exception
                # Question: is this check necessary?
                if new_ciff.width < 0 or new_ciff.width > 18446744073709551615:
                         raise Exception(f"Invalid width value: {new_ciff.width} (expected >= 0)")

                # read the height
                height = ciff_file.read(8)
                # check if height contains 8 bytes
                if len(height) != 8:
                    raise Exception("Invalid height length: expected 8 bytes")
                bytes_read += 8
                # interpret the bytes as an 8-byte-long integer
                new_ciff.height = struct.unpack("<Q", height)[0]
                # the height must be in [0, 2^64 - 1]
                # (the '<Q' unpack already guarantees it's non-negative)
                if new_ciff.height > 18446744073709551615:
                         raise Exception(f"Invalid height value: {new_ciff.height} (expected <= 2^64-1)")

                # content size must equal width*height*3
                if new_ciff.content_size != new_ciff.width * new_ciff.height * 3:
                   raise Exception(
                       f"Invalid content_size mismatch: content_size={new_ciff.content_size}, expected={new_ciff.width * new_ciff.height * 3}"
                   )

                # read the name of the image character by character
                caption = ""
                c = ciff_file.read(1)
                # check if c contains 1 byte
                if len(c) != 1:
                    raise Exception("Invalid caption: missing caption data or newline terminator")
                bytes_read += 1
                char = c.decode('ascii')
                # read until the first '\n' (caption cannot contain '\n')
                while char != '\n':
                    # append read character to caption
                    caption += char
                    # read next character
                    c = ciff_file.read(1)
                    # check if c contains 1 byte
                    if len(c) != 1:
                        raise Exception("Invalid caption: unexpected EOF before newline")
                    bytes_read += 1
                    char = c.decode('ascii')
                new_ciff.caption = caption

                # read all the tags
                tags = list()
                # read until the end of the header
                tag = ""
                while bytes_read < new_ciff.header_size:
                    c = ciff_file.read(1)
                    # check if c contains 1 byte
                    if len(c) != 1:
                        raise Exception("Invalid tags: unexpected EOF while reading tags")
                    bytes_read += 1
                    char = c.decode('ascii')
                    # tags should not contain '\n'
                    # char must not be a '\n'
                    if char == '\n':
                        raise Exception("Invalid tags: newline character found within tags section")
                    # tags are separated by terminating nulls
                    tag += char
                    if char == '\0':
                        tags.append(tag)
                        tag = ""
                    # the very last character in the header must be a '\0'
                    # check the last character of the header
                    if (bytes_read == new_ciff.header_size) and char != '\0':
                       raise Exception("Invalid tags: header does not end with NUL terminator")

                # all tags must end with '\0'
                # check the end of each tag for the '\0'
                for tag in tags:
                   if tag[-1] != '\0':
                       raise Exception(f"Invalid tag terminator: tag {tag!r} does not end with NUL")

                new_ciff.tags = tags

                # read the pixels
                while bytes_read < new_ciff.header_size+new_ciff.content_size:
                    c = ciff_file.read(3)
                    # check if c contains 3 bytes
                    if len(c) != 3:
                        raise Exception("Invalid pixel data: unexpected EOF (RGB triplet incomplete)")
                    bytes_read += 3
                    pixel = struct.unpack("BBB", c)
                    new_ciff.pixels.append(pixel)

                # we should have reached the end of the file
                # try to read a byte. If successful, raise Exception
                extra_byte = ciff_file.read(1)
                if len(extra_byte) != 0:
                    raise Exception("Invalid trailing data: file contains extra bytes after expected end")

        except Exception as e:
            print(f"Error parsing CIFF file: {e}")
            new_ciff.is_valid = False

        return new_ciff
