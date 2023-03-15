import React, { useEffect, useState } from 'react';
import { useMethods } from '../../hooks/useProgram';

interface GetAllProps {
    account: any
    program: any
}

const GetAll = ({account, program}: GetAllProps) => {
    const [accounts, setAccounts] = useState(null);

    const accountNameToCamel = (accountName: string) => {
        accountName = accountName.charAt(0).toLowerCase() + accountName.slice(1);
        return accountName;
    }

    const handleSubmitTransaction = () => {
        program.account[accountNameToCamel(account.name)].all().then(setAccounts)
    }

    useEffect(() => {
        console.log(accounts);
      }, [accounts]);

    return (
        <div className="method-fiedls">
            <button className="submit-transaction" onClick={handleSubmitTransaction}>Get Accounts</button>
            { accounts && accounts.map((account) => {
                return (
                    <>
                        <div>Public Key: {account.publicKey.toBase58()}</div>
                    </>
                )
            })}
        </div>
    );
};

export default GetAll;