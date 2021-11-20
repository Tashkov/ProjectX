import React, {useState, useEffect} from 'react';

function App(props) {
    
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/tweets?from=2020-05-01&to=2020-05-30").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )    
    }, [])

    return (
        <div>
            
            {(typeof data.tweets === 'undefined') ? (
                <p>Loading...</p>
            ): ( 
                data.tweets.map((member, i) => (
                    <p key={i}>{member}</p>
                ))
            )}


        </div>
    );
}

export default App;
