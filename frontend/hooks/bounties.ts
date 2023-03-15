import axios from 'axios';
import { toast } from 'react-nextjs-toast';

export const getBounties = async (token: string) => {
  try {
    const response = await axios.get(process.env.NEXT_PUBLIC_BACKEND_URL + 'get-bounties', {
      headers: {
        'Authorization': `Token ${token}` 
      }
    })
    return response.data
  } catch {
    return []
  }
}

export const startBountyRequest = async (token: string, bounty, wallet) => {
  try {
    const response = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + 'apply-issue', 
    {
      github_issue_id: bounty.issue_id,
      wallet: wallet.toBase58()
    },
    {
      headers: {
        'Authorization': `Token ${token}` 
      }
    })
    console.log(response.data)
    toast.notify(`You have succesfully applied as: ${wallet.toBase58()}`, {
      duration: 5,
      type: "success",
      title: "Successfully Applied"
    }) 
    return response.data
    
  } catch {
    return []
  }
}