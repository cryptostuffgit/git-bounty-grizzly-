import Head from 'next/head';
import styles from '../styles/Home.module.css';
import Login from 'components/Login';

export default function Home() {
  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Login />
    </>
  );
}