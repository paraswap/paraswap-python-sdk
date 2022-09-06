from random import randint

from web3 import Web3
from web3.types import TxParams

from .abi.erc20_abi import ERC20_ABI
from .exceptions import BadRequest, InternalError, NotFound


def random_uint(limit: int) -> int:
    return randint(0, limit)


ERRORS_STATUS_CODE = {
    400: BadRequest,
    404: NotFound,
    500: InternalError,
}


def handle_requests_errors(response):
    if response.status_code in ERRORS_STATUS_CODE:
        raise ERRORS_STATUS_CODE[response.status_code](response.text)


class Erc20Helper:

    web3: Web3

    def __init__(self, _web3: Web3, token: str) -> None:
        self.web3 = _web3
        self.contract = self.web3.eth.contract(
            address=Web3.toChecksumAddress(token), abi=ERC20_ABI
        )

    def allowance(self, address: str, spender: str) -> int:
        approval = self.contract.functions.allowance(address, spender).call()

        return approval

    def approve(self, spender: str, amount: int, tx_params: TxParams):
        tx = self.contract.functions.approve(
            spender,
            amount,
        ).buildTransaction(tx_params)

        return tx
