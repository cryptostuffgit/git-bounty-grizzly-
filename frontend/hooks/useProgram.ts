import { AnchorProvider, Program } from '@project-serum/anchor';
import { useWallet } from '@solana/wallet-adapter-react';
import { Connection, clusterApiUrl, PublicKey } from '@solana/web3.js';
import * as anchor from '@project-serum/anchor'
import idl from '../booty_contract.json';
import { BootyContract } from '../booty_contract';

type Network = "devnet" | "mainnet-beta";

// Get our program's id from the IDL file.
const programId = new PublicKey(idl.metadata.address);

const useProgram = () => {
  const wallet = useWallet();
  
  const getProvider = () => {
    const connection = new Connection(process.env.NEXT_PUBLIC_RPC, 'processed');
    const provider = new AnchorProvider(
      connection, wallet, {commitment: 'processed'},
    );
    return provider;
  }
  const provider = getProvider();
  const program = new anchor.Program(idl as anchor.Idl, programId, provider) as Program<BootyContract>;
    
  return program;
}

export default useProgram