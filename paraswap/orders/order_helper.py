from eip712_structs import make_domain
from web3 import Account, Web3
from web3.types import TxParams

from ..abi.augustus_rfq_abi import AUGUSTUS_RFQ_ABI
from ..config import AUGUSTUS_RFQ
from ..types import Network
from .types import Order, OrderWithSignature


class OrderHelper:

    web3: Web3
    augustus_rfq_address: str

    def __init__(self, network: Network, _web3: Web3) -> None:
        self.augustus_rfq_address = AUGUSTUS_RFQ[network]

        self.web3 = _web3
        self.augustus_rfq_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(self.augustus_rfq_address),
            abi=AUGUSTUS_RFQ_ABI,
        )

        self.domain = make_domain(
            chainId=network,
            name="AUGUSTUS RFQ",
            version=1,
            verifyingContract=self.augustus_rfq_address.lower(),
        )

    def fill_order(self, order: OrderWithSignature, tx_params: TxParams):
        tx = self.augustus_rfq_contract.functions.fillOrder(
            order.order.data_dict(), order.signature
        ).buildTransaction(tx_params)
        return tx

    def cancel_order(self, order_hash: str, tx_params: TxParams):
        tx = self.augustus_rfq_contract.functions.cancelOrder(
            order_hash
        ).buildTransaction(tx_params)
        return tx

    def sign_order(self, account: Account, order: Order) -> OrderWithSignature:
        signable = order.signable_bytes(self.domain)

        hashed = Web3.keccak(signable)
        signed = account.signHash(hashed)

        return OrderWithSignature(order, signed.signature.hex(), signed.messageHash.hex())
