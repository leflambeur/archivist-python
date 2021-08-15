"""Create an asset given url to Archivist and user Token.

The module contains two functions: main and create_asset. Main function parses in
a url to the Archivist and a token, which is a user authorization.
The main function would initialize an archivist connection using the url and
the token, called "arch", then call arch.assets.create() and the asset will be created.
"""

from archivist.archivist import Archivist
from archivist.storage_integrity import StorageIntegrity


def create_asset(arch):
    """Create an asset using Archivist Connection.

    Args:
        arch: archivist connection.

    Returns:
        newasset: a new asset created.

    """
    attrs = {
        "arc_display_name": "display_name",  # Asset's display name in the user interface
        "arc_description": "display_description",  # Asset's description in the user interface
        "arc_display_type": "desplay_type",  # Arc_display_type is a free text field
        # allowing the creator of
        # an asset to specify the asset
        # type or class. Be careful when setting this:
        # assets are grouped by type and
        # sharing policies can be
        # configured to share assets based on
        # their arc_display_type.
        # So a mistake here can result in asset data being
        # under- or over-shared.
        "some_custom_attribute": "value"  # You can add any custom value as long as
        # it does not start with arc_
    }
    #
    # store asset on the DLT or not. If DLT is not enabled for the user an error will occur if
    # StorageIntegrity.LEDGER is specified. If unspecified then TENANT_STORAGE is used
    # i.e. not stored on the DLT...
    # storage_integrity = StorageIntegrity.TENANT_STORAGE
    props = {
        "storage_integrity": StorageIntegrity.LEDGER,
    }

    # The first argument are the properties of the asset
    # The second argument are the attributes of the asset
    # The third argument is wait for confirmation:
    #   If @confirm@ is True then this function will not
    #   return until the asset is confirmed on the blockchain and ready
    #   to accept events (or an error occurs)
    #
    return arch.assets.create(props, attrs, confirm=True)
    # alternatively if some work can be done whilst the asset is confirmed then this call can be
    # replaced by a two-step alternative:

    # asset = arch.assets.create(props, attrs, confirm=False)

    # ... do something else here
    # and then wait for confirmation

    # self.arch.assets.wait_for_confirmation(asset['identity']))


def main():
    """Main function of create asset.

    Parse in user input of url and auth token and use them to
    create an example archivist connection and create an asset.

    """
    with open(".auth_token", mode="r") as tokenfile:
        authtoken = tokenfile.read().strip()

    # Initialize connection to Archivist. max_time is the time to wait for confirmation
    # of an asset or event creation - the default is 1200 seconds but one can optionally
    # specify a differnet value here particularly when creating assets on TENANT_STORAGE
    # (rather than LEDGER) as confirmation times are much shorter in this case.
    arch = Archivist(
        "https://app.rkvst.io",
        auth=authtoken,
        max_time=300,
    )
    # Create a new asset
    asset = create_asset(arch)
    print("Asset", asset)


if __name__ == "__main__":
    main()
