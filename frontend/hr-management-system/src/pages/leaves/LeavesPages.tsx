import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { leaveService } from "@/services/leave";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const statusColors = {
  DEMANDE: "bg-yellow-100 text-yellow-800 border-yellow-200",
  APPROUVE: "bg-green-100 text-green-800 border-green-200",
  REFUSE: "bg-red-100 text-red-800 border-red-200",
};

export const LeavesPage = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["leaves"],
    queryFn: leaveService.getAll,
  });

  if (isLoading) {
    return <div>Chargement...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Gestion des Congés</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Début</TableHead>
              <TableHead>Fin</TableHead>
              <TableHead>Jours</TableHead>
              <TableHead>Statut</TableHead>
              <TableHead>Solde</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((leave) => (
              <TableRow key={leave.id}>
                <TableCell>{leave.employe_name}</TableCell>
                <TableCell>{leave.type_conge}</TableCell>
                <TableCell>
                  {format(new Date(leave.date_debut), "dd MMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>
                  {format(new Date(leave.date_fin), "dd MMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>{leave.nb_jours}</TableCell>
                <TableCell>
                  <Badge className={statusColors[leave.statut]}>
                    {leave.statut}
                  </Badge>
                </TableCell>
                <TableCell>{leave.solde_restant} jours</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
