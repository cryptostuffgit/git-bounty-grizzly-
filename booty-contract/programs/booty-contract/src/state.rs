use anchor_lang::prelude::*;

#[account]
pub struct Bounty {
    pub sheriff: Pubkey,
    pub time_created: u32,
    pub valid_until: u32,
    pub price: u64,
    pub is_claimed: bool
}

impl Bounty {
    pub const BOUNTY_SIZE: usize = 8 + 32 + 32 + 4 + 4 + 8 + 1; 
}
