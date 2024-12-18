"""
Example of a well-known file:

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


Example of a apple-app-site-association file:
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

import dataclasses


@dataclasses.dataclass
class AssetLink:
    relation: list[str]
    target: dict[str, str]


@dataclasses.dataclass
class AASA:
    app_links: list[A]


@dataclasses.dataclass
class AASAAppLink:
    details: list[str]


@dataclasses.dataclass
class AASAAppLink:
    apple_app_site_association: dict[str, str]
    asset_links: list[AssetLink]


from typing import Self

from config import get_logger

from dbcon.queries import update_apps_well_known_store, STORE

from litestar import Controller, get
from litestar.exceptions import HTTPException

logger = get_logger(__name__)


class WellKnownController(Controller):
    """
    Recording for well-known endpoints.

    Endpoints for well-known
    =========
    GET /.well-known/apple-app-site-association
    GET /.well-known/AssetLinks.json
    """

    path = "/.well-known"

    @get(path="apple-app-site-association")
    async def apple_app_site_association(
        self: Self,
    ) -> AASA:
        """
        Return the apple-app-site-association file.
        """
        ios_apps = await STORE.get("ios_apps")
        if len(ios_apps) == 0:
            raise HTTPException(status_code=404, detail="No ios apps found")

        return AASA(
            apple_app_site_association={"status": "success"},
            asset_links=[],
        )

    @get(path="assetlinks.json")
    async def assetlinks_json(
        self: Self,
    ) -> AssetLink:
        """
        Return the assetlinks.json file.
        """
        android_apps = await STORE.get("android_apps")
        if len(android_apps) == 0:
            raise HTTPException(status_code=404, detail="No android apps found")

        asset_links: list[AssetLink] = []
        for package_name in android_apps:
            sha_256_cert_fingerprints = android_apps[package_name][
                "sha256_cert_fingerprints"
            ]
            asset_link = AssetLink(
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
        """
        Update the apps well-known store.
        """
        await update_apps_well_known_store()
