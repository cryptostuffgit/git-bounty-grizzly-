import React, { useEffect, useState } from 'react';
import { useMethods } from '../../hooks/useProgram';

interface ContractProps {
    program: any
    method: any,
    programTypes: any
}

const Method = ({program, method, programTypes}: ContractProps) => {
    const [args, setArgs] = useState({});
    const {
        submitTransaction
      } = useMethods();

    const getArgType = (typeName) => {
        const t = programTypes.find(t => t.name == typeName) || [];
        return t;
    }
    const fields = method?.args.map(a => getArgType(a.type.defined)).map(f => f.type.fields).flat() || [];

    const handleInputArg = (event) => {
        const newArgs = {
            ...args
        }
        newArgs[event.target.placeholder] = event.target.value;
        setArgs(newArgs)
    }

    const handleSubmitTransaction = () => {
        submitTransaction(args, program, method, fields);
    }

    return (
        <div className="method-fiedls">
            <div className="header">Fields</div>
            {
                fields.map(f => {
                    return (
                        <input className="program-address-input" placeholder={f.name} onKeyUp={handleInputArg} />
                    )
                })
            }
            <div  className="header">Accounts</div>
            {
                method.accounts.filter(a => a.name !== "systemProgram").map(a => {
                    return (
                        <input className="program-address-input" placeholder={a.name} onKeyUp={handleInputArg} />
                    )
                })
            }
            <button className="submit-transaction" onClick={handleSubmitTransaction}>Submit Transaction</button>
        </div>
    );
};

export default Method;