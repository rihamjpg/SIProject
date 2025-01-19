import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getAnalytics } from "@/services/analytics";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

export const AnalyticsPage = () => {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["analytics"],
    queryFn: async () => {
      console.log("Fetching analytics...");
      const data = await getAnalytics();
      console.log("Analytics data:", data);
      return data;
    },
  });

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="text-center">Chargement des données...</div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-6">
        <div className="text-center text-red-500">
          Une erreur est survenue lors du chargement des données
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Tableau de Bord Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Total Employees Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Employés
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.total}</div>
          </CardContent>
        </Card>

        {/* Service Distribution Card */}
        <Card className="col-span-1 md:col-span-2 lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-sm font-medium">
              Distribution par Service
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.by_service}
                  nameKey="id_service__nom_service"
                  dataKey="count"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ id_service__nom_service, percent }) =>
                    `${id_service__nom_service} (${(percent * 100).toFixed(
                      0
                    )}%)`
                  }
                >
                  {data.by_service.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Education Distribution Card */}
        <Card className="col-span-1 md:col-span-2 lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-sm font-medium">
              Distribution par Niveau d'Études
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.by_education}
                  nameKey="niveau_etudes"
                  dataKey="count"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ niveau_etudes, percent }) =>
                    `${niveau_etudes} (${(percent * 100).toFixed(0)}%)`
                  }
                >
                  {data.by_education.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AnalyticsPage;
