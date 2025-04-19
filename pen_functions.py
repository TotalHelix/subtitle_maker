from PIL import Image, ImageDraw, ImageFont
jp_font = ImageFont.truetype("BIZ-UDGothicR.ttc", 60)
en_font = ImageFont.truetype("arial.ttf", 50)
furigana = ImageFont.truetype("BIZ-UDGothicR.ttc", 30)
frame = (1920, 1080)


def _int(thing_to_int):
    try:
        return int(thing_to_int)
    except ValueError:
        return thing_to_int


def from_bottom(y):
    """takes the y position from the bottom of the canvas and returns the position from the top
    (example: 20 pixels from the bottom is 1900 pixels from the top)"""
    return frame[1]-y


def center_start(text, font=jp_font):
    """returns where the left edge of text would be if it is centered on the canvas"""
    text_width = font.getlength(text)
    return frame[0]/2 - text_width/2


class TextWriter:
    def __init__(self):
        # make the canvas and pen
        self.canvas = Image.new("RGBA", frame, color=(0, 0, 0, 0))
        self.pen = ImageDraw.Draw(self.canvas)

        # cursor control
        self.cursor_x = 0
        self.cursor_y = 0

    def set_pos(self, position):
        """set the cursor position. Accepts "center" instead of a coordinate
        update: why would you want to set to center, you would just type to the right"""
        if (not isinstance(position, tuple)) or (len(position) != 2):
            raise TypeError(f"set_pos requires a tuple position of length 2, instead received {str(type(position))}.")

        if not (
                (isinstance(_int(position[0]), int) or position[0] == "center") and
                (isinstance(_int(position[1]), int) or position[1] == "center")
        ):
            raise TypeError(f"one of the positions set is invalid. got: {position}")

        self.cursor_x = frame[0]/2 if position[0] == "center" else position[0]
        self.cursor_y = frame[1]/2 if position[1] == "center" else position[1]

    def scrawl(self, text, color, font=en_font, stroke=True):
        """write the text and move the cursor to where the text ends"""
        print(f"writing {text} with font {font.getname()[0]}")

        self.pen.text(
            (self.cursor_x, self.cursor_y),     # position
            text, fill=color, font=font,        # text
            stroke_width=5 if stroke else 0, stroke_fill=(0, 0, 0, 255)  # stroke
        )

        text_length = font.getlength(text)
        self.cursor_x += text_length

    def furigana_scrawl(self, jp_text, reading, color, stroke=True):
        """scrawl text and add furigana above it"""
        for i, char in enumerate(jp_text):
            # if char is kana
            if char in "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン":
                self.scrawl(char, color, stroke=stroke, font=jp_font)
            # if we reach a kanji
            else:
                # write the furigana
                self.pen.text(
                    (self.cursor_x, self.cursor_y-40),         # position
                    reading, fill=color, font=furigana,     # text
                    stroke_width=5 if stroke else 0, stroke_fill=(0, 0, 0, 255)  # stroke
                )
                self.scrawl(jp_text[i:], color, stroke=stroke, font=jp_font)
                break
