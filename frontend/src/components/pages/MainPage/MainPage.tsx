"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";

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

interface KeywordResponse {
  sentiment: string;
  keywords: Array<{
    keyword: string;
    frequency: number;
  }>;
  total_keywords: number;
}

type Tab = 'sentiment' | 'keywords' | 'posts';
type KeywordSentiment = 'all' | 'positive' | 'negative' | 'neutral';

const MainPage = () => {
  const [loading, setLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState<SentimentResponse | null>(null);
  const [keywordData, setKeywordData] = useState<KeywordResponse | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('sentiment');
  const [selectedSentiment, setSelectedSentiment] = useState<KeywordSentiment>('all');

  const fetchSentimentData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/sentiment-analysis');
      const data = await response.json();
      setSentimentData(data);
    } catch (error) {
      console.error('Error fetching sentiment data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchKeywordData = async () => {
    try {
      setLoading(true);
      const url = selectedSentiment === 'all' 
        ? 'http://localhost:8000/keywords'
        : `http://localhost:8000/keywords?sentiment=${selectedSentiment}`;
      const response = await fetch(url);
      const data = await response.json();
      setKeywordData(data);
    } catch (error) {
      console.error('Error fetching keyword data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Define consistent colors for both charts
  const chartColors = {
    positive: "#4ade80",
    negative: "#f87171",
    neutral: "#60a5fa",
    others: "#a855f7",
    default: "#60a5fa" // Using neutral blue as default
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'sentiment':
        return (
          <>
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
                      stroke={chartColors.positive}
                      fill={chartColors.positive}
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="negative"
                      stackId="1"
                      stroke={chartColors.negative}
                      fill={chartColors.negative}
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="neutral"
                      stackId="1"
                      stroke={chartColors.neutral}
                      fill={chartColors.neutral}
                      fillOpacity={0.5}
                    />
                    <Area
                      type="monotone"
                      dataKey="others"
                      stackId="1"
                      stroke={chartColors.others}
                      fill={chartColors.others}
                      fillOpacity={0.5}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            )}
          </>
        );
      case 'keywords':
        return (
          <>
            <div className="w-full grid grid-cols-3 items-center mb-4">
              <div /> {/* Empty div for spacing */}
              <div className="flex justify-center">
                <Button 
                  onClick={fetchKeywordData} 
                  disabled={loading}
                >
                  {loading ? "Loading..." : "Fetch Keyword Data"}
                </Button>
              </div>
              <div className="flex justify-end">
                <div className="inline-flex rounded-md shadow-sm" role="group">
                  <Button 
                    variant={selectedSentiment === 'all' ? 'default' : 'outline'} 
                    className="rounded-r-none"
                    onClick={() => {
                      setSelectedSentiment('all');
                      setKeywordData(null);
                    }}
                  >
                    All
                  </Button>
                  <Button 
                    variant={selectedSentiment === 'positive' ? 'default' : 'outline'} 
                    className="rounded-none border-x-0"
                    onClick={() => {
                      setSelectedSentiment('positive');
                      setKeywordData(null);
                    }}
                  >
                    Positive
                  </Button>
                  <Button 
                    variant={selectedSentiment === 'negative' ? 'default' : 'outline'} 
                    className="rounded-l-none"
                    onClick={() => {
                      setSelectedSentiment('negative');
                      setKeywordData(null);
                    }}
                  >
                    Negative
                  </Button>
                </div>
              </div>
            </div>
            {keywordData && (
              <div className="w-full h-[600px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={keywordData.keywords.slice(0, 20)}
                    margin={{
                      top: 20,
                      right: 30,
                      left: 150,
                      bottom: 20,
                    }}
                    layout="vertical"
                    barSize={15}
                    barGap={0}
                  >
                    <XAxis 
                      type="number"
                      stroke="#888888"
                      fontSize={12}
                    />
                    <YAxis
                      type="category"
                      dataKey="keyword"
                      stroke="#888888"
                      fontSize={11}
                      width={140}
                      tickMargin={5}
                      interval={0}
                    />
                    <Tooltip />
                    <Bar
                      dataKey="frequency"
                      fill={chartColors[selectedSentiment === 'all' ? 'default' : selectedSentiment]}
                      radius={[0, 4, 4, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div>
      <div className="flex justify-center items-center min-h-[calc(100vh-8rem)]">
        <div className="flex flex-col items-center gap-8 bg-gray-50 p-8 rounded-lg shadow-sm w-3/4 h-[80vh]">
          <div className="inline-flex rounded-md shadow-sm" role="group">
            <Button 
              variant={activeTab === 'sentiment' ? 'default' : 'outline'} 
              className="rounded-r-none"
              onClick={() => setActiveTab('sentiment')}
            >
              Sentiment Analysis
            </Button>
            <Button 
              variant={activeTab === 'keywords' ? 'default' : 'outline'} 
              className="rounded-none border-x-0"
              onClick={() => setActiveTab('keywords')}
            >
              Keyword Frequency
            </Button>
            <Button 
              variant={activeTab === 'posts' ? 'default' : 'outline'} 
              className="rounded-l-none"
              onClick={() => setActiveTab('posts')}
            >
              Top Posts
            </Button>
          </div>
          <div className="bg-white p-4 rounded-md shadow-sm w-full flex-1 flex flex-col items-center">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
