import { WalletMultiButton } from '@solana/wallet-adapter-react-ui'
import React from 'react'

function Navbar() {
  return (
    <div className='nav'>
      <div className='logo'>
        Git Bounty
      </div>
      <div className='wallet-info'>
        <WalletMultiButton />
      </div>
    </div>
  )
}

export default Navbar