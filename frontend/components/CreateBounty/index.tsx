import React, { useEffect, useState } from 'react';
import { getRepos } from '../../hooks/getRepos';
import RepoCard from 'components/RepoCard';

const CreateBounty = ({token}) => {
    const [repos, setRepos] = useState([])
    
    useEffect(() => {
        getRepos(token).then(response => {
            console.log("repos", response)
            setRepos(response)
        }
    )
    },[token])

  return (
    <div className="">
        <h2>My Repositories</h2>
        <div className="repo-container">
          {repos.map(repo => {
              return (
                <RepoCard repo={repo} />
              )
            }) 
          }
        </div>
    </div>
  );
};

export default CreateBounty;