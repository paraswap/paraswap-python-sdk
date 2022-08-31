from web3 import Web3
from web3.types import Nonce, TxParams

from .types import OrderWithSignature
from ..config import AUGUSTUS_RFQ
from ..abi.augustus_rfq_abi import AUGUSTUS_RFQ_ABI
from ..types import Network

class OrderOnChainHelper():

    web3: Web3
    augustus_rfq_address: str

    def __init__(self, network: Network, _web3: Web3) -> None:
        self.augustus_rfq_address = AUGUSTUS_RFQ[network]

        self.web3 = _web3
        self.augustus_rfq_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(self.augustus_rfq_address),
            abi=AUGUSTUS_RFQ_ABI,
        )

    def fill_order(self, order: OrderWithSignature, tx_params: TxParams):
        print(order.order.data_dict())

        tx = self.augustus_rfq_contract.functions.fillOrder(order.order.data_dict(), order.signature).transact(tx_params)
        print(tx)
        return tx

    def cancel_order(self, order_hash: str, tx_params: TxParams):
        tx = self.augustus_rfq_contract.functions.cancelOrder(order_hash).buildTransaction(tx_params)
        return tx
