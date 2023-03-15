import useProgram from './useProgram';
import { useWallet } from '@solana/wallet-adapter-react';
import { toast } from 'react-nextjs-toast';
import { BN } from "@project-serum/anchor";
import * as anchor from '@project-serum/anchor';
import axios from 'axios';
import { useToken } from '../hooks/authentication';

const LAMPORT_PER_SOL = 1000000000;

const systemProgram = new anchor.web3.PublicKey(
  '11111111111111111111111111111111',
)

export const createIssue = async (bountyPrice, issueData, repoName, pda, token) => {
  console.log(token)
  const response = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + 'create-issue', {
    repository: repoName,
    issue_number: issueData.github_issue_number,
    lamports: (new BN(bountyPrice * LAMPORT_PER_SOL)).toString(),
    pda: pda,
  }, {
    headers: {
      'Authorization': `Token ${token}` 
    }
  })

  console.log(response)
}

export const useMethods = () => {
  const program = useProgram();
  const wallet = useWallet();
  const {token} = useToken();

  const startIssue = async (bountyPrice: number, issueData: any, repoName: string) => {
    
    const date = new Date();
    date.setFullYear(date.getFullYear() + 1);
    const validUntil = Math.floor(date.getTime() / 1000)
    const branchName = issueData.github_issue_id.toString()

    const [bountyPubkey, _] = (
      await anchor.web3.PublicKey.findProgramAddress(
        [Buffer.from('bounty'), Buffer.from(branchName), wallet.publicKey.toBuffer()],
        program.programId,
      )
    );
    
    await program.methods
      .startIssue({
        bountyPrice: new BN(bountyPrice * LAMPORT_PER_SOL),
        validUntil: validUntil,
        branchName: branchName
      })
      .accounts({
        payer: wallet.publicKey,
        bounty: bountyPubkey,
        systemProgram: systemProgram
      })
      .rpc()
      .then((tx) => {
        createIssue(bountyPrice, issueData, repoName, bountyPubkey.toBase58(), token)
        console.log(tx);
        // API request here
        toast.notify('Succesfully Created Bounty.', {
          duration: 5,
          type: "success",
          title: "Succesfully Created Issue"
        })
      })
      .catch(e => {
        console.log(e);
        if (e.error) {
          toast.notify(e.error.errorMessage, {
            duration: 5,
            type: "error",
            title: e.error.errorCode.code.replace(/([A-Z])/g, ' $1').trim()
          })
        } else if (e.logs[3].includes("insufficient lamports")) {
          toast.notify('Insufficient SOL to create this bounty.', {
            duration: 5,
            type: "error",
            title: "Insufficient Funds"
          })
        }
      })
  }

  return {
    startIssue
  }
}
