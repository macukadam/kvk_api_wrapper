class APIpaths():
    """API paths for KVK api."""

    # With the Basisprofiel API you can request extensive information from companies from the Trade Register
    basisprofielen = 'basisprofielen'
    # With the Zoeken API you can look up companies in the Trade Register. You can then request the data using another API.
    zoeken = 'zoeken'
    # With the Vestigingsprofiel API you request specific information from companies from the Trade Register.
    vestigingsprofielen = 'vestigingsprofielen'
    # With the Naamgeving API you request name data of companies from the Trade Register.
    naamgevingen = 'naamgevingen/kvknummer'

class BasisProfielPaths():
    """Basic profile paths for KVK api."""

    # Retrieve owner information for a specific company.
    eigenaar = 'eigenaar'
    # Retrieve head office information for a specific company.
    hoodfvestiging = 'hoofdvestiging'
    # Retrieve a list of branches for a specific company.
    vestigingen = 'vestigingen'

