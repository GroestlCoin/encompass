import unittest

import lib.chainparams as chainparams
import lib.chains
import lib.transaction
from lib.transaction import Transaction, deserialize
import lib.bitcoin
from lib.util_coin import int_to_hex

class TestTransaction(unittest.TestCase):
    def setUp(self):
        super(TestTransaction, self).setUp()
        chainparams.set_active_chain('BTC')
        self.chain = chainparams.get_active_chain()

    def test_deserialize(self):
        chainparams.set_active_chain("BTC")
        # some random tx
        rawtx = '010000000198fb6f1c46eb0416b6a91bc9d0b8dfa554a96b23f00070f430bbf6d05b26ea16010000006c493046022100d00ff7bb2e9d41ef200ceb2fd874468b09a21e549ead6f2a74f35ad02ce25df8022100b1307da37c806ae638502c60d0ebbbe6da2ae9bb03f8798953059269e0ef3b46012102e7d08484e6c4c26bd2a3aabab09c65bbdcb4a6bba0ee5cf7008ef19b9540f818ffffffff0200743ba40b0000001976a91429a158767437cd82ccf4bd3e34ecd16c267fc36388aca0c01319180000001976a9140b31340661bb7a4165736ca2fc6509164b1dc96488ac00000000'
        tx = deserialize(rawtx, chainparams.get_active_chain())
        self.assertEqual(tx['version'], 1)
        # inputs
        self.assertEqual(len(tx['inputs']), 1)
        first_in = tx['inputs'][0]
        self.assertEqual(first_in['is_coinbase'], False)
        self.assertEqual(first_in['prevout_hash'], '16ea265bd0f6bb30f47000f0236ba954a5dfb8d0c91ba9b61604eb461c6ffb98')
        self.assertEqual(first_in['prevout_n'], 1)
        self.assertEqual(first_in['num_sig'], 1)
        self.assertEqual(first_in['pubkeys'], ['02e7d08484e6c4c26bd2a3aabab09c65bbdcb4a6bba0ee5cf7008ef19b9540f818'])
        self.assertEqual(first_in['signatures'], ['3046022100d00ff7bb2e9d41ef200ceb2fd874468b09a21e549ead6f2a74f35ad02ce25df8022100b1307da37c806ae638502c60d0ebbbe6da2ae9bb03f8798953059269e0ef3b46'])
        self.assertEqual(first_in['sequence'], 4294967295)
        # outputs
        self.assertEqual(len(tx['outputs']), 2)
        # output 1
        first_out = tx['outputs'][0]
        self.assertEqual(first_out['address'], '14o7zMMUJkG6De24r3JkJ6USgChq7iWF86')
        self.assertEqual(first_out['prevout_n'], 0)
        self.assertEqual(first_out['scriptPubKey'], '76a91429a158767437cd82ccf4bd3e34ecd16c267fc36388ac')
        self.assertEqual(first_out['type'], 'address')
        self.assertEqual(first_out['value'], 50000000000)
        # output 2
        second_out = tx['outputs'][1]
        self.assertEqual(second_out['address'], '122BNoyhmuUt9G9mdEm3mN4nb73c1UgNKt')
        self.assertEqual(second_out['prevout_n'], 1)
        self.assertEqual(second_out['scriptPubKey'], '76a9140b31340661bb7a4165736ca2fc6509164b1dc96488ac')
        self.assertEqual(second_out['type'], 'address')
        self.assertEqual(second_out['value'], 103499940000)
        # locktime
        self.assertEqual(tx['lockTime'], 0)

    def test_peercoin_deserialize(self):
        chainparams.set_active_chain('PPC')
        rawtx = '0100000058e4615501a367e883a383167e64c84e9c068ba5c091672e434784982f877eede589cb7e53000000006a473044022043b9aee9187effd7e6c7bc444b09162570f17e36b4a9c02cf722126cc0efa3d502200b3ba14c809fa9a6f7f835cbdbbb70f2f43f6b30beaf91eec6b8b5981c80cea50121025edf500f18f9f2b3f175f823fa996fbb2ec52982a9aeb1dc2e388a651054fb0fffffffff0257be0100000000001976a91495efca2c6a6f0e0f0ce9530219b48607a962e77788ac45702000000000001976a914f28abfb465126d6772dcb4403b9e1ad2ea28a03488ac00000000'
        tx = deserialize(rawtx, chainparams.get_active_chain())
        self.assertEqual(tx['version'], 1)
        self.assertEqual(len(tx['inputs']), 1)
        self.assertEqual(len(tx['outputs']), 2)
        self.assertEqual(tx['lockTime'], 0)
        self.assertEqual(tx['timestamp'], 1432478808)

    def test_serialize(self):
        chainparams.set_active_chain('BTC')
        rawtx = '010000000198fb6f1c46eb0416b6a91bc9d0b8dfa554a96b23f00070f430bbf6d05b26ea16010000006c493046022100d00ff7bb2e9d41ef200ceb2fd874468b09a21e549ead6f2a74f35ad02ce25df8022100b1307da37c806ae638502c60d0ebbbe6da2ae9bb03f8798953059269e0ef3b46012102e7d08484e6c4c26bd2a3aabab09c65bbdcb4a6bba0ee5cf7008ef19b9540f818ffffffff0200743ba40b0000001976a91429a158767437cd82ccf4bd3e34ecd16c267fc36388aca0c01319180000001976a9140b31340661bb7a4165736ca2fc6509164b1dc96488ac00000000'
        tx = Transaction.deserialize(rawtx, chainparams.get_active_chain())
        self.assertEqual(str(tx), rawtx)

    def test_peercoin_serialize(self):
        chainparams.set_active_chain('PPC')
        rawtx = '0100000058e4615501a367e883a383167e64c84e9c068ba5c091672e434784982f877eede589cb7e53000000006a473044022043b9aee9187effd7e6c7bc444b09162570f17e36b4a9c02cf722126cc0efa3d502200b3ba14c809fa9a6f7f835cbdbbb70f2f43f6b30beaf91eec6b8b5981c80cea50121025edf500f18f9f2b3f175f823fa996fbb2ec52982a9aeb1dc2e388a651054fb0fffffffff0257be0100000000001976a91495efca2c6a6f0e0f0ce9530219b48607a962e77788ac45702000000000001976a914f28abfb465126d6772dcb4403b9e1ad2ea28a03488ac00000000'
        tx = Transaction.deserialize(rawtx, chainparams.get_active_chain())
        self.assertEqual(tx.serialize()[8:16], rawtx[8:16])
