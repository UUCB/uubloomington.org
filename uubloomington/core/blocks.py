from wagtail import blocks


class ReadMoreTagBlock(blocks.StaticBlock):
    class Meta:
        icon = 'arrow-down'
        label = '"Read More" tag'
        admin_text = f'{label}: Anything after this tag will be hidden behind a "Read More" button.'
        template = 'core/read_more_snippet.html'
