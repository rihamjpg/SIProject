import { ColumnDef } from "@tanstack/react-table";
import { Employee } from "@/types/employee";
import { Button } from "@/components/ui/button";
import { MoreHorizontal, Edit, Trash } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export const columns: ColumnDef<Employee>[] = [
  {
    accessorKey: "matricule",
    header: "Matricule",
  },
  {
    accessorKey: "nom",
    header: "Nom",
  },
  {
    accessorKey: "prenom",
    header: "Prénom",
  },
  {
    accessorKey: "email_pro",
    header: "Email",
  },
  {
    accessorKey: "poste_occupe",
    header: "Poste",
  },
  {
    accessorKey: "service.nom_service",
    header: "Service",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const employee = row.original;
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => console.log("edit", employee)}>
              <Edit className="mr-2 h-4 w-4" />
              Modifier
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => console.log("delete", employee)}>
              <Trash className="mr-2 h-4 w-4" />
              Supprimer
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];
