pub mod actions;
pub mod error;
pub mod state;
pub use actions::*;
use {
    crate::{error::*, state::*},
};
use anchor_lang::prelude::*;

declare_id!("HzAWxmoXNewwrJRwUY39Xjnoh25hAiQBnPgcfKYGbmxi");

pub mod owner {
    super::declare_id!("2XWVTvB3TBNUo29Xxwfcix2XSy22jEknqY9P8s3WXsHA");
}

#[program]
pub mod booty_contract {
    use super::*;
    
    #[access_control(ctx.accounts.validate(&ctx, &params))]
    pub fn start_issue(ctx: Context<StartIssue>, params: StartIssueParams) -> Result<()> {
        StartIssue::actuate(ctx, params)
    }

    #[access_control(ctx.accounts.validate(&ctx))]
    pub fn payount_booty(ctx: Context<PayoutBooty>, branch_name: String) -> Result<()> {
        PayoutBooty::actuate(ctx)
    }
}

