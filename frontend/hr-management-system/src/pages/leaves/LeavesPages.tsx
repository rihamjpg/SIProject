// import { Button } from "@/components/ui/button";
// import { DataTable } from "@/components/ui/data-table";
// import { Plus } from "lucide-react";
// import { columns } from "./columns";
// import { useState } from "react";
// import { AddLeaveDialog } from "@/components/leaves/AddLeaveDialog";

// const LeavesPage = () => {
//   const [isDialogOpen, setIsDialogOpen] = useState(false);

//   return (
//     <div className="space-y-6">
//       <div className="flex justify-between items-center">
//         <h1 className="text-3xl font-bold">Gestion des Congés</h1>
//         <Button onClick={() => setIsDialogOpen(true)}>
//           <Plus className="mr-2 h-4 w-4" />
//           Demander un Congé
//         </Button>
//       </div>
//       <DataTable columns={columns} data={[]} />
//       <AddLeaveDialog open={isDialogOpen} onOpenChange={setIsDialogOpen} />
//     </div>
//   );
// };

// export default LeavesPage;
