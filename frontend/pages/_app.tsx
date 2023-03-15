import '../styles/globals.css'
import '../styles/Main.scss'
import React from 'react';
import Head from 'next/head';
import CssBaseline from '@material-ui/core/CssBaseline'
import dynamic from 'next/dynamic'
import Navbar from '../components/Navbar';
import { useToken, useAuthentication } from '../hooks/authentication';
import { useRouter } from 'next/router'
import { ToastContainer } from 'react-nextjs-toast'

require('@solana/wallet-adapter-react-ui/styles.css');

export default function MyApp({ Component, pageProps }) {
  const router = useRouter()
  const { token, setToken } = useToken()
  const { user } = useAuthentication(token)

  const WalletConnectProvider = dynamic(
    () => import('../context/WalletConnectionProvider'),
    { ssr: false }
  );
  React.useEffect(() => {
    // Remove the server-side injected CSS.
    const jssStyles = document.querySelector('#jss-server-side');
    if (jssStyles) {
      jssStyles.parentElement.removeChild(jssStyles);
    }
  }, []);
 
  React.useEffect(() => {
    if (user) {
      router.push('/repository')
    }
  }, [user])

  return (
    <React.Fragment>
      <Head>
        <title>Ultimate Solana - A Frontend For All Solana Smart Contracts</title>
        <meta name="title" content="Ultimate Solana - A Frontend For All Solana Smart Contracts" />
        <meta name="description" content="Ultimate Racing - A Frontend For All Solana Smart Contracts" />
        <meta name="keywords" content="solana, anchor, ultimate, frontend, dapp" />
        <meta name="robots" content="index,follow" />
        <meta httpEquiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="language" content="English" />
        <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width" />
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com"/>
        <link href="https://fonts.googleapis.com/css2?family=Golos+Text&family=Golos+Text:wght@500&display=swap" rel="stylesheet"/>
      </Head>
      {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
      <CssBaseline />
      
      <WalletConnectProvider>
        <Navbar />
        <Component {...pageProps} />
        <ToastContainer />
      </WalletConnectProvider>

    </React.Fragment>
  );
}

