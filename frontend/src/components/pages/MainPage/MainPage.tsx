"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Area, AreaChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";

interface SentimentDataPoint {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
  others: number;
}

interface SentimentResponse {
  timeline: SentimentDataPoint[];
  overall: {
    positive: number;
    negative: number;
    neutral: number;
    others: number;
    total: number;
  };
}

const MainPage = () => {
  const [loading, setLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState<SentimentResponse | null>(null);

  const fetchSentimentData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/sentiment-analysis');
      const data = await response.json();
      setSentimentData(data);
      console.log(data);
    } catch (error) {
      console.error('Error fetching sentiment data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-center items-center min-h-[calc(100vh-8rem)]">
        <div className="flex flex-col items-center gap-8 bg-gray-50 p-8 rounded-lg shadow-sm w-3/4 h-[80vh]">
          <div className="inline-flex rounded-md shadow-sm" role="group">
            <Button variant="outline" className="rounded-r-none">Sentiment Analysis</Button>
            <Button variant="outline" className="rounded-none border-x-0">Keyword Frequency</Button>
            <Button variant="outline" className="rounded-l-none">Top Posts</Button>
          </div>
          <div className="bg-white p-4 rounded-md shadow-sm w-full flex-1 flex flex-col items-center">
            <Button 
              onClick={fetchSentimentData} 
              disabled={loading}
              className="mb-4"
            >
              {loading ? "Loading..." : "Fetch Sentiment Data"}
            </Button>
            {sentimentData && (
              <div className="w-full h-[500px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart
                    data={sentimentData.timeline}
                    margin={{
                      top: 10,
                      right: 30,
                      left: 0,
                      bottom: 0,
                    }}
                  >
                    <XAxis 
                      dataKey="date" 
                      stroke="#888888"
                      fontSize={12}
                    />
                    <YAxis
                      stroke="#888888"
                      fontSize={12}
                    />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="positive"
                      stackId="1"
                      stroke="#4ade80"
                      fill="#4ade80"
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="negative"
                      stackId="1"
                      stroke="#f87171"
                      fill="#f87171"
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="neutral"
                      stackId="1"
                      stroke="#60a5fa"
                      fill="#60a5fa"
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="others"
                      stackId="1"
                      stroke="#a855f7"
                      fill="#a855f7"
                      fillOpacity={0.5}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
