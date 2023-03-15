import typing
from anchorpy.error import ProgramError


class NotEnoughFunds(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6000, "Sorry, you do not have enough funds to create this bounty!"
        )

    code = 6000
    name = "NotEnoughFunds"
    msg = "Sorry, you do not have enough funds to create this bounty!"


class InvalidPayer(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6001,
            "Sorry, you do not have the correct permmissions to payout this bounty!",
        )

    code = 6001
    name = "InvalidPayer"
    msg = "Sorry, you do not have the correct permmissions to payout this bounty!"


class BountyNotGreaterThanZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Please make sure your bounty reward is greater than 0")

    code = 6002
    name = "BountyNotGreaterThanZero"
    msg = "Please make sure your bounty reward is greater than 0"


class ExpiraryError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Please wait for the withdraw period to end")

    code = 6003
    name = "ExpiraryError"
    msg = "Please wait for the withdraw period to end"


class BountyClaimedError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Sorry, this bounty has already been claimed")

    code = 6004
    name = "BountyClaimedError"
    msg = "Sorry, this bounty has already been claimed"


CustomError = typing.Union[
    NotEnoughFunds,
    InvalidPayer,
    BountyNotGreaterThanZero,
    ExpiraryError,
    BountyClaimedError,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: NotEnoughFunds(),
    6001: InvalidPayer(),
    6002: BountyNotGreaterThanZero(),
    6003: ExpiraryError(),
    6004: BountyClaimedError(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
