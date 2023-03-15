export const lamportsToSol = (lamports: string) => {
    return (Number(lamports) / 10 ** 9).toFixed(2).toString()
}