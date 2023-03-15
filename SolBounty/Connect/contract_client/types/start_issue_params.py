from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class StartIssueParamsJSON(typing.TypedDict):
    bounty_price: int
    valid_until: int
    branch_name: str


@dataclass
class StartIssueParams:
    layout: typing.ClassVar = borsh.CStruct(
        "bounty_price" / borsh.U64,
        "valid_until" / borsh.U32,
        "branch_name" / borsh.String,
    )
    bounty_price: int
    valid_until: int
    branch_name: str

    @classmethod
    def from_decoded(cls, obj: Container) -> "StartIssueParams":
        return cls(
            bounty_price=obj.bounty_price,
            valid_until=obj.valid_until,
            branch_name=obj.branch_name,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "bounty_price": self.bounty_price,
            "valid_until": self.valid_until,
            "branch_name": self.branch_name,
        }

    def to_json(self) -> StartIssueParamsJSON:
        return {
            "bounty_price": self.bounty_price,
            "valid_until": self.valid_until,
            "branch_name": self.branch_name,
        }

    @classmethod
    def from_json(cls, obj: StartIssueParamsJSON) -> "StartIssueParams":
        return cls(
            bounty_price=obj["bounty_price"],
            valid_until=obj["valid_until"],
            branch_name=obj["branch_name"],
        )
