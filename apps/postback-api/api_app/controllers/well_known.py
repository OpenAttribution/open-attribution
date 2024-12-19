"""
Generate well-known files for iOS and Android apps.

Example of Android .well-known/assetlinks.json file:

 https://developer.android.com/training/app-links/verify-android-applinks#multi-host
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.puppies.app",
    "sha256_cert_fingerprints":
    ["14:6D:E9:83:C5:73:06:50:D8:EE:B9:95:2F:34:FC:64:16:A0:83:42:E6:1D:BE:A8:8A:04:96:B2:3F:CF:44:E5"]
  }
  },
  {
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.monkeys.app",
    "sha256_cert_fingerprints":
    ["14:6D:E9:83:C5:73:06:50:D8:EE:B9:95:2F:34:FC:64:16:A0:83:42:E6:1D:BE:A8:8A:04:96:B2:3F:CF:44:E5"]
  }
}]


Example of iOS .well-known/apple-app-site-association file:
 https://developer.apple.com/documentation/xcode/supporting-associated-domains
{
  "applinks": {
      "details": [
           {
             "appIDs": [ "ABCDE12345.com.example.app", "ABCDE12345.com.example.app2" ],
             "components": [
               {
                  "/": "/buy/*",
                  "comment": "Matches any URL with a path that starts with /buy/."
               },
             ]
           }
       ]
   },
   "webcredentials": {
      "apps": [ "ABCDE12345.com.example.app" ]
   },
}
"""

from typing import Self

from config import get_logger
from dbcon.queries import STORE, update_apps_well_known_store
from litestar import Controller, get
from litestar.exceptions import HTTPException

from api_app.models import (
    AppleAASA,
    AppleAppSiteAssociationComponent,
    Applinks,
    Detail,
    GoogleAssetLink,
)

logger = get_logger(__name__)


class WellKnownController(Controller):
    """
    Recording for well-known endpoints.

    Endpoints for well-known
    =========
    GET /.well-known/apple-app-site-association
    GET /.well-known/assetlinks.json
    """

    path = "/.well-known"

    @get(path="apple-app-site-association")
    async def apple_app_site_association(
        self: Self,
    ) -> AppleAASA:
        """
        Return the apple-app-site-association file.

        Note: The url suffix is hardcoded to /oat

        """
        ios_apps = await STORE.get("ios_apps")
        if len(ios_apps) == 0:
            raise HTTPException(status_code=404, detail="No ios apps found")

        for store_id in ios_apps:
            bundle_id = ios_apps[store_id]["bundle_id"]
            team_id = ios_apps[store_id]["apple_team_id"]
            aasa_app_id = f"{team_id}.{bundle_id}"

        aasa_data = AppleAASA(
            applinks=Applinks(
                details=[
                    Detail(
                        team_app_ids=[aasa_app_id],
                        components=[
                            AppleAppSiteAssociationComponent(
                                id="no_universal_links",
                                exclude=True,
                            ),
                            AppleAppSiteAssociationComponent(
                                path="/oat/*",
                                comment="Matches paths under /oat/.",
                            ),
                        ],
                    ),
                ],
            ),
        )
        # aasa_dict = aasa_data.to_dict()

        return aasa_data

    @get(path="assetlinks.json")
    async def assetlinks_json(
        self: Self,
    ) -> list[GoogleAssetLink]:
        """Return the AssetLinks.json file."""
        android_apps = await STORE.get("android_apps")
        if len(android_apps) == 0:
            raise HTTPException(status_code=404, detail="No android apps found")

        asset_links: list[GoogleAssetLink] = []
        for package_name in android_apps:
            sha_256_cert_fingerprints = android_apps[package_name][
                "sha256_cert_fingerprints"
            ]
            asset_link = GoogleAssetLink(
                relation=["delegate_permission/common.handle_all_urls"],
                target={
                    "namespace": "android_app",
                    "package_name": package_name,
                    "sha256_cert_fingerprints": sha_256_cert_fingerprints,
                },
            )
            asset_links.append(asset_link)

        return asset_links

    @get(path="updateapps")
    async def update_apps(
        self: Self,
    ) -> None:
        """Update the apps well-known store."""
        await update_apps_well_known_store()
