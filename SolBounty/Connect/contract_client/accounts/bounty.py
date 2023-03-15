import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class BountyJSON(typing.TypedDict):
    sheriff: str
    time_created: int
    valid_until: int
    price: int
    is_claimed: bool


@dataclass
class Bounty:
    discriminator: typing.ClassVar = b"\xed\x10i\xc6\x13E\xf2\xea"
    layout: typing.ClassVar = borsh.CStruct(
        "sheriff" / BorshPubkey,
        "time_created" / borsh.U32,
        "valid_until" / borsh.U32,
        "price" / borsh.U64,
        "is_claimed" / borsh.Bool,
    )
    sheriff: Pubkey
    time_created: int
    valid_until: int
    price: int
    is_claimed: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Bounty"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["Bounty"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Bounty"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Bounty":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Bounty.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            sheriff=dec.sheriff,
            time_created=dec.time_created,
            valid_until=dec.valid_until,
            price=dec.price,
            is_claimed=dec.is_claimed,
        )

    def to_json(self) -> BountyJSON:
        return {
            "sheriff": str(self.sheriff),
            "time_created": self.time_created,
            "valid_until": self.valid_until,
            "price": self.price,
            "is_claimed": self.is_claimed,
        }

    @classmethod
    def from_json(cls, obj: BountyJSON) -> "Bounty":
        return cls(
            sheriff=Pubkey.from_string(obj["sheriff"]),
            time_created=obj["time_created"],
            valid_until=obj["valid_until"],
            price=obj["price"],
            is_claimed=obj["is_claimed"],
        )
