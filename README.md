# hr-management-system

## Project Overview
This project is a comprehensive Human Resources Management System (HRMS) designed to streamline and automate various HR processes within an organization. The application is built using Django for the backend and Vue.js with TypeScript for the frontend.

## Features
- **Employee Management**: Manage employee records, including personal information, contracts, and payroll.
- **Leave Management**: Track and manage employee leave requests and balances.
- **Payroll Management**: Calculate and manage employee salaries, including deductions and bonuses.
- **Recruitment Management**: Streamline the recruitment process, from posting job openings to tracking applications.
- **Reporting and Analytics**: Generate reports and dashboards for better decision-making.

## Project Structure
```
hr-management-system
├── backend
│   ├── api
│   ├── config
│   ├── core
│   ├── manage.py 
│   └── requirements.txt
└── frontend
    ├── src
    ├── package.json
    ├── tsconfig.json
    └── vite.config.ts
```

## Getting Started

### Backend Setup
1. Navigate to the `backend` directory.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations to set up the database:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install the required packages:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.