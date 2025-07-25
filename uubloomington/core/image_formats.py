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

# TODO: Remove this if we haven't needed it by June 2024
# class EagerLoadingFormat(Format):
#     def image_to_html(self, image, alt_text, extra_attributes={}):
#         extra_attributes['loading'] = "eager"
#         return super().image_to_html(image, alt_text, extra_attributes)
#
#
# register_image_format(
#     EagerLoadingFormat(
#         name='eager_loading_fullwidth',
#         label='Full width - Eager Loading',
#         classname='richtext-image full-width',
#         filter_spec='width-800'
#     )
# )
#
# register_image_format(
#     EagerLoadingFormat(
#         name='eager_loading_right_aligned',
#         label='Right-aligned - Eager Loading',
#         classname='richtext-image right',
#         filter_spec='width-500'
#     )
# )
#
# register_image_format(
#     EagerLoadingFormat(
#         name='eager_loading_left_aligned',
#         label='Left-aligned - Eager Loading',
#         classname='richtext-image left',
#         filter_spec='width-500'
#     )
# )


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