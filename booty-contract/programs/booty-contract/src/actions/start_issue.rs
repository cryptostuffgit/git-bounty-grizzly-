use crate::*;
use anchor_lang::prelude::*;
use anchor_lang::prelude::Clock;

#[derive(Accounts)]
#[instruction(start_issue_params: StartIssueParams)]
pub struct StartIssue<'info> {
    #[account(
        mut
    )]
    pub payer: Signer<'info>,

    #[account(
        init,
        payer = payer,
        space = Bounty::BOUNTY_SIZE,
        seeds = [b"bounty", start_issue_params.branch_name.as_bytes(), payer.key().as_ref()],
        bump,
    )]
    pub bounty: Account<'info, Bounty>,
    
    pub system_program: Program<'info, System>,    
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct StartIssueParams {
    bounty_price: u64,
    valid_until: u32,
    branch_name: String
}


impl StartIssue<'_> {
    pub fn validate(&self, ctx: &Context<Self>, params: &StartIssueParams) -> Result<()> {
        require!(params.bounty_price > 0, BootyError::BountyNotGreaterThanZero);
        require!(ctx.accounts.payer.lamports() >= params.bounty_price, BootyError::NotEnoughFunds);
        Ok(())
    }

    pub fn actuate(ctx: Context<Self>, params: StartIssueParams) -> Result<()> {
        let bounty = &mut ctx.accounts.bounty;
        let payer = &mut ctx.accounts.payer;
        
        bounty.sheriff = payer.key();
        bounty.time_created = Clock::get().unwrap().unix_timestamp as u32;
        bounty.valid_until = params.valid_until;
        bounty.price = params.bounty_price;
        bounty.is_claimed = false;

        let ix = anchor_lang::solana_program::system_instruction::transfer(
            &payer.key(),
            &bounty.key(),
            params.bounty_price,
        );
        anchor_lang::solana_program::program::invoke(
            &ix,
            &[
                bounty.to_account_info(),
                payer.to_account_info(),
            ],
        )?;

        Ok(())
    }
}