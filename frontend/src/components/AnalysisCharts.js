import React from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#AF19FF",
  "#FF4567",
];
const AnalysisChartsCard = ({ analysisCharts }) => {
  // if (!analysisCharts) {
  //   return null; // Prevent render if result is undefined
  // }
  // const [showChart, setShowChart] = useState(false);
  //
  // const toggleChart = () => {
  //   setShowChart((prev) => !prev);
  // };

  // Transform data for Recharts
  const emotionData = Object.entries(analysisCharts.emotion.percentage).map(
    ([name, value]) => ({ name, value }),
  );

  const topicData = Object.entries(analysisCharts.topic.percentage).map(
    ([name, value]) => ({ name, value }),
  );

  const sentimentData = [
    { name: "Positive", value: analysisCharts.sentiment.positive_percentage },
    {
      name: "Negative",
      value: 100 - analysisCharts.sentiment.positive_percentage,
    },
  ];

  return (
    <div className="charts-container">
      <h2>Aggregate Statistics</h2>
      <div className="chart">
        <h3>Sentiment</h3>
        <PieChart width={300} height={300}>
          <Pie
            data={sentimentData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label
          >
            {sentimentData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      <div className="chart">
        <h3>Emotion</h3>
        <PieChart width={300} height={300}>
          <Pie
            data={emotionData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#82ca9d"
            label
          >
            {emotionData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      <div className="chart">
        <h3>Topic</h3>
        <PieChart width={300} height={300}>
          <Pie
            data={topicData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#FF8042"
            label
          >
            {topicData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>
    </div>
  );
};

export default AnalysisChartsCard;
