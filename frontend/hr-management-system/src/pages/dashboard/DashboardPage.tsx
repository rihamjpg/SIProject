import { Card } from "@/components/ui/card";

const DashboardPage = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Tableau de Bord</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6">
          <h3 className="font-semibold text-gray-500">Total Employés</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
        <Card className="p-6">
          <h3 className="font-semibold text-gray-500">Congés en Attente</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
        <Card className="p-6">
          <h3 className="font-semibold text-gray-500">Départements</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
