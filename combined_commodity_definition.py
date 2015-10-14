__author__ = 'taen'


class CombinedCommodityDefinition(object):
    """
        Combined commodity definition. It contains zero or more product family linkage objects.
        It need not contain any if it exists solely to be the target of a scanning-based intercommodity spread.
        Similarly, it may contain zero or more rate adjustment objects, needed in order to scale
        between maintenance and initial and to convert between account types.
        It may contain zero or more tiers of various types.
        It may contain zero or more delta-based spreads. A delta-based spread contained within a combined commodity is by definition an intracommodity spread.
        And it may contain zero or more periods which are in spot, and to which spot charges apply.
        And if it uses liquidation risk it may contain one or more liquidation risk rate objects.

    """

    intra_tiers = None #Intracommodity spread tier definitions
    inter_tiers = None # Intercommodity spread tier definitions
    rate_tiers = None # A container for scan rates. Price scan range and volatility scan range tier definitions. Contains price and volatility scan range rates.
                      # Specifies the price scan range and volatility scan range tiers for a combined commodity, with their associated rates.
    scan_tiers = None  # scanning tier definitions
    intra_delta_spreads = None # spread definitions for intra-commodity tiering.
    som_tiers = None  # short option minimum tier definitions

    risk_exponent = 0
    # cmb_method = None
    som_method = None
    spot_method = None
    wfpr_method = None
    proc_method = None

    product_links = None

    def __init__(self):
        self.product_links = list()