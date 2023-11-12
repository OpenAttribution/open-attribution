
from config import get_logger

from litestar import Controller, get

logger = get_logger(__name__)

"""
/impressions/
/clicks/
"""



class PostbackController(Controller):
    path = "/impressions"

    @get(path="/{app:str}")
    async def impressions(self, app: str) -> None:
        """
        Handles a GET request for a list of apps

        Args:
            app:app

        Returns:
            A dictionary representation of the list of apps for homepage
        """
        logger.info(f"{self.path} start")
        print(f"app={app}")

        logger.info(f"{self.path} return")
        return

    