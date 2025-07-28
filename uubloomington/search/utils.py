from wagtail.search.query import MATCH_NONE, Phrase, PlainText, Fuzzy, Not
from wagtail.search.utils import separate_filters_from_query, OR, AND


def fuzzy_parse_query_string(query_string, operator=None, zero_terms=MATCH_NONE):
    """
    This takes a query string typed in by a user and extracts the following:

     - Quoted terms (for phrase search)
     - Filters
     - Individual search terms as Fuzzy search terms

    For example, the following query:

      `hello "this is a phrase" live:true` would be parsed into:

    filters: {'live': 'true'}
    tokens: And([Fuzzy('hello'), Phrase('this is a phrase')])
    """
    filters, query_string = separate_filters_from_query(query_string)

    is_phrase = False
    tokens = []
    if '"' in query_string:
        parts = query_string.split('"')
    else:
        parts = query_string.split("'")

    for part in parts:
        part = part.strip()

        if part:
            if is_phrase:
                tokens.append(Phrase(part))
            # elif part.startswith('!'):
            #     tokens.append(
            #         Not(PlainText(part.strip('!'), operator=operator or PlainText.DEFAULT_OPERATOR))
            #     )
            # TODO: The above doesn't actually work. Revisit it later. Might be useful. Could also just get rid of it.
            else:
                tokens.append(
                    Fuzzy(part, operator=operator or Fuzzy.DEFAULT_OPERATOR)
                )

        is_phrase = not is_phrase

    if tokens:
        if operator == "or":
            search_query = OR(tokens)
        else:
            search_query = AND(tokens)
    else:
        search_query = zero_terms

    return filters, search_query