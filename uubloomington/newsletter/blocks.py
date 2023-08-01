from wagtail import blocks


class ArticleBlock(blocks.PageChooserBlock):
    class Meta:
        page_type = 'Article'
        template = 'newsletter/blocks/article.html'


class TableOfContentsBlock(blocks.StaticBlock):
    class Meta:
        template = 'newsletter/blocks/table_of_contents.html'
