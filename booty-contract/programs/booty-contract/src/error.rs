use anchor_lang::prelude::*;

#[error_code]
pub enum BootyError {
    #[msg("Sorry, you do not have enough funds to create this bounty!")]
    NotEnoughFunds,
    #[msg("Sorry, you do not have the correct permmissions to payout this bounty!")]
    InvalidPayer,
    #[msg("Please make sure your bounty reward is greater than 0")]
    BountyNotGreaterThanZero,
    #[msg("Please wait for the withdraw period to end")]
    ExpiraryError,
    #[msg("Sorry, this bounty has already been claimed")]
    BountyClaimedError,
}