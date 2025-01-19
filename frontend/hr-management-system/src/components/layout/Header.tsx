import { Button } from "@/components/ui/button";
import { authService } from "@/services/auth";
import { LogOut, User } from "lucide-react";

export const Header = () => {
  const userType = authService.getUserType();

  return (
    <header className="bg-white border-b h-16 px-6 flex items-center justify-between">
      <h1 className="text-xl font-semibold">Système GRH</h1>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600 flex items-center gap-2">
          <User size={16} />
          {userType?.toUpperCase()}
        </span>
        <Button variant="ghost" size="sm" onClick={() => authService.logout()}>
          <LogOut size={16} className="mr-2" />
          Déconnexion
        </Button>
      </div>
    </header>
  );
};
