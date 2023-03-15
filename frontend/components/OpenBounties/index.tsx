import { useWallet } from '@solana/wallet-adapter-react';
import React, { useEffect, useState } from 'react';
import { getBounties, startBountyRequest } from '../../hooks/bounties';
import { lamportsToSol } from '../../utils/solana';
import { buildGithubIssueUrl } from '../../utils/github'
import { toast, ToastContainer } from 'react-nextjs-toast';

const OpenBounties = ({token}) => {
  const wallet = useWallet();
  const [bounties, setBounties] = useState([])

  useEffect(() => {
    getBounties(token).then(response => {
      console.log("bounties", response)
      setBounties(response)
    })
  }, [token])

  const startBounty = (bounty) => () => {
    if(!wallet.connected){
      toast.notify("Sorry you must connect a wallet", {
        duration: 5,
        type: "error",
        title: "Error"
      }) 
    } else {
      startBountyRequest(token, bounty, wallet.publicKey)
    }
  }
  

  return (
    <div className="open-bounties-countainer">
      <ToastContainer className={"toast-container"} align={"right"} position={"bottom"} />
      {bounties && bounties.map(bounty => {
        return (
            <tr className="open-bounties-row">
              <td>{bounty.title}</td>
              <td>{bounty.repository}</td>
              <td>{lamportsToSol(bounty.lamports)} SOL</td>
              <td><a href={buildGithubIssueUrl(bounty)} target="_blank">View Issue</a></td>
              <td><a href={"https://explorer.solana.com/address/" + bounty.pda + "?cluster=devnet"} target="_blank">View SolScan</a></td>
              <td><div className='link-payment-address' onClick={startBounty(bounty)}>Apply for Bounty</div><div className='fork-branch'>Fork Repository</div></td>
              
            </tr>
        )
      })}
    </div>
  );
};

export default OpenBounties;
