import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { applicationService } from "@/services/application";
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
import { Calendar, CheckCircle, XCircle } from "lucide-react";

export const ApplicationsPage = () => {
  const { data } = useQuery({
    queryKey: ["applications"],
    queryFn: applicationService.getAll,
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case "En cours":
        return "bg-blue-100 text-blue-800";
      case "Accepté":
        return "bg-green-100 text-green-800";
      case "Refusé":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Candidatures</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Candidat</TableHead>
              <TableHead>Poste</TableHead>
              <TableHead>Date candidature</TableHead>
              <TableHead>Statut</TableHead>
              <TableHead>Documents</TableHead>
              <TableHead>Entretien</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((application) => (
              <TableRow key={application.id}>
                <TableCell>{application.candidat_name}</TableCell>
                <TableCell>{application.poste}</TableCell>
                <TableCell>
                  {format(
                    new Date(application.date_candidature),
                    "dd MMM yyyy",
                    {
                      locale: fr,
                    }
                  )}
                </TableCell>
                <TableCell>
                  <Badge className={getStatusColor(application.statut)}>
                    {application.statut}
                  </Badge>
                </TableCell>
                <TableCell>
                  {application.documents_valides ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-500" />
                  )}
                </TableCell>
                <TableCell>
                  {application.date_entretien ? (
                    format(
                      new Date(application.date_entretien),
                      "dd MMM yyyy",
                      {
                        locale: fr,
                      }
                    )
                  ) : (
                    <Button variant="ghost" size="icon">
                      <Calendar className="h-4 w-4" />
                    </Button>
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
