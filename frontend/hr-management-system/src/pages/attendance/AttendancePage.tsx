import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { attendanceService } from "@/services/attendance";
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

export const AttendancePage = () => {
  const [page, setPage] = useState(1);

  const { data } = useQuery({
    queryKey: ["attendance", page],
    queryFn: () => attendanceService.getAll(page),
  });

  const getStatusBadge = (attendance: any) => {
    if (attendance.jour_ferie)
      return <Badge className="bg-blue-100 text-blue-800">Férié</Badge>;
    if (attendance.conge)
      return <Badge className="bg-purple-100 text-purple-800">Congé</Badge>;
    if (attendance.present)
      return <Badge className="bg-green-100 text-green-800">Présent</Badge>;
    return <Badge className="bg-red-100 text-red-800">Absent</Badge>;
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Pointages</h1>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employé</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Arrivée</TableHead>
              <TableHead>Départ</TableHead>
              <TableHead>Heures</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Supplémentaires</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.results.map((attendance) => (
              <TableRow key={attendance.id}>
                <TableCell>{attendance.employe_name}</TableCell>
                <TableCell>
                  {format(new Date(attendance.date_pointage), "dd MMMM yyyy", {
                    locale: fr,
                  })}
                </TableCell>
                <TableCell>{attendance.heure_arrivee}</TableCell>
                <TableCell>{attendance.heure_depart}</TableCell>
                <TableCell>{attendance.heures_travaillees}h</TableCell>
                <TableCell>{getStatusBadge(attendance)}</TableCell>
                <TableCell>{attendance.heures_supplementaires}h</TableCell>
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
