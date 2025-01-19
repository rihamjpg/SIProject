import { NavLink } from "react-router-dom";
import {
  Home,
  Users,
  Calendar,
  FileText,
  BarChart,
  DollarSign,
  Clock,
  History,
  ClipboardCheck,
  Brain,
} from "lucide-react";

const navigation = [
  { name: "Tableau de bord", href: "/", icon: Home },
  { name: "Employés", href: "/employees", icon: Users },
  { name: "Congés", href: "/leaves", icon: Calendar },
  { name: "Contrats", href: "/contracts", icon: FileText },
  { name: "Analytics", href: "/analytics", icon: BarChart },
  {
    name: "Salaires",
    href: "/salaries",
    icon: DollarSign,
  },
  {
    name: "Pointages",
    href: "/attendance",
    icon: Clock,
  },
  {
    name: "Historique",
    href: "/history",
    icon: History,
  },
  {
    name: "Évaluations",
    href: "/evaluations",
    icon: ClipboardCheck,
  },
  {
    name: "Compétences",
    href: "/skills",
    icon: Brain,
  },
  {
    name: "Candidatures",
    href: "/applications",
    icon: FileText,
  },
  {
    name: "Avances (Massrouf)",
    href: "/massrouf",
    icon: DollarSign,
  },
];

export const Sidebar = () => {
  return (
    <div className="w-64 bg-white border-r h-screen">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-primary">GRH</h2>
      </div>
      <nav className="space-y-1 px-3">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center px-3 py-2 rounded-md text-sm font-medium ${
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-gray-600 hover:bg-gray-100"
              }`
            }
          >
            <item.icon className="mr-3 h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};
