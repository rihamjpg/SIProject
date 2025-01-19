import {
  Bar,
  BarChart as RechartsBarChart,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { LeaveData } from "@/types/analytics";

interface BarChartProps {
  data: LeaveData[];
}

export const BarChart = ({ data }: BarChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsBarChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="hsl(var(--primary))" />
      </RechartsBarChart>
    </ResponsiveContainer>
  );
};

import { Line, LineChart as RechartsLineChart } from "recharts";
import { EmployeeGrowthData } from "@/types/analytics";

interface LineChartProps {
  data: EmployeeGrowthData[];
}

export const LineChart = ({ data }: LineChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsLineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="count" stroke="hsl(var(--primary))" />
      </RechartsLineChart>
    </ResponsiveContainer>
  );
};
