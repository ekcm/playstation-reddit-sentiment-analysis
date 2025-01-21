import { Button } from "@/components/ui/button";

const MainPage = () => {
  return (
    <div>
      <div className="flex justify-center items-center min-h-[calc(100vh-8rem)]">
        <div className="flex flex-col items-center gap-8 bg-gray-50 p-8 rounded-lg shadow-sm w-3/4 h-[80vh]">
          <div className="inline-flex rounded-md shadow-sm" role="group">
            <Button variant="outline" className="rounded-r-none">Sentiment Analysis</Button>
            <Button variant="outline" className="rounded-none border-x-0">Keyword Frequency</Button>
            <Button variant="outline" className="rounded-l-none">Top Posts</Button>
          </div>
          <div className="bg-white p-4 rounded-md shadow-sm w-full flex-1">
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
