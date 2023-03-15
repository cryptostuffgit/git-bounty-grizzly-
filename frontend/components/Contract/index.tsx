import { AnchorProvider, Program } from '@project-serum/anchor';
import { useWallet } from '@solana/wallet-adapter-react';
import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-nextjs-toast';
import Button from '@mui/material/Button';
import * as anchor from '@project-serum/anchor';
import useProgram from "../../hooks/useProgram";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import Method from '../Method';

interface ContractProps {
    program: Program<anchor.Idl>,
    idl: anchor.Idl
}

const Contract = ({program, idl}: ContractProps) => {
    const [expanded, setExpanded] = React.useState<string | false>(false);

    const handleChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
        setExpanded(isExpanded ? panel : false);
    };

  return (
    <div className="contract-container">
        {idl.instructions.map((method, index) => {
            return(
                <Accordion expanded={expanded === index.toString()} onChange={handleChange(index.toString())}>
                    <AccordionSummary
                        aria-controls="panel1bh-content"
                        id="panel1bh-header"
                    >
                        <Typography sx={{ width: '33%', flexShrink: 0 }}>
                            {method.name}
                        </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            <Method program={program} method={method} programTypes={idl.types}/>
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            )
        })}
    </div>
  );
};

export default Contract;