import logging
import bin.settings as settings
from bin.get_json_from_url import get_json_from_url
from decimal import Decimal


# Configure logging
logger = logging.getLogger(__name__)

class TokenInformation():
    """
    Base class to collect TokenInformation from CoinGecko.
    The function needs a contract address to collect the correct information
    """
    def __init__(self,contractaddress):
        logger.info(
            "Collecting token information for contract address: {}".format(
                contractaddress))
        self.contractaddress = contractaddress
        self.fiatsymbol = settings.config.fiatsymbol
        self.json = None
        self.fiatprice = None
        self.tokenname = None
        self.tokensymbol = None

        # Get the content from Coingecko (output in JSON format)
        self.get_content()
        # Extract the most import information from the JSON and store this
        # in the object.
        self.extract_json()

    def get_content(self):
        cgurl = ("https://api.coingecko.com/api/v3/coins/ethereum/contract/"
        "{}").format(self.contractaddress)
        logger.info("The Coingecko transaction URL is: {}".format(
            cgurl))
        try:
            self.json = get_json_from_url(cgurl)
            logger.info("The JSON file is succesfully retrieved")
        except:
            logger.error("Can't retrieve the JSON file from the url")

    def extract_json(self):
        logger.info("Extracting import information from JSON file")
        self.tokenname = self.json['name']
        logger.info("The following token name has been found: {}".format(
            self.tokenname))
        self.tokensymbol = self.json['symbol']
        logger.info("The following token symbol has been found: {}".format(
            self.tokensymbol))
        self.fiatprice = Decimal(
            self.json['market_data']['current_price'][self.fiatsymbol])
        logger.info("The following fiatprice has been found: {} {}".format(
            self.fiatprice,self.fiatsymbol))


