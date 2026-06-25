import React, { useState } from "react";
import axios from "axios";
import "./App.css";

import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const [data, setData] = useState({
    positive: 78,
    neutral: 12,
    negative: 10,
    rating: "4.3 / 5",
    reviews: 1250,
    confidence: "92%",
    recommendation: "Strong Buy",
    summary: "Most users are highly satisfied with the product."
  });

  // 🔥 API CALL
  const analyzeProduct = async () => {
    try {
      setLoading(true);

      // 1️⃣ scrape call
      await axios.post("http://localhost:5000/scrape", {
        url: url
      });

      // 2️⃣ dashboard call
      const res = await axios.get("http://localhost:5000/dashboard");

      setData({
        ...data,
        positive: res.data.positive,
        neutral: res.data.neutral,
        negative: res.data.negative
      });

    } catch (err) {
      console.log(err);
      alert("Backend error 😢");
    } finally {
      setLoading(false);
    }
  };

  // 📊 chart
  const chartData = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        data: [
          data.positive,
          data.neutral,
          data.negative
        ],
        backgroundColor: ["#22C55E", "#F59E0B", "#EF4444"],
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="container">

      <div className="card">

        <h1>🛒 Product Sentiment Analyzer</h1>

        <p className="subtitle">
          Analyze Amazon & Flipkart Reviews using AI
        </p>

        <input
          type="text"
          placeholder="Paste Product URL Here..."
          className="input-box"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={analyzeProduct} disabled={loading} className="analyze-btn">
          {loading ? "Analyzing..." : "🔍 Analyze Product"}
        </button>

      </div>

      <div className="result-card">

        <h2>📊 Analysis Result</h2>

        <div className="stats-container">

          <div className="stat-card">
            <h3>⭐ Rating</h3>
            <p>{data.rating}</p>
          </div>

          <div className="stat-card">
            <h3>📝 Reviews</h3>
            <p>{data.reviews}</p>
          </div>

          <div className="stat-card">
            <h3>🤖 Confidence</h3>
            <p>{data.confidence}</p>
          </div>

        </div>

        <div className="chart-container">
          <div className="chart-box">
            <Pie data={chartData} />
          </div>
        </div>

        <div className="sentiment-box">

          <div className="positive">
            <h3>😊 Positive</h3>
            <p>{data.positive}%</p>
          </div>

          <div className="neutral">
            <h3>😐 Neutral</h3>
            <p>{data.neutral}%</p>
          </div>

          <div className="negative">
            <h3>😔 Negative</h3>
            <p>{data.negative}%</p>
          </div>

        </div>

        <div className="recommendation">
          <h3>💡 Recommendation</h3>
          <p>{data.recommendation}</p>
        </div>

        <div className="summary">
          <h3>📌 Overall Summary</h3>
          <p>{data.summary}</p>
        </div>

      </div>

    </div>
  );
}

export default App;