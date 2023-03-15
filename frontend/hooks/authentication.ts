import { useState, useEffect } from "react";
import { useRouter } from 'next/router'
import axios from 'axios';

export const useToken = () => {
  const router = useRouter()

  const getToken = () => {
    let token = null;
    if (typeof window !== 'undefined') {
      token = window.sessionStorage.getItem('token');
    }
    
    if (token) {
      return token
    }
    return null
  };

  const [token, setToken] = useState(getToken());

  const saveToken = (token) => {
    sessionStorage.setItem('token', token);
    setToken(token);
    router.reload()
  };

  return {
    setToken: saveToken,
    token
  }
}

export const useAuthentication = (token) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      axios.get(process.env.NEXT_PUBLIC_BACKEND_URL + 'check-user', {
        headers: {
          'Authorization': `Token ${token}` 
        }
      }).then(response => setUser(response.data.username))
    }
  }, [token])

  return {
    user
  }
}