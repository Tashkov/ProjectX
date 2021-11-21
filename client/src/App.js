import React, {useState, useEffect} from 'react';
import './App.css';



function App() {
    
    const [data, setData] = useState([]);


    useEffect(() => {
        fetch("/tweets?from=2020-06-01&to=2020-06-30",{
            'methods':'GET',
            headers : {
                'Content-Type':'application/json'
            }
        })
        .then(response => response.json())
        .then(response => setData(response))
        .catch(error => console.log(error))

    },[])

    return (
        <div className="App container m-4">
        <div className="row">
            <div className="text-center">
            <h1>On the thrid try i managed to make this work</h1>
            <h2>Total tweets for a month sorted by day</h2>
            <p>{data.map(tweet => <div>{tweet.date}: Total tweets - {tweet["total_tweets"]}</div>)}</p>
            </div>
        </div>        
        </div>

    );
}
export default App;
