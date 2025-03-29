import React from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
const COLORS = [
  "#0088FE", // Light Blue
  "#00C49F", // Teal
  "#FFBB28", // Yellow-Orange
  "#FF8042", // Orange
  "#AF19FF", // Purple
  "#FF4567", // Coral Red
  "#6A5ACD", // Slate Blue
  "#32CD32", // Lime Green
];

// // Utility function to shuffle colors
// const shuffleColors = (colors) => [...colors].sort(() => Math.random() - 0.5);

// Shuffling colors for each dataset
const hateColors = ["#FF4567", "#00C49F"];
const spamColors = ["#AF19FF", "#FF8042"];
//const fakeColors = ["#FFBB28", "#32CD32"];
const sentimentColors = ["#0088FE", "#FF4567"];

const AnalysisChartsCard = ({ analysisCharts }) => {
  // Transform data for Recharts
  const emotionData = Object.entries(analysisCharts.emotion.percentage).map(
    ([name, value]) => ({ name, value }),
  );

  const topicData = Object.entries(analysisCharts.topic.percentage).map(
    ([name, value]) => ({ name, value }),
  );

  const sentimentData = [
    {
      name: "Positive",
      value: Math.round(analysisCharts.sentiment.positive_percentage),
    },
    {
      name: "Negative",
      value: Math.round(100 - analysisCharts.sentiment.positive_percentage),
    },
  ];
  const hateData = [
    { name: "Hate", value: Math.round(analysisCharts.hate_speech.percentage) },
    {
      name: "Not Hate",
      value: Math.round(100 - analysisCharts.hate_speech.percentage),
    },
  ];

  const spamData = [
    { name: "Spam", value: Math.round(analysisCharts.spam.percentage) },
    {
      name: "Not Spam",
      value: Math.round(100 - analysisCharts.spam.percentage),
    },
  ];

  return (
    <div className="charts-container">
      <div className="chart">
        <h3>Hate</h3>
        <PieChart width={400} height={400}>
          <Pie
            data={hateData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={125}
            fill="#8884d8"
            label
          >
            {hateData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={hateColors[index % hateColors.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>
      <div className="chart">
        <h3>Sentiment</h3>
        <PieChart width={400} height={400}>
          <Pie
            data={sentimentData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={125}
            fill="#8884d8"
            label
          >
            {sentimentData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={sentimentColors[index % sentimentColors.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>
      <div className="chart">
        <h3>Spam</h3>
        <PieChart width={400} height={400}>
          <Pie
            data={spamData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={125}
            fill="#8884d8"
            label
          >
            {spamData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={spamColors[index % spamColors.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>
      <div className="chart">
        <h3>Emotion</h3>
        <PieChart width={400} height={400}>
          <Pie
            data={emotionData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={125}
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
        <PieChart width={400} height={400}>
          <Pie
            data={topicData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={125}
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
