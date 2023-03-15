from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class PayountBootyArgs(typing.TypedDict):
    branch_name: str


layout = borsh.CStruct("branch_name" / borsh.String)


class PayountBootyAccounts(typing.TypedDict):
    payer: Pubkey
    receiver: Pubkey
    sheriff: Pubkey
    bounty: Pubkey


def payount_booty(
    args: PayountBootyArgs,
    accounts: PayountBootyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["receiver"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["sheriff"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["bounty"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdf;-\xed\xf5\x01<\xfe"
    encoded_args = layout.build(
        {
            "branch_name": args["branch_name"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
