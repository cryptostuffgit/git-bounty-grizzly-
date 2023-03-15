import React, { useEffect, useState } from 'react';
import Issue from '../Issue';

const RepoCard = ({repo}) => {
  const [issues, setIssues] = useState(repo.issues)
  const [showIssues, setShowIssues] = useState(false)

  return (
    <div className='repo-card'>
    <div className='repo-head' onClick={() => {setShowIssues(!showIssues)}}>
      {!showIssues && <h4>{repo.name} <span className="arrow">></span></h4>}
      {showIssues && <h4>{repo.name} <span className="arrow">v</span></h4>}
    </div>
    {showIssues &&
        <div className="issues">
          {issues.length == 0 && <>Add an issue on Github</>}
          {issues.map(issue => {
              return (
                <Issue repo={repo.name} data={issue} />
              )
            })
          }
        </div>
    }
  </div>
  )
}

export default RepoCard