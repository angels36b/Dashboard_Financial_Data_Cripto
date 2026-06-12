import {useState, useEffect} from 'react';

const WhaleFlow = () => {
    const [whales, setWhales] = useState([]);

    useEffect(() => {
        const fetchWhales = async() => {
            try{
                const response = await fetch ('http://127.0.0.1:8000/api/whales');
                const result = await response.json();
                if (result.status === "success"){
                    setWhales(result.data);
                }
            }catch (error){
             console.error("Error conection to Whale API ", error);

            }
        };
        fetchWhales();
        }, []);

    return(
        <div className="whale-feed">
            {whales.map((whale,index) =>{
                //Clasification of the intentional of institut 
             const direction = whale.direction.toLowerCase();
             const isLong = direction ==='long';
             const isShort = direction === 'short';
             const directionClass = isLong ? 'whale-long' : isShort ? 'whale-short' : 'whale-transfer';
            
            return (
                <div key = {index} className = "whale-card">
                    <span className = {`whale-direction ${directionClass}`}>
                        {isLong ? '🟢 LONG' : isShort ? '🔴 SHORT' : '⚪ TRANSFER'}
                    </span>
                    <span className="whale-amount"> {whale.amount} BTC</span>
                    <span className="whale-exchance">@{whale.exchange}</span>
                    <span className="whale-time">{whale.timestamp.split(' ')[1]}</span>
                </div>
            );
            })}
        </div>
    );
};
export default WhaleFlow;