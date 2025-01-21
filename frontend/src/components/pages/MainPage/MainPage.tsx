"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";

const MainPage = () => {
  const [loading, setLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState(null);

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
          <div className="bg-white p-4 rounded-md shadow-sm w-full flex-1 flex flex-col items-center justify-center">
            <Button 
              onClick={fetchSentimentData} 
              disabled={loading}
              className="mb-4"
            >
              {loading ? "Loading..." : "Fetch Sentiment Data"}
            </Button>
            {sentimentData && (
              <div className="text-center">
                <pre className="text-left">
                  {JSON.stringify(sentimentData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
