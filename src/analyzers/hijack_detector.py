











def detect_multiple_origin_as(origins):
    """
    Detects if there is more than one origin ASN in a BGP announcement.
    Multiple origin ASNs for the same prefix can indicate a BGP hijack.
    """
    return len(set(origins)) > 1











