import React, { useEffect, useState } from 'react';
import { useMethods } from '../../hooks/useMethods';
import CircularProgress from '@mui/material/CircularProgress';
import { toast } from 'react-nextjs-toast';
import { useWallet } from '@solana/wallet-adapter-react';

const Issue = ({repo, data}) => {
  const [sol, setSol] = useState(0)
  const [transactionPending, setTransactionPending] = useState(false);
  const { startIssue } = useMethods()
  const wallet = useWallet();

  const handleClick = () => {
    if (sol > 0) {
      try {
        setTransactionPending(true)
        startIssue(sol, data, repo)
      } finally {
        setTransactionPending(false)
      }
    } else {
      toast.notify('Sol must be greater than zero.', {
        duration: 5,
        type: "error",
        title: "Sol Less Than Zero"
      })
    }
  }

  return (
    <div className='issue' >
      <h2>{data.title}</h2>
      {!data.pda && 
        <div className="Create-Bounty">
          <input placeholder={"Enter SOL Bounty"} onKeyUp={(e) => setSol(e.target.value)}/>
          {
            !wallet.connected && <>Connect Your Wallet</>
          }
          {
            wallet.connected && <>
              <button onClick={handleClick}>
                {
                  transactionPending ? <CircularProgress color="inherit" /> : <>Create Bounty</>
                }
              </button>
            </>
          }
        </div>
      }  
      <hr></hr>
    </div>
  )
}

export default Issue