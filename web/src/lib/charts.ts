import * as echarts from "echarts";

type Theme = "light" | "dark";

export function getTheme(): Theme {
  return (document.documentElement.dataset.theme as Theme) || "light";
}

export function chartPalette(theme: Theme) {
  const isDark = theme === "dark";
  return {
    text: isDark ? "#fafafa" : "#0a0a0a",
    textMuted: isDark ? "#a1a1aa" : "#6b7280",
    grid: isDark ? "#1f1f1f" : "#f3f4f6",
    border: isDark ? "#262626" : "#e5e5e5",
    bg: isDark ? "#141414" : "#ffffff",
    accent: isDark ? "#60a5fa" : "#2563eb",
    success: isDark ? "#4ade80" : "#16a34a",
    danger: isDark ? "#f87171" : "#dc2626",
    muted: isDark ? "#525252" : "#9ca3af",
  };
}

export function baseOption(theme: Theme): echarts.EChartsOption {
  const p = chartPalette(theme);
  return {
    textStyle: { color: p.text, fontFamily: "Inter, system-ui, sans-serif" },
    grid: { left: 50, right: 20, top: 30, bottom: 40, containLabel: true },
    tooltip: {
      trigger: "axis",
      backgroundColor: p.bg,
      borderColor: p.border,
      borderWidth: 1,
      textStyle: { color: p.text, fontSize: 12 },
      axisPointer: {
        type: "cross",
        lineStyle: { color: p.muted, type: "dashed" },
        crossStyle: { color: p.muted },
        label: { backgroundColor: p.textMuted },
      },
    },
    xAxis: {
      type: "category",
      axisLine: { lineStyle: { color: p.border } },
      axisLabel: { color: p.textMuted, fontSize: 11 },
      splitLine: { show: false },
    },
    yAxis: {
      type: "value",
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: p.textMuted, fontSize: 11 },
      splitLine: { lineStyle: { color: p.grid } },
    },
    legend: {
      top: 4,
      textStyle: { color: p.textMuted, fontSize: 12 },
      itemWidth: 14,
      itemHeight: 8,
    },
  };
}

type InitFn = (theme: Theme) => echarts.EChartsOption;

export function mountChart(elId: string, getOption: InitFn) {
  const el = document.getElementById(elId);
  if (!el) return;

  let chart = echarts.init(el);
  chart.setOption(getOption(getTheme()));

  const handleResize = () => chart.resize();
  window.addEventListener("resize", handleResize);

  document.addEventListener("themechange", () => {
    chart.dispose();
    chart = echarts.init(el);
    chart.setOption(getOption(getTheme()));
  });

  return chart;
}
