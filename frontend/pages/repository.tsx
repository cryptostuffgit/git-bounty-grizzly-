import { useWallet } from '@solana/wallet-adapter-react';
import Head from 'next/head';
import MainView from '../components/MainView';
import Navbar from '../components/Navbar';
import styles from '../styles/Home.module.css';
import { useToken, useAuthentication } from '../hooks/authentication';

export default function Home() {
  const { token } = useToken()
  const { user } = useAuthentication(token)

  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {user && <MainView user={user} token={token}/>}
    </>
  );
}
