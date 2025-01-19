import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { recruitmentService } from "@/services/recruitment";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Flame } from "lucide-react";

export const RecruitmentsPage = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["recruitments"],
    queryFn: recruitmentService.getAll,
  });

  if (isLoading) return <div>Chargement...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Recrutements</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {data?.results.map((recruitment) => (
          <Card key={recruitment.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle>{recruitment.titre_poste}</CardTitle>
                  <p className="text-sm text-gray-500">
                    {recruitment.reference_poste}
                  </p>
                </div>
                <div className="flex gap-2">
                  {recruitment.urgent && (
                    <Badge className="bg-red-100 text-red-800">
                      <Flame className="w-4 h-4 mr-1" />
                      Urgent
                    </Badge>
                  )}
                  <Badge
                    className={
                      recruitment.statut === "OUVERT"
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }
                  >
                    {recruitment.statut}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Service</p>
                  <p>{recruitment.service_name}</p>
                </div>
                <div>
                  <p className="text-gray-500">Type de contrat</p>
                  <p>{recruitment.type_contrat_propose}</p>
                </div>
                <div>
                  <p className="text-gray-500">Salaire proposé</p>
                  <p>
                    {Number(recruitment.salaire_propose).toLocaleString(
                      "fr-FR"
                    )}{" "}
                    DZD
                  </p>
                </div>
                <div>
                  <p className="text-gray-500">Postes disponibles</p>
                  <p>{recruitment.postes_disponibles}</p>
                </div>
              </div>
              <div>
                <p className="text-gray-500">Date limite</p>
                <p>
                  {format(new Date(recruitment.date_cloture), "dd MMMM yyyy", {
                    locale: fr,
                  })}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
