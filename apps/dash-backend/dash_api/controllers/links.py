"""API for returning analytics data for dash."""

from typing import Self

import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from dash_api.models import AppLinks, LinkData

logger = get_logger(__name__)


class LinkController(Controller):
    """Controll all ad apps."""

    path = "/api/links"

    @get(path="/")
    async def links(self: Self) -> AppLinks:
        """
        Handle GET request for a list of links.

        Returns
        -------
            Data for a list of links

        """
        logger.info(f"{self.path} links load")
        df = dbcon.queries.query_app_links()
        links_dict = df.to_dict(orient="records")
        myresp = AppLinks(links=links_dict)
        logger.info(f"{self.path} return {links_dict=}")
        return myresp

    @post(path="/{domain_id:int}")
    async def add_link(
        self: Self,
        domain_id: int,
        data: LinkData,
    ) -> None:
        """
        Handle POST request for a new share link.

        Request body should contain:
        {
            "google_app_id": int | null,
            "apple_app_id": int | null,
            "share_slug": string,
            "network_id": int,
            "campaign_name": string,
            "ad_name": string | null,
            "web_landing_page": string
        }

        """
        logger.info(f"{self.path} links load")
        dbcon.queries.insert_app_link(
            domain_id=domain_id,
            share_slug=data.share_slug,
            network_id=data.network_id,
            campaign_name=data.campaign_name,
            google_app_id=data.google_app_id,
            apple_app_id=data.apple_app_id,
            ad_name=data.ad_name,
            web_landing_page=data.web_landing_page,
        )

    @delete(path="/{link_id:int}")
    async def delete_link(self: Self, link_id: int) -> None:
        """Handle DELETE request for a link."""
        logger.info(f"{self.path} DELETE link {link_id=}")
        dbcon.queries.delete_app_link(link_id=link_id)

    @get(path="/domains")
    async def domains(self: Self) -> AppLinks:
        """
        Handle GET request for a list of domains.

        Returns
        -------
            Data for a list of domains

        """
        logger.info(f"{self.path} domains load")
        df = dbcon.queries.query_client_domains()
        domains_dict = df.to_dict(orient="records")
        myresp = AppLinks(links=domains_dict)
        logger.info(f"{self.path} return {domains_dict=}")
        return myresp

    @post(path="/domains/{domain_url:str}")
    async def add_domain(self: Self, domain_url: str) -> None:
        """Add a domain to the database."""
        logger.info(f"{self.path} add domain {domain_url=}")
        domain_url = domain_url.replace("https://", "")
        domain_url = domain_url.replace("http://", "")
        domain_url = domain_url.replace("www.", "")
        domain_url = domain_url.removesuffix("/")
        dbcon.queries.insert_client_domains(domain_url=domain_url)

    @delete(path="/domains/{domain_id:int}")
    async def delete_domain(self: Self, domain_id: int) -> None:
        """Delete a domain from the database."""
        logger.info(f"{self.path} DELETE domain {domain_id=}")
        dbcon.queries.delete_client_domain(domain_id=domain_id)
