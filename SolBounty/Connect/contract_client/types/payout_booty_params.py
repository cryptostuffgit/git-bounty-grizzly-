from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class PayoutBootyParamsJSON(typing.TypedDict):
    branch_name: str


@dataclass
class PayoutBootyParams:
    layout: typing.ClassVar = borsh.CStruct("branch_name" / borsh.String)
    branch_name: str

    @classmethod
    def from_decoded(cls, obj: Container) -> "PayoutBootyParams":
        return cls(branch_name=obj.branch_name)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"branch_name": self.branch_name}

    def to_json(self) -> PayoutBootyParamsJSON:
        return {"branch_name": self.branch_name}

    @classmethod
    def from_json(cls, obj: PayoutBootyParamsJSON) -> "PayoutBootyParams":
        return cls(branch_name=obj["branch_name"])
