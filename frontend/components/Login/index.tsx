import React, { useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useRouter } from 'next/router'
import { getGitHubUrl, handleGithubCallback } from '../../utils/github';
import { useToken } from '../../hooks/authentication';

const Login = () => {
  const router = useRouter()

  const { token, setToken } = useToken()

  useEffect(() => {
    console.log(router.query)
    if ('code' in router.query) {
      handleGithubCallback(router.query.code as string)
      .then(response => {
        if ('data' in response) {
          setToken(response.data['token'])
        }
      })
    }
  }, [])

  return (
    <div className="login-container">
        <div className="login-card">
            <div className="login-button" onClick={() => window.location.assign(getGitHubUrl())}>
                Login With Github
            </div>
        </div>
    </div>
  );
};

export default Login;