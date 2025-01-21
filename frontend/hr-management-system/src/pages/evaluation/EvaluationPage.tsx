import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { evaluationService } from "@/services/evaluation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
// import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export const EvaluationsPage = () => {
  const { data } = useQuery({
    queryKey: ["evaluations"],
    queryFn: evaluationService.getAll,
  });

  const getScoreColor = (score: number) => {
    if (score >= 15) return "bg-green-100 text-green-800";
    if (score >= 10) return "bg-yellow-100 text-yellow-800";
    return "bg-red-100 text-red-800";
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Évaluations</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Évaluateur</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Note</TableHead>
              <TableHead>Période</TableHead>
              <TableHead>Prochaine évaluation</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((evaluation) => (
              <TableRow key={evaluation.id}>
                <TableCell>{evaluation.employe_name}</TableCell>
                <TableCell>{evaluation.evaluateur_name}</TableCell>
                <TableCell>
                  {format(new Date(evaluation.date_evaluation), "dd MMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>
                  <Badge className={getScoreColor(evaluation.note_globale)}>
                    {evaluation.note_globale.toFixed(1)}/20
                  </Badge>
                </TableCell>
                <TableCell>{evaluation.periode}</TableCell>
                <TableCell>
                  {format(
                    new Date(evaluation.date_prochaine_evaluation),
                    "dd MMM yyyy",
                    {
                      locale: fr,
                    }
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
