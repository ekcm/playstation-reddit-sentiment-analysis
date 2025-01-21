import { Separator } from "@/components/ui/separator"

export const Navbar = () => {
    return (
      <nav>
        <div>
          <div className="flex justify-center items-center h-16">
            <h1 className="text-2xl font-bold">
                PlayStation x MIT Reddit Sentiment Analysis
            </h1>
          </div>
          <p className="text-center">
            This is a small project as part of the MIT course. Note: insights generated are only for the /r/thelastofus subreddit
          </p>
        </div>
        <Separator className="my-4" />
      </nav>
    );
  };