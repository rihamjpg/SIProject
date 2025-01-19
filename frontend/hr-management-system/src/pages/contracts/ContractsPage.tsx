import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { contractService } from "@/services/contract";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Eye } from "lucide-react";

export const ContractsPage = () => {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["contracts", page],
    queryFn: () => contractService.getAll(page),
  });

  if (isLoading) return <div>Chargement...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Contrats</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Date début</TableHead>
              <TableHead>Salaire</TableHead>
              <TableHead>Statut</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((contract) => (
              <TableRow key={contract.id}>
                <TableCell>{contract.employe_name}</TableCell>
                <TableCell>{contract.type_contrat}</TableCell>
                <TableCell>
                  {format(new Date(contract.date_debut), "dd MMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>
                  {Number(contract.salaire_base).toLocaleString("fr-FR")}{" "}
                  {contract.devise}
                </TableCell>
                <TableCell>
                  <Badge
                    className={
                      contract.statut === "ACTIF"
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }
                  >
                    {contract.statut}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      /* TODO: Show details dialog */
                    }}
                  >
                    <Eye className="h-4 w-4" />
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
          onClick={() => setPage(page - 1)}
        >
          Précédent
        </Button>
        <Button
          variant="outline"
          disabled={!data?.next}
          onClick={() => setPage(page + 1)}
        >
          Suivant
        </Button>
      </div>
    </div>
  );
};
