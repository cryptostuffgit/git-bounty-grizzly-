from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from anchorpy import Provider
from .contract_client.instructions import payount_booty
from .contract_client.accounts import Bounty
from solana.rpc.async_api import AsyncClient
from .contract_client.program_id import PROGRAM_ID
from anchorpy import Wallet

async def payout_bounty(receiver: str, issue_pda: str, issue_id: str):
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
        print(res)  # True
        secret_key = open('./owner.json', 'r')
        owner = Keypair.from_json(secret_key.read())

        bounty = Pubkey.from_string(issue_pda)
        bounty_acc = await Bounty.fetch(client, bounty, None, PROGRAM_ID)

        receiver = Pubkey.from_string(receiver)

        ix = payount_booty({
            "branch_name": str(issue_id),
        }, {
            "payer": owner.pubkey(),
            "receiver": receiver,
            "sheriff": bounty_acc.sheriff,
            "bounty": bounty,
        })
        tx = Transaction().add(ix)

        provider = Provider(client, Wallet(owner))

        tx = await provider.send(tx, [owner])
        print(tx)
