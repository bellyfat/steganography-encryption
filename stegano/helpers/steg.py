from PIL import Image


class SteganoImage(object):
    def __init__(self, imgpath, msg=None):
        super(SteganoImage, self).__init__()
        self.img_path = imgpath
        if msg and len(msg) > 255:
            raise ValueError(
                'Message cannot be longer than 255 characters')
        self.msg_to_hide = msg

    def encode(self, save_path):
        img_to_encode = Image.open(self.img_path)
        if img_to_encode.mode != 'RGB':
            raise TypeError('Image needs to be RGB')
        # use a copy of image to hide the text in
        encoded = img_to_encode.copy()
        width, height = img_to_encode.size
        index = 0
        length = len(self.msg_to_hide)
        for row in range(height):
            for col in range(width):
                r, g, b = img_to_encode.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    character = self.msg_to_hide[index - 1]
                    asc = ord(character)
                else:
                    asc = r
                encoded.putpixel((col, row), (asc, g, b))
                index += 1
        encoded.save(save_path)

    def decode(self):
        img_to_decode = Image.open(self.img_path)
        width, height = img_to_decode.size
        decoded_msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = img_to_decode.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some .png files
                    r, g, b, a = img_to_decode.getpixel((col, row))
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    decoded_msg += chr(r)
                index += 1
        return decoded_msg
