import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { massroufService } from "@/services/massrouf";
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
  EN_ATTENTE: "bg-yellow-100 text-yellow-800",
  APPROUVÉ: "bg-green-100 text-green-800",
  REJETÉ: "bg-red-100 text-red-800",
};

export const MassroufPage = () => {
  const { data } = useQuery({
    queryKey: ["massroufs"],
    queryFn: massroufService.getAll,
  });

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Avances sur Salaire</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Montant</TableHead>
              <TableHead>Date demande</TableHead>
              <TableHead>Statut</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((massrouf) => (
              <TableRow key={massrouf.id}>
                <TableCell>{massrouf.employe_name}</TableCell>
                <TableCell>
                  {Number(massrouf.montant_demande).toLocaleString("fr-FR")} DZD
                </TableCell>
                <TableCell>
                  {format(new Date(massrouf.date_demande), "dd MMMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>
                  <Badge className={statusColors[massrouf.statut]}>
                    {massrouf.statut}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
