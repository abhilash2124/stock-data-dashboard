import { useState, useEffect } from 'react'
import './App.css'
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

function App() {
  const [companies, setCompanies] = useState([]);
  const [selected, setSelected] = useState("");
  const [data, setData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [s1, setS1] = useState("");
  const [s2, setS2] = useState("");
  const [compareData, setCompareData] = useState(null);
  const [gainer, setGainer] = useState(null);
  const [days, setDays] = useState(30);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/companies")
      .then(res => res.json())
      .then(data => setCompanies(data.companies));
  }, []);

  useEffect(() => {
    if (selected) {
      fetchData(selected);
    }
  }, [days]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/top-gainer")
      .then(res => res.json())
      .then(data => setGainer(data));
  }, []);


  const fetchData = (symbol) => {
    console.log("STEP 1");

    setSelected(symbol);

    console.log("STEP 2");

    fetch("http://127.0.0.1:8000/data/" + symbol)
      .then(res => {
        console.log("STEP 3");
        return res.json();
      })
      .then(data => {
        console.log("STEP 4", data);
        // setData(data?.data || []);
        setData(data.data.slice(-days));
      })
      .catch(err => console.error("Error:", err));

    fetch(`http://127.0.0.1:8000/summary/${symbol}`)
      .then(res => res.json())
      .then(data => setSummary(data))
      .catch(err => console.error("Error:", err));
  };

  return (
    <>
      <h1 style={{ textAlign: "center" }}>
        📊 Stock Dashboard
      </h1>
      <div style={{
        padding: "10px",
        margin: "5px",
        borderRadius: "5px",
        background: "#e8f3eaff",
        display: "flex", height: "100vh"
      }}>

        <div style={{ width: "200px", borderRight: "1px solid gray", padding: "10px" }}>
          <h3>Companies</h3>

          {companies.map(c => (
            <button
              key={c}
              onClick={() => fetchData(c)}
              style={{ display: "block", margin: "5px", cursor: "pointer" }}
            >
              {c}
            </button>
          ))}
        </div>

        <div style={{ marginBottom: "10px" }}>
          <select onChange={(e) => setDays(Number(e.target.value))}>
            <option value={30}>30 Days</option>
            <option value={90}>90 Days</option>
          </select>
        </div>

        <div style={{ flex: 1, padding: "20px" }}>
          <h2>{selected}</h2>

          {data.length > 0 ? (
            <div>
              <p>Records: {data.length}</p>

              <Line
                data={{
                  labels: data.map(item => item.date),
                  datasets: [
                    {
                      label: "Close Price",
                      data: data.map(item => item.close),
                      borderColor: "blue",
                      fill: false
                    }
                  ]
                }}
              />
            </div>
          ) : (
            <p>No data loaded</p>
          )}

          {summary && (
            <div style={{ marginTop: "15px" }}>
              <p>52W High: {summary["52w_high"].toFixed(2)}</p>
              <p>52W Low: {summary["52w_low"].toFixed(2)}</p>
              <p>Avg Close: {summary["avg_close"].toFixed(2)}</p>
            </div>
          )}
        </div>


        <div style={{ width: "250px", borderLeft: "1px solid gray", padding: "10px" }}>

          <div style={{ marginTop: "20px" }}>
            <h3>🔥 Top Gainer</h3>
            {gainer && (
              <div>
                <p>{gainer.stock} ({(gainer.return * 100).toFixed(2)}%)</p>
              </div>
            )}
          </div>
          <h3>Compare Stocks</h3>

          <select onChange={(e) => setS1(e.target.value)}>
            <option value="">Stock 1</option>
            {companies.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <br /><br />

          <select onChange={(e) => setS2(e.target.value)}>
            <option value="">Stock 2</option>
            {companies.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <br /><br />


          <button
            onClick={() => {
              fetch(`http://127.0.0.1:8000/compare?symbol1=${s1}&symbol2=${s2}`)
                .then(res => res.json())
                .then(data => setCompareData(data));
            }}
            style={{ cursor: "pointer" }}
            disabled={!s1 || !s2}
          >
            Compare
          </button>

          {compareData && (
            <div style={{ marginTop: "15px" }}>
              <h4>Result</h4>

              <p><b>{compareData.stock1.symbol}</b></p>
              <p>Avg: {compareData.stock1.avg.toFixed(2)}</p>
              <p style={{ color: compareData.stock1.trend === "upward" ? "green" : "red" }}>
                Trend: {compareData.stock1.trend}
              </p>

              <p><b>{compareData.stock2.symbol}</b></p>
              <p>Avg: {compareData.stock2.avg.toFixed(2)}</p>
              <p style={{ color: compareData.stock2.trend === "upward" ? "green" : "red" }}>
                Trend: {compareData.stock2.trend}
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
export default App;
