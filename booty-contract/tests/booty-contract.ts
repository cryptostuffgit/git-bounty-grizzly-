import fs from 'mz/fs';

import { BN } from "@project-serum/anchor";
import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { PublicKey } from "@solana/web3.js";
import { BootyContract } from "../target/types/booty_contract";

const LAMPORT_PER_SOL = 1000000000;

const provider = anchor.AnchorProvider.env();

describe("booty-contract", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(provider);
  const program = anchor.workspace.BootyContract as Program<BootyContract>;

  it("Does Stuff", async () => {
    // Add your test here.
    const systemProgram = new PublicKey(
      '11111111111111111111111111111111',
    );

    const owner = await getKeypair('./owner.json')
    await airdrop(owner.publicKey);

    const sherif = anchor.web3.Keypair.generate();
    await airdrop(sherif.publicKey);

    const [issuePubkey, _] = (
      await anchor.web3.PublicKey.findProgramAddress(
        [Buffer.from('bounty'), Buffer.from('branch-cool-feature-12435735'), sherif.publicKey.toBuffer()],
        program.programId,
      )
    );

    console.log("Creating issue");
    const startIssueTx = await program.methods
      .startIssue({
        bountyPrice: new BN(1 * LAMPORT_PER_SOL),
        validUntil: 1710459633,
        branchName: "branch-cool-feature-12435735"
      })
      .accounts({
        payer: sherif.publicKey,
        bounty: issuePubkey,
        systemProgram: systemProgram
      })
      .signers([sherif])
      .rpc()
      .catch(e => console.log(e));

      let bounty = await program.account.bounty.fetch(issuePubkey);
      console.log(JSON.stringify(bounty))

    console.log("Paying Stranger");
   
    const receiver = anchor.web3.Keypair.generate();
    
    console.log(owner.publicKey.toBase58())

    const payountBootyTx = await program.methods
      .payountBooty({
        branchName: "branch-cool-feature-12435735"
      })
      .accounts({
        payer: owner.publicKey,
        receiver: receiver.publicKey,
        sheriff: bounty.sheriff,
        bounty: issuePubkey,
        systemProgram: systemProgram
      })
      .signers([owner])
      .rpc()
      .catch(e => console.log(e));

      const receiver_balance = await provider.connection.getBalance(
        receiver.publicKey,
      );

      console.log(receiver_balance);
      bounty = await program.account.bounty.fetch(issuePubkey);
      console.log(JSON.stringify(bounty))
  });
});

export const getKeypair = async (filepath: string): Promise<anchor.web3.Keypair>  => {
  const secretKeyString = await fs.readFile(filepath, { encoding: 'utf8' });
  const secretKey = Uint8Array.from(JSON.parse(secretKeyString));
  return anchor.web3.Keypair.fromSecretKey(secretKey)
}

const airdrop = async (publicKey: PublicKey) => {
  const signature = await provider.connection.requestAirdrop(publicKey, 2 * LAMPORT_PER_SOL);
  await provider.connection.confirmTransaction(signature);
}
