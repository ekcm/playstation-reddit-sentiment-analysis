import { Separator } from "@/components/ui/separator"

export const Navbar = () => {
    return (
      <nav>
        <div className="w-3/4 mx-auto">
          <div className="flex justify-center items-center h-16">
            <h1 className="text-2xl font-bold">
                PlayStation x MIT Reddit Sentiment Analysis
            </h1>
          </div>
          <p className="text-center mx-auto">
            This is a small project for the IAP - Sony Interactive Entertainment Comes to MIT: The Nexus of Games and AI Course.
            This project is a proof of concept to show how large language models can be used for sentiment analysis on social media.
            
            Note: data is scraped from the <a href="https://www.reddit.com/r/thelastofus/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 transition-colors">/r/thelastofus</a> subreddit.
          </p>
        </div>
        <Separator className="my-4" />
      </nav>
    );
  };