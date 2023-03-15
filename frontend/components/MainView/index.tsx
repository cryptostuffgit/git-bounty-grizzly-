import { useWallet } from '@solana/wallet-adapter-react';
import React, { useEffect, useState } from 'react';
import { useAuthentication } from '../../hooks/authentication';
import OpenBounties from '../OpenBounties';
import CreateBounty from '../CreateBounty';

const MainView = ({user, token}) => {
  const wallet = useWallet();
  return (
    
    <div className="main-container">

      <div className="create-side">
        <CreateBounty token={token} />
      </div>

      <div className="bounty-side">
        <h2>Open Bounties</h2>
        <OpenBounties token={token} />
      </div>

    </div>
  );
};

export default MainView;
