"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";
import type { RadarAxis } from "@/types/scout";

interface Props {
  axes: RadarAxis[];
  color?: string;
  size?: number;
}

export default function ScoutRadarChart({ axes, color = "#8b5cf6", size = 280 }: Props) {
  return (
    <ResponsiveContainer width="100%" height={size}>
      <RadarChart data={axes} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="#2a2a38" />
        <PolarAngleAxis
          dataKey="label"
          tick={{ fill: "#9ca3af", fontSize: 11, fontWeight: 500 }}
        />
        <Radar
          name="Player"
          dataKey="value"
          stroke={color}
          fill={color}
          fillOpacity={0.25}
          strokeWidth={2}
          dot={{ r: 3, fill: color, strokeWidth: 0 }}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
