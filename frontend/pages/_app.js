import '../styles/globals.css';
import { useState, useEffect } from 'react';

// Mock useSession for demo purposes
const useSession = () => {
  return [null, { update: () => {} }]; // [session, updateSession]
};

function MyApp({ Component, pageProps }) {
  const [session, setSession] = useState(null);

  return (
    <>
      <Component {...pageProps} session={session} />
    </>
  );
}

export default MyApp;
