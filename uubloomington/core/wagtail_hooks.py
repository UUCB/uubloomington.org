import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail import hooks


@hooks.register('register_rich_text_features')
def register_centered_text_feature(features):
    feature_name = 'centered'
    type_ = 'centered'

    control = {
        'type': type_,
        'label': '?',
        'icon': '',
        'description': 'Centered Text',
        'element': 'p',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['centered.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=centered]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'p', 'props': {'class': 'centered'}}}},
    })

@hooks.register('register_rich_text_features')
def register_right_aligned_text_feature(features):
    feature_name = 'right-aligned'
    type_ = 'right-aligned'

    control = {
        'type': type_,
        'label': '?',
        'icon': '',
        'description': 'Right-Aligned Text',
        'element': 'p',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['right-aligned.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=right-aligned]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'p', 'props': {'class': 'right-aligned'}}}},
    })