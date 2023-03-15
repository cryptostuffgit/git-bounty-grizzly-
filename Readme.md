# Git Bounty UPDATED

## A Solana platform for creating and claiming github issue bounties

### About

The inspiration for this project was to create better incentives for developers to contribute to open source projects.

On our platform you link your github and then can link issues by assigning them to a smart contract that is fully collateralized with the bounty amount.
Then developers can come and fork the repository and submit a pull request to the assgined branch for the bounty
Using github webhooks, when the pull request is merged, the developer gets paid the bounty amount

### Running Locally

#### Contract
The contract is deployed to devnet at: https://explorer.solana.com/address/HzAWxmoXNewwrJRwUY39Xjnoh25hAiQBnPgcfKYGbmxi?cluster=devnet

#### Frontend
1. create a `.env.local` under the `frontend` folder
2. setup github oauth and fill out the env variables:
```
NEXT_PUBLIC_NETWORK=devnet
NEXT_PUBLIC_RPC=https://api.devnet.solana.com

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/

NEXT_PUBLIC_GITHUB_OAUTH_CLIENT_ID=
NEXT_PUBLIC_GITHUB_OAUTH_CLIENT_SECRET=
NEXT_PUBLIC_GITHUB_OAUTH_REDIRECT_URI=http://localhost:3000
```
3. run `pnpm install`
4. run `pnpm dev`

#### Backend
1. create a `.env` under the `SolBounty` folder
2. add the following variables:
```
GITHUB_OAUTH_CLIENT_ID=
GITHUB_OAUTH_CLIENT_SECRET=
```
3. run `python3 -m venv env`
4. run `pip install -r requierments.txt`
5. run `python manage.py migrate`
6. run `python manage.py runserver`

Submitted for Grizzlython, Enjoy :)
