from pen_functions import *
import re

def extract(text):
    """extract text in parentheses"""
    # Find all matches and remove them from the original text
    removed_text = re.findall(r'\(.*?\)', text)
    cleaned_text = re.sub(r'\(.*?\)', '', text)

    reading = removed_text[0].replace("(", "").replace(")", "") if removed_text else ""

    # Return the cleaned text and the removed text
    return cleaned_text, reading


def make_subtitle(jp_text, en_text, output_location, color_palette=None):
    """
    makes the subtitle out of jp and en text.
    :arg jp_text: each section should be split up by pipes (|), with furigana after kanji. example: 皆(みな)さん|どうも
    :arg en_text: like jp text, sections should be split by pipes, but each section should start with its position in
                  the Japanese sentence. For example, the above JP would be (2)Hello|(1)everyone!
    :arg output_location: the file to save the output as
    :arg color_palette: the colors that are cycled through to color code words. should be a list of tuples: (r, g, b, a)
    """

    # default colors
    if not color_palette:
        color_palette = [
            (255, 227, 253, 255), (177, 152, 245, 255), (158, 215, 255, 255), (203, 242, 213, 255),
            (255, 251, 194, 255), (255, 177, 158, 255), (255, 94, 136, 255), (255, 255, 255, 255)
        ]

    cursor = TextWriter()
    clean_jp = re.sub(r"\(.*?\)", "", jp_text).replace("|", "")
    cursor.set_pos((center_start(clean_jp, font=jp_font), from_bottom(160)))

    # write japanese text
    for i, section in enumerate(jp_text.split("|")):
        clean_jp, reading = extract(section)

        cursor.furigana_scrawl(clean_jp, reading, color_palette[i])

    clean_en = re.sub(r"\(.*?\)", "", en_text).replace("|", "")
    cursor.set_pos((center_start(clean_en, font=en_font), from_bottom(80)))

    # write english text
    for section in en_text.split("|"):
        # add a space to the end
        section = section + " "

        # extract the index
        clean_en, i = extract(section)

        cursor.scrawl(clean_en, color_palette[int(i)-1])

    cursor.canvas.save(output_location)
    # cursor.canvas.save(save_location+datetime.today().strftime("%m-%d-%y %H_%M.png"))
    # cursor.canvas.show()


# if running just the subtitle maker without the gui, here's some sample input
if __name__ == "__main__":
    make_subtitle(
        "皆(みな)さん|どうもこんばんは", "(2)Good morning|(1)everyone!",  # jp and en text
    )
