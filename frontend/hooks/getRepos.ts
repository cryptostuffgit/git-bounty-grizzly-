import axios from 'axios';

export const getRepos = async (token: string) => {
  try {
    const response = await axios.get(process.env.NEXT_PUBLIC_BACKEND_URL + 'link-repository', {
      headers: {
        'Authorization': `Token ${token}` 
      }
    })
    return response.data
  } catch {
    return []
  }
}