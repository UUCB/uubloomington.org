from wagtail.images.formats import Format, register_image_format


class AutoHeightOfParentFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes={}):
        extra_attributes['_'] = "on load or resize from window " \
                                "hide me " \
                                "then tell my parentElement measure end " \
                                "then set my @height to result's height " \
                                "then show me " \
                                "then if my width is greater than result's width / 2 remove .parent-height from me " \
                                "else if i do not match .parent-height add .parent-height to me end "

        return super().image_to_html(image, alt_text, extra_attributes)


register_image_format(
    AutoHeightOfParentFormat(
        'right_height_of_parent',
        'Right-aligned - Height of Parent',
        'richtext-image right parent-height',
        'max-400x400'
    )
)

register_image_format(
    AutoHeightOfParentFormat(
        'left_height_of_parent',
        'Left-aligned - Height of Parent',
        'richtext-image left parent-height',
        'max-400x400'
    )
)