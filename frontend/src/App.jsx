import { useState } from "react";

function App() {

  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const summarizeVideo = async () => {

    if (!url) {
      alert("Please enter YouTube URL");
      return;
    }

    setLoading(true);
    setSummary("");

    try {

      const response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (data.summary) {
        setSummary(data.summary);
      } else {
        setSummary(data.error);
      }

    } catch (error) {

      setSummary("Something went wrong.");
      console.error(error);

    }

    setLoading(false);
  };

  return (

    <div className="min-h-screen bg-black text-white overflow-hidden relative">

      {/* Background Glow */}
      <div className="absolute top-[-200px] left-[-200px] w-[500px] h-[500px] bg-blue-600 rounded-full blur-[180px] opacity-20"></div>

      <div className="absolute bottom-[-200px] right-[-200px] w-[500px] h-[500px] bg-purple-600 rounded-full blur-[180px] opacity-20"></div>

      {/* Main Container */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-12">

        {/* Hero */}
        <div className="text-center max-w-4xl">

          <div className="inline-flex items-center gap-2 bg-slate-900 border border-slate-700 rounded-full px-5 py-2 mb-8">

            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>

            <span className="text-sm text-slate-300">
              AI Powered Video Intelligence
            </span>

          </div>

          <h1 className="text-7xl md:text-8xl font-black leading-tight mb-8">

            Summarize
            <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              {" "}YouTube Videos
            </span>

          </h1>

          <p className="text-slate-400 text-xl leading-9 max-w-2xl mx-auto mb-14">

            Instantly transform long YouTube videos into concise AI-generated summaries,
            key insights, and actionable takeaways.

          </p>

        </div>

        {/* Input Card */}
        <div className="w-full max-w-5xl bg-white/5 backdrop-blur-xl border border-white/10 rounded-[32px] shadow-2xl p-8">

          <div className="flex flex-col lg:flex-row gap-5">

            <input
              type="text"
              placeholder="Paste YouTube URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 bg-slate-900/80 border border-slate-700 rounded-2xl px-6 py-5 text-lg outline-none focus:border-blue-500 transition-all"
            />

            <button
              onClick={summarizeVideo}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:scale-105 transition-all duration-300 px-10 py-5 rounded-2xl text-lg font-bold shadow-xl"
            >
              Summarize
            </button>

          </div>

          {/* Loading */}
          {loading && (

            <div className="flex flex-col items-center justify-center py-16">

              <div className="relative">

                <div className="w-20 h-20 border-4 border-blue-500/30 rounded-full"></div>

                <div className="w-20 h-20 border-4 border-t-blue-500 rounded-full animate-spin absolute top-0 left-0"></div>

              </div>

              <p className="mt-8 text-slate-400 text-lg">
                AI is analyzing the video...
              </p>

            </div>

          )}

          {/* Summary */}
          {summary && (

            <div className="mt-10 bg-slate-900/70 border border-slate-700 rounded-3xl p-8">

              <div className="flex items-center justify-between mb-8">

                <h2 className="text-3xl font-bold">
                  AI Summary
                </h2>

                <button
                  onClick={() => navigator.clipboard.writeText(summary)}
                  className="bg-slate-800 hover:bg-slate-700 transition px-5 py-3 rounded-xl"
                >
                  Copy
                </button>

              </div>

              <div className="text-slate-300 leading-9 whitespace-pre-wrap text-lg">
                {summary}
              </div>

            </div>

          )}

        </div>

      </div>

    </div>

  );
}

export default App;