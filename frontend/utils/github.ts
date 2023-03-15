import axios from 'axios';
import qs from 'qs';

export const getGitHubUrl = () => {
  const rootURl = 'https://github.com/login/oauth/authorize';

  const options = {
    client_id: process.env.NEXT_PUBLIC_GITHUB_OAUTH_CLIENT_ID as string,
    redirect_uri: process.env.NEXT_PUBLIC_GITHUB_OAUTH_REDIRECT_URI as string,
    scope: 'user public_repo admin:repo_hook',
  };

  const qs = new URLSearchParams(options);

  return `${rootURl}?${qs.toString()}`;
}

export const handleGithubCallback = async (code: string) => {
  try {
    const response = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + 'social/github', {
      access_code: code,
    })
    return response
  } catch {
    return {}
  }
}

export const buildGithubIssueUrl = (bounty) => {
  return `https://github.com/${bounty.user}/${bounty.repository}/issues/${bounty.issue_id}`
}