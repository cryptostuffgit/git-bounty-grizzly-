import React, { useEffect, useState } from 'react';
import { PublicKey } from '@solana/web3.js';


interface GetAccountProps {
    account: any
    program: any
}

const GetAccount = ({account, program}: GetAccountProps) => {
    const [publicKey, setPublicKey] = useState("");
    const [accountData, setaccountData] = useState(null);

    const handleInputArg = (event) => {
        setPublicKey(event.target.value);
    }

    const accountNameToCamel = (accountName: string) => {
        accountName = accountName.charAt(0).toLowerCase() + accountName.slice(1);
        return accountName;
    }

    const handleSubmitTransaction = () => {
        program.account[accountNameToCamel(account.name)].fetch(new PublicKey(publicKey)).then(setaccountData)
    }

    return (
        <div className="method-fiedls">
            <div className="header">Public Key</div>
            <input className="program-address-input" onKeyUp={handleInputArg} />
            <button className="submit-transaction" onClick={handleSubmitTransaction}>Find Account</button>
            {accountData && Object.keys(accountData).map(key => {
                return <div className='json-key'>{key}: {JSON.stringify(accountData[key])}</div>
            })}
        </div>
    );
};

export default GetAccount;