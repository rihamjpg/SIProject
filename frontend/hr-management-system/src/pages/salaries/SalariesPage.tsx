import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { FileText } from "lucide-react";
import { salaryService } from "@/services/salary";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";

export const SalariesPage = () => {
  const [page, setPage] = useState(1);
  const { toast } = useToast();

  const { data, isLoading } = useQuery({
    queryKey: ["salaries", page],
    queryFn: () => salaryService.getAll(page),
  });

  const generatePaySlip = useMutation({
    mutationFn: salaryService.generatePaySlip,
    onSuccess: () => {
      toast({
        title: "Succès",
        description: "Fiche de paie générée avec succès",
        className: "bg-green-50 border-green-500 text-green-900",
      });
    },
  });

  if (isLoading) return <div>Chargement...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Salaires</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Période</TableHead>
              <TableHead>Salaire de base</TableHead>
              <TableHead>Primes</TableHead>
              <TableHead>Montant final</TableHead>
              <TableHead>Statut</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((salary) => (
              <TableRow key={salary.id}>
                <TableCell>{salary.employe_name}</TableCell>
                <TableCell>
                  {format(new Date(salary.date_paiement), "MMMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>
                  {Number(salary.salaire_base).toLocaleString("fr-FR")} DZD
                </TableCell>
                <TableCell>
                  {(
                    Number(salary.prime_rendement) +
                    Number(salary.prime_anciennete)
                  ).toLocaleString("fr-FR")}{" "}
                  DZD
                </TableCell>
                <TableCell className="font-medium">
                  {Number(salary.montant_final).toLocaleString("fr-FR")} DZD
                </TableCell>
                <TableCell>
                  <Badge className="bg-green-100 text-green-800">
                    {salary.statut_paiement}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => generatePaySlip.mutate(salary.id)}
                    disabled={salary.fiche_paie_generee}
                  >
                    <FileText className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="flex justify-end space-x-2">
        <Button
          variant="outline"
          disabled={!data?.previous}
          onClick={() => setPage((p) => p - 1)}
        >
          Précédent
        </Button>
        <Button
          variant="outline"
          disabled={!data?.next}
          onClick={() => setPage((p) => p + 1)}
        >
          Suivant
        </Button>
      </div>
    </div>
  );
};
