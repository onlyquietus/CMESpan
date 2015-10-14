__author__ = 'taen'

from collections import namedtuple

def named_tuple_from_headers(tuplename, header_row):
    """ Creates a named tuple from a header row.

    The headers are converted to lower case, and a couple of sub-string substitutions are made
    """
    headers = [header.lower().replace("#","num").replace(" ","_").replace("/","_").replace("[","_").replace("]","_") for header in header_row if header is not None]
    return namedtuple(tuplename, headers)
