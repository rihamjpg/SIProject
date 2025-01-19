import { useQuery } from "@tanstack/react-query";
import { skillService } from "@/services/skill";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain } from "lucide-react";

export const SkillsPage = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["skills"],
    queryFn: skillService.getAll,
  });

  if (isLoading) return <div>Chargement...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Compétences</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.results.map((skill) => (
          <Card key={skill.id} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xl font-semibold">
                {skill.nom}
              </CardTitle>
              <Badge variant="secondary">{skill.employes_count} employés</Badge>
            </CardHeader>
            <CardContent>
              {skill.description || "Aucune description"}
              <div className="mt-4">
                <div className="text-sm text-gray-500">Employés:</div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {skill.employes.map((employeId) => (
                    <Badge key={employeId} variant="outline">
                      ID: {employeId}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
