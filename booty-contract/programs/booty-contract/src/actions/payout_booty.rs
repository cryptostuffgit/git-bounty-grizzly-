use crate::*;
use anchor_lang::prelude::*;

#[derive(Accounts)]
#[instruction(branch_name: String)]
pub struct PayoutBooty<'info> {
    #[account(
        mut,
        constraint = payer.key() == owner::ID
    )]
    pub payer: Signer<'info>,

    #[account(mut)]
    pub receiver: SystemAccount<'info>,

    pub sheriff: SystemAccount<'info>,

    #[account(
        mut,
        seeds=[b"bounty", branch_name.as_bytes(), sheriff.key().as_ref()],
        bump
    )]
    pub bounty: Account<'info, Bounty>,

    pub system_program: Program<'info, System>,
}

impl PayoutBooty<'_>{
    pub fn validate(&self, ctx: &Context<Self>) -> Result<()>{
        require!(!ctx.accounts.bounty.is_claimed, BootyError::BountyClaimedError);
        Ok(())
    }

    pub fn actuate(ctx: Context<Self>) -> Result<()>{
        let bounty = &mut ctx.accounts.bounty;
        let receiver = &mut ctx.accounts.receiver;

        bounty.is_claimed = true;
        
        let bounty_info = bounty.to_account_info();
    
        let mut receiver_lamports = receiver.lamports.borrow_mut();
        let mut bounty_lamports = bounty_info.lamports.borrow_mut();

        **bounty_lamports -= bounty.price;
        **receiver_lamports += bounty.price;

        Ok(())
    }
}