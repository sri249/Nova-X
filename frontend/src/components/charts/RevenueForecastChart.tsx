"use client";

import { ResponsiveContainer, ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface RevenueForecastChartProps {
  data: any[];
}

export function RevenueForecastChart({ data }: RevenueForecastChartProps) {
  return (
    <div className="h-[350px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart
          data={data}
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid stroke="#f5f5f5" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="revenue" barSize={20} fill="#413ea0" name="Revenue" />
          <Line type="monotone" dataKey="expenses" stroke="#ff7300" name="Expenses" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
