"use client";

import { useState } from "react";

export default function Home() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdText, setJdText] = useState("");
  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!resumeFile) {
      setError("Please upload a resume file.");
      return;
    }
    if (!jdText.trim() && !jdFile) {
      setError("Please provide a job description (text or file).");
      return;
    }

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    if (jdFile) {
      formData.append("jd_file", jdFile);
    } else {
      formData.append("jd_text", jdText);
    }

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Something went wrong.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const score = result?.match_score ?? 0;
  const ringBackground = `conic-gradient(var(--indigo) ${score * 3.6}deg, var(--line) 0deg)`;

  return (
    <div className="min-h-screen">
      <header className="top-bar">
        <div className="max-w-4xl mx-auto flex items-center gap-3 px-4 py-4">
          <div className="logo-mark">R</div>
          <div>
            <p className="font-display text-base font-semibold leading-none">
              Resume Screener
            </p>
            <p className="text-xs text-gray-400 mt-1">
              Match analysis, powered by AI
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto py-10 px-4">
        <div className="mb-8">
          <p className="font-mono text-xs tracking-widest uppercase text-[var(--gold)] mb-2">
            Resume Diagnostics
          </p>
          <h1 className="font-display text-4xl font-semibold text-[var(--ink)]">
            How well do you match the role?
          </h1>
          <p className="text-gray-500 mt-2 text-sm max-w-lg">
            Upload a resume and a job description. We'll score the fit, flag
            missing keywords, and suggest specific edits.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 items-start">
          <div className="panel p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="step-badge">01</span>
              <h2 className="font-display text-lg font-medium">Inputs</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Resume (PDF or DOCX)
                </label>
                {resumeFile ? (
                  <div className="upload-box file-badge px-4 py-4 text-sm text-gray-700">
                    <span className="truncate">{resumeFile.name}</span>
                    <button
                      type="button"
                      onClick={() => setResumeFile(null)}
                      className="file-badge-remove"
                    >
                      Remove
                    </button>
                  </div>
                ) : (
                  <label className="upload-box flex items-center justify-center px-4 py-6 cursor-pointer text-sm text-gray-500">
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={(e) => setResumeFile(e.target.files[0])}
                      className="hidden"
                    />
                    Click to select a file
                  </label>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Job Description
                </label>
                <textarea
                  rows={5}
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                  placeholder="Paste the job description here..."
                  disabled={!!jdFile}
                  className="w-full text-sm border border-[var(--line)] rounded-lg p-3 disabled:bg-gray-100"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Or upload a JD file (PDF/DOCX)
                </label>
                {jdFile ? (
                  <div className="upload-box file-badge px-4 py-4 text-sm text-gray-700">
                    <span className="truncate">{jdFile.name}</span>
                    <button
                      type="button"
                      onClick={() => setJdFile(null)}
                      className="file-badge-remove"
                    >
                      Remove
                    </button>
                  </div>
                ) : (
                  <label className="upload-box flex items-center justify-center px-4 py-4 cursor-pointer text-sm text-gray-500">
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={(e) => setJdFile(e.target.files[0])}
                      className="hidden"
                    />
                    Click to select a file
                  </label>
                )}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full py-3 text-sm"
              >
                {loading ? "Analyzing..." : "Analyze Resume"}
              </button>

              {loading && <div className="scan-loader" />}
            </form>

            {error && (
              <p className="mt-4 text-sm font-medium text-red-600">{error}</p>
            )}
          </div>

          <div className="panel p-6">
            <div className="flex items-center gap-2 mb-5">
              <span className="step-badge">02</span>
              <h2 className="font-display text-lg font-medium">Results</h2>
            </div>

            {!result && !loading && (
              <div className="flex flex-col items-start gap-3 py-6">
                <div className="empty-state-icon">?</div>
                <p className="text-sm text-gray-400 max-w-xs">
                  Once you analyze a resume, your match score, missing
                  keywords, and rewrite suggestions will show up here.
                </p>
              </div>
            )}

            {loading && !result && (
              <div className="flex flex-col items-start gap-3 py-6">
                <div className="empty-state-icon">...</div>
                <p className="text-sm text-gray-400">
                  Reading the resume and comparing it to the job description.
                </p>
              </div>
            )}

            {result && (
              <div>
                <div className="flex items-center gap-5 mb-6">
                  <div
                    className="score-ring"
                    style={{ background: ringBackground }}
                  >
                    <div className="score-ring-value">
                      <p className="font-mono text-2xl font-semibold">
                        {score}
                      </p>
                      <p className="text-xs text-gray-400">/ 100</p>
                    </div>
                  </div>
                  <div>
                    <p className="font-display text-lg font-medium">
                      Match Score
                    </p>
                    <p className="text-sm text-gray-500">
                      Overall fit against this job description
                    </p>
                  </div>
                </div>

                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Missing Keywords
                </h3>
                <div className="flex flex-wrap gap-2 mb-6">
                  {result.missing_keywords.map((kw, idx) => (
                    <span key={idx} className="chip">
                      {kw}
                    </span>
                  ))}
                </div>

                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Suggestions
                </h3>
                <ol className="space-y-2">
                  {result.suggestions.map((sug, idx) => (
                    <li key={idx} className="flex gap-3 text-sm text-gray-600">
                      <span className="font-mono text-[var(--gold)] shrink-0">
                        {String(idx + 1).padStart(2, "0")}
                      </span>
                      <span>{sug}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        </div>

        <p className="text-xs text-gray-400 mt-10 text-center">
          Built for the AI Resume Screener internship project.
        </p>
      </main>
    </div>
  );
}