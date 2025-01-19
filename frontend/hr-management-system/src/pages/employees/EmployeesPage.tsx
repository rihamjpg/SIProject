import { Button } from "@/components/ui/button";
import { Eye, Plus, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useQuery } from "@tanstack/react-query";
import { employeeService } from "@/services/employees";
import { Employee } from "@/types/employee";
import { useToast } from "@/hooks/use-toast";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { PaginatedResponse } from "@/types/pagination";

const EmployeesPage = () => {
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<
    Employee | undefined
  >();
  const { toast } = useToast();
  const navigate = useNavigate();

  const { data, isLoading, isError, error, refetch } = useQuery<
    PaginatedResponse<Employee>
  >({
    queryKey: ["employees"],
    queryFn: async () => {
      const response = await employeeService.getAll();
      return response as unknown as PaginatedResponse<Employee>;
    },
  });

  const employees = data?.results || [];

  console.log(employees[0]);

  if (isError) {
    return <div>Une erreur est survenue: {error.message}</div>;
  }

  const handleDelete = async (employee: Employee) => {
    try {
      await employeeService.delete(employee.id_employe);
      toast({
        title: "Succès",
        description: `L'employé ${employee.nom} a été supprimé`,
        className: "bg-green-50 border-green-500 text-green-900",
      });
      refetch();
    } catch (error) {
      toast({
        title: "Erreur",
        description: `L'employé ${employee.nom} a encore des conflits non résolus et n'a pas pu être supprimé`,
        className: "bg-red-50 border-red-500 text-red-900",
      });
    } finally {
      setIsDeleteDialogOpen(false);
      setSelectedEmployee(undefined);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Gestion des Employés</h1>
        <Button
          onClick={() => navigate("/employees/add")}
          className="space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Ajouter un employé</span>
        </Button>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Matricule</TableHead>
              <TableHead>Nom</TableHead>
              <TableHead>Prénom</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Service</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  Chargement...
                </TableCell>
              </TableRow>
            ) : employees.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  Aucun employé trouvé
                </TableCell>
              </TableRow>
            ) : (
              employees.map((employee: Employee) => (
                <TableRow key={employee.id_employe}>
                  <TableCell>{employee.matricule}</TableCell>
                  <TableCell>{employee.nom}</TableCell>
                  <TableCell>{employee.prenom}</TableCell>
                  <TableCell>{employee.email_pro}</TableCell>
                  <TableCell>{employee.service_name}</TableCell>

                  <TableCell className="text-right space-x-2">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() =>
                        navigate(`/employees/${employee.id_employe}`)
                      }
                      className="h-8 w-8 mr-2"
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="destructive"
                      size="icon"
                      onClick={() => {
                        setSelectedEmployee(employee);
                        setIsDeleteDialogOpen(true);
                      }}
                      className="h-8 w-8"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <AlertDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
      >
        <AlertDialogContent className="bg-white">
          <AlertDialogHeader>
            <AlertDialogTitle>Confirmer la suppression</AlertDialogTitle>
            <AlertDialogDescription>
              Êtes-vous sûr de vouloir supprimer cet employé ? Cette action est
              irréversible.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel className="hover:bg-gray-100 ">
              Annuler
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={() => selectedEmployee && handleDelete(selectedEmployee)}
              className="bg-red-500 text-white hover:bg-red-600"
            >
              Supprimer
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default EmployeesPage;
