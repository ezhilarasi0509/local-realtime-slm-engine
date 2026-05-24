"use client";

import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

type BenchmarkResult = {
  model: string;
  response: {
    topic?: string;
    definition?: string;
    key_points?: string[];
    example?: string;
  };
  model_size: number;
  ram_usage: number;
  tokens_per_sec: number;
  token_count: number;
  inference_time: number;
  response_length: number;
  latency_ms: number;
  time_to_first_token: number;
  speed_score: number;
  quality_score: number;
  relevance_score: number;
  completeness_score: number;
  structure_score: number;
  final_score: number;
  valid_output: boolean;
  retry_count: number;
};

type BenchmarkResponse = {
  benchmark_id?: string;
  request_id?: string;
  timestamp?: string;
  prompt: string;
  best_model: string;
  why_model_won: string[];
  leaderboard: {
    rank: number;
    model: string;
    score: number;
  }[];
  results: BenchmarkResult[];
};

type FinalSummary = {
  benchmark_summary?: {
    total_single_benchmark_runs: number;
    model_summary: any[];
  };
  system_profile?: any;
};

export default function Home() {
  const [prompt, setPrompt] = useState(
    "Explain model inference and why tokens per second matters."
  );

  const [temperature, setTemperature] = useState(0);
  const [benchmark, setBenchmark] = useState<BenchmarkResponse | null>(null);
  const [summary, setSummary] = useState<FinalSummary | null>(null);

  const [loadingBenchmark, setLoadingBenchmark] = useState(false);
  const [loadingSuite, setLoadingSuite] = useState(false);
  const [error, setError] = useState("");

  const modelIcons: Record<string, string> = {
    llama3: "🦙",
    mistral: "🌪️",
    phi3: "🧠",
  };

  async function fetchFinalSummary() {
    try {
      const res = await fetch(`${API_BASE}/api/v1/reports/final-summary`);
      const data = await res.json();
      setSummary(data);
    } catch {
      setError("Backend not connected. Start FastAPI server.");
    }
  }

  useEffect(() => {
    fetchFinalSummary();
  }, []);

  async function runBenchmark() {
    if (!prompt.trim()) {
      setError("Please enter a prompt.");
      return;
    }

    setError("");
    setLoadingBenchmark(true);

    try {
      const res = await fetch(`${API_BASE}/benchmark`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "llama3",
          prompt,
          temperature,
        }),
      });

      if (!res.ok) {
        throw new Error("Benchmark failed");
      }

      const data = await res.json();
      setBenchmark(data);
      await fetchFinalSummary();
    } catch {
      setError("Benchmark failed. Check backend and Ollama.");
    } finally {
      setLoadingBenchmark(false);
    }
  }

  async function runSmallSuite() {
    setError("");
    setLoadingSuite(true);

    try {
      const res = await fetch(`${API_BASE}/api/v1/benchmark-suite/run-small`, {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error("Small suite failed");
      }

      await fetchFinalSummary();
    } catch {
      setError("Small suite failed. Check backend.");
    } finally {
      setLoadingSuite(false);
    }
  }

  function exportJson() {
    window.open(`${API_BASE}/api/v1/reports/export-json`, "_blank");
  }

  function exportCsv() {
    window.open(`${API_BASE}/api/v1/reports/export-csv`, "_blank");
  }

  function openReport() {
    window.open(`${API_BASE}/api/v1/reports/final-summary`, "_blank");
  }

  const installedModels =
    summary?.system_profile?.ollama?.installed_models || [];

  const hardware = summary?.system_profile?.hardware;
  const machine = summary?.system_profile?.machine;

  const bestResult = benchmark?.results?.find(
    (item) => item.model === benchmark.best_model
  );

  const rankedResults =
    benchmark?.results
      ?.slice()
      .sort((a, b) => b.final_score - a.final_score) || [];

  return (
    <main className="min-h-screen bg-[#0B1120] px-4 py-4 text-slate-100">
      <div className="mx-auto max-w-[1600px]">
        {/* HEADER */}
        <section className="mb-4 rounded-[26px] border border-slate-700/70 bg-[#111827] px-6 py-5 shadow-2xl">
          <h1 className="text-center text-4xl font-black tracking-tight text-slate-50 md:text-5xl">
            Local LLM Benchmark Dashboard
          </h1>

          <p className="mx-auto mt-3 max-w-3xl text-center text-sm leading-6 text-slate-400 md:text-base">
            Offline Ollama model comparison across latency, throughput,
            structured JSON reliability, retry behavior, and output quality.
          </p>
        </section>

        {error && (
          <div className="mb-4 rounded-2xl border border-red-400/40 bg-red-500/10 p-4 text-sm text-red-200">
            {error}
          </div>
        )}

        {/* TOP GRID */}
        <section className="grid gap-4 xl:grid-cols-[1.55fr_0.85fr]">
          {/* BENCHMARK INPUT */}
          <section className="rounded-[26px] border border-cyan-500/25 bg-[#111827] p-5 shadow-xl shadow-cyan-950/10">
            <div className="mb-3 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-2xl font-bold text-slate-50">
                  Run Model Benchmark
                </h2>
                <p className="text-sm text-cyan-100/60">
                  Runs the same prompt across Phi3, Llama3, and Mistral.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-cyan-300">
                  Temperature
                </span>
                <select
                  value={temperature}
                  onChange={(e) => setTemperature(Number(e.target.value))}
                  className="rounded-xl border border-cyan-500/40 bg-[#0F172A] px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-300"
                >
                  <option value={0}>0 deterministic</option>
                  <option value={0.7}>0.7 stochastic</option>
                </select>
              </div>
            </div>

            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full resize-none rounded-2xl border border-cyan-500/25 bg-[#0F172A] p-4 text-sm leading-6 text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-cyan-300"
            />

            <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              <button
                onClick={runBenchmark}
                disabled={loadingBenchmark}
                className="rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-black text-white shadow-lg shadow-emerald-700/20 transition hover:-translate-y-1 hover:bg-emerald-500 disabled:opacity-60"
              >
                {loadingBenchmark ? "Running..." : "Run Benchmark"}
              </button>

              <button
                onClick={runSmallSuite}
                disabled={loadingSuite}
                className="rounded-2xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-bold text-slate-100 transition hover:border-cyan-500/50 hover:bg-slate-700 disabled:opacity-60"
              >
                {loadingSuite ? "Running Suite..." : "Run Small Suite"}
              </button>

              <button
                onClick={exportJson}
                className="rounded-2xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-bold text-slate-100 transition hover:border-cyan-500/50 hover:bg-slate-700"
              >
                Export JSON
              </button>

              <button
                onClick={exportCsv}
                className="rounded-2xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-bold text-slate-100 transition hover:border-cyan-500/50 hover:bg-slate-700"
              >
                Export CSV
              </button>

              <button
                onClick={openReport}
                className="rounded-2xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-bold text-slate-100 transition hover:border-cyan-500/50 hover:bg-slate-700"
              >
                Final Report
              </button>
            </div>
          </section>

          {/* INSTALLED MODELS */}
          <section className="rounded-[26px] border border-indigo-500/25 bg-[#111827] p-5 shadow-xl shadow-indigo-950/10">
            <h2 className="text-xl font-bold text-slate-50">
              Installed Ollama Models
            </h2>

            <p className="mt-1 text-sm text-indigo-100/60">
              Local models available for offline inference.
            </p>

            <div className="mt-4 space-y-3">
              {installedModels.map((model: any) => (
                <div
                  key={model.name}
                  className="flex items-center justify-between rounded-2xl border border-indigo-500/10 bg-[#0F172A] p-4"
                >
                  <div>
                    <p className="font-bold text-slate-100">{model.name}</p>
                    <p className="text-xs text-indigo-200/40">ID: {model.id}</p>
                  </div>

                  <span className="rounded-xl bg-indigo-500/20 px-3 py-1 text-sm font-bold text-indigo-100">
                    {model.size} GB
                  </span>
                </div>
              ))}
            </div>
          </section>
        </section>

        {/* SYSTEM PROFILE */}
        <section className="mt-4 grid gap-3 md:grid-cols-4">
          <ProfileStat label="OS" value={machine?.os || "-"} />
          <ProfileStat
            label="Architecture"
            value={machine?.architecture || "-"}
          />
          <ProfileStat
            label="CPU Cores"
            value={hardware?.cpu_cores_logical || "-"}
          />
          <ProfileStat
            label="RAM"
            value={`${hardware?.total_ram_gb || "-"} GB`}
          />
        </section>

        {/* FULL WIDTH MODEL CARDS */}
        <section className="mt-4 grid gap-4 xl:grid-cols-3">
          {rankedResults.length > 0 ? (
            rankedResults.map((item, index) => {
              const isWinner = item.model === benchmark?.best_model;

              return (
                <div
                  key={item.model}
                  className={`rounded-[30px] border p-5 shadow-xl transition hover:-translate-y-1 ${
                    isWinner
                      ? "border-emerald-400/70 bg-emerald-700 text-white shadow-emerald-900/20"
                      : "border-slate-700/70 bg-[#111827] text-slate-100"
                  }`}
                >
                  <div className="mb-5 flex items-center justify-between gap-3">
                    <h3 className="text-3xl font-black capitalize text-slate-50">
                      {index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉"}{" "}
                      {modelIcons[item.model]} {item.model}
                    </h3>

                    {isWinner && (
                      <span className="rounded-full bg-[#0B1120] px-4 py-2 text-xs font-black text-emerald-300">
                        Winner
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <Metric
                      label="Score"
                      value={item.final_score}
                      winner={isWinner}
                      tone="performance"
                    />
                    <Metric
                      label="Latency"
                      value={`${item.latency_ms} ms`}
                      winner={isWinner}
                      tone="performance"
                    />
                    <Metric
                      label="TTFT"
                      value={`${item.time_to_first_token}s`}
                      winner={isWinner}
                      tone="performance"
                    />
                    <Metric
                      label="Tokens/sec"
                      value={item.tokens_per_sec}
                      winner={isWinner}
                      tone="performance"
                    />
                    <Metric
                      label="Valid JSON"
                      value={item.valid_output ? "Yes" : "No"}
                      winner={isWinner}
                      tone="reliability"
                    />
                    <Metric
                      label="Retries"
                      value={item.retry_count}
                      winner={isWinner}
                      tone="warning"
                    />
                  </div>
                </div>
              );
            })
          ) : (
            <>
              <EmptyModel name="Phi3" icon="🧠" />
              <EmptyModel name="Llama3" icon="🦙" />
              <EmptyModel name="Mistral" icon="🌪️" />
            </>
          )}
        </section>

        {/* BEST MODEL OUTPUT */}
        <section className="mt-4 rounded-[26px] border border-slate-700/70 bg-[#111827] p-5 shadow-xl">
          <div className="mb-5 flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
            <div>
              <h2 className="text-2xl font-bold text-slate-50">
                Best Model Structured Output
              </h2>
              <p className="mt-1 text-sm text-slate-400">
                Detailed JSON response from the winning model with benchmark
                identifiers and decision reasons.
              </p>
            </div>

            {benchmark && (
              <div className="grid w-full gap-3 md:grid-cols-2 xl:max-w-[650px]">
                <IdCard
                  label="Benchmark ID"
                  value={benchmark.benchmark_id || "-"}
                  tone="benchmark"
                />
                <IdCard
                  label="Request ID"
                  value={benchmark.request_id || "-"}
                  tone="request"
                />
              </div>
            )}
          </div>

          {bestResult ? (
            <div className="grid gap-4 xl:grid-cols-[1.15fr_0.95fr_0.7fr]">
              <div className="rounded-2xl bg-[#0F172A] p-5">
                <SectionLabel tone="performance">Topic</SectionLabel>
                <h3 className="mt-2 text-2xl font-black text-slate-50">
                  {bestResult.response.topic || "No topic returned"}
                </h3>

                <SectionLabel tone="performance" className="mt-5">
                  Definition
                </SectionLabel>
                <p className="mt-2 text-sm leading-7 text-slate-300">
                  {bestResult.response.definition || "No definition returned."}
                </p>

                <SectionLabel tone="performance" className="mt-5">
                  Example
                </SectionLabel>
                <p className="mt-2 text-sm leading-7 text-slate-300">
                  {bestResult.response.example || "No example returned."}
                </p>
              </div>

              <div className="rounded-2xl bg-[#0F172A] p-5">
                <SectionLabel tone="reliability">Key Points</SectionLabel>

                <div className="mt-3 space-y-3">
                  {(bestResult.response.key_points || []).length > 0 ? (
                    bestResult.response.key_points?.map((point, index) => (
                      <div
                        key={index}
                        className="rounded-2xl border border-slate-700 bg-[#111827] p-4 text-sm leading-6 text-slate-300"
                      >
                        <span className="mr-2 font-black text-emerald-300">
                          {index + 1}.
                        </span>
                        {point}
                      </div>
                    ))
                  ) : (
                    <div className="rounded-2xl border border-dashed border-slate-700 p-6 text-center text-sm text-slate-500">
                      No key points returned.
                    </div>
                  )}
                </div>
              </div>

              <div className="rounded-2xl bg-[#0F172A] p-5">
                <SectionLabel tone="reliability">Why It Won</SectionLabel>

                <h3 className="mt-2 text-3xl font-black capitalize text-emerald-300">
                  {modelIcons[benchmark.best_model]} {benchmark.best_model}
                </h3>

                <div className="mt-5 space-y-3">
                  {benchmark.why_model_won.length > 0 ? (
                    benchmark.why_model_won.map((reason, index) => (
                      <div
                        key={index}
                        className="rounded-2xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-sm font-semibold leading-6 text-emerald-100"
                      >
                        ✓ {reason}
                      </div>
                    ))
                  ) : (
                    <div className="rounded-2xl border border-slate-700 bg-[#111827] p-4 text-sm leading-6 text-slate-400">
                      Winner selected by highest weighted benchmark score.
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-2xl border border-dashed border-slate-700 p-10 text-center text-sm text-slate-400">
              Run a benchmark to show the detailed winning model output here.
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

function ProfileStat({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="rounded-2xl border border-slate-700/70 bg-[#111827] p-4 shadow-lg">
      <p className="text-[11px] font-bold uppercase tracking-[0.22em] text-slate-400">
        {label}
      </p>
      <p className="mt-2 text-2xl font-black capitalize text-slate-50">
        {value}
      </p>
    </div>
  );
}

function Metric({
  label,
  value,
  winner,
  tone,
}: {
  label: string;
  value: string | number;
  winner: boolean;
  tone: "performance" | "reliability" | "warning";
}) {
  const labelTone = {
    performance: "text-cyan-300",
    reliability: "text-emerald-300",
    warning: "text-amber-300",
  };

  return (
    <div
      className={`rounded-2xl p-4 ${
        winner
          ? "bg-slate-50 text-slate-950"
          : "bg-[#0F172A] text-slate-100"
      }`}
    >
      <p
        className={`text-[11px] font-black uppercase tracking-[0.18em] ${
          winner ? "text-slate-600" : labelTone[tone]
        }`}
      >
        {label}
      </p>
      <p
        className={`mt-2 text-xl font-black ${
          winner ? "text-slate-950" : "text-slate-50"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function EmptyModel({
  name,
  icon,
}: {
  name: string;
  icon: string;
}) {
  return (
    <div className="rounded-[30px] border border-dashed border-slate-700 bg-[#111827] p-5">
      <h3 className="text-3xl font-black text-slate-50">
        {icon} {name}
      </h3>
      <div className="mt-5 rounded-2xl bg-[#0F172A] p-8 text-center text-sm text-slate-500">
        Run benchmark to load metrics.
      </div>
    </div>
  );
}

function IdCard({
  label,
  value,
  tone,
}: {
  label: string;
  value: string | number;
  tone: "benchmark" | "request";
}) {
  const toneClass = {
    benchmark: {
      label: "text-amber-300",
      border: "border-amber-400/20",
      bg: "bg-amber-400/5",
    },
    request: {
      label: "text-cyan-300",
      border: "border-cyan-400/20",
      bg: "bg-cyan-400/5",
    },
  };

  return (
    <div
      className={`rounded-2xl border ${toneClass[tone].border} ${toneClass[tone].bg} px-4 py-3`}
    >
      <p
        className={`text-[10px] font-bold uppercase tracking-[0.2em] ${toneClass[tone].label}`}
      >
        {label}
      </p>
      <p className="mt-1 truncate text-xs font-bold text-slate-300">{value}</p>
    </div>
  );
}

function SectionLabel({
  children,
  tone,
  className = "",
}: {
  children: React.ReactNode;
  tone: "performance" | "reliability";
  className?: string;
}) {
  const labelTone = {
    performance: "text-cyan-300",
    reliability: "text-emerald-300",
  };

  return (
    <p
      className={`${className} text-xs font-bold uppercase tracking-widest ${labelTone[tone]}`}
    >
      {children}
    </p>
  );
}