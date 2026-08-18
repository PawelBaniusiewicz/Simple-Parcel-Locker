import { NavLink, Outlet } from 'react-router';
import { useAuth } from "../../../../../hooks/useAuth.ts";
import * as routes from '../../../../../constants/routes.ts'

export default function AdminDashboard() {
    const { user } = useAuth();

    return (
        <div className="flex h-screen bg-gray-50 font-sans">
            <aside className="w-64 bg-slate-800 text-white flex flex-col shadow-xl z-20">
                <div className="p-6 text-center border-b border-slate-700">
                    <h1 className="text-2xl font-black tracking-wider text-blue-400">ADMIN PANEL</h1>
                    <p className="text-xs text-slate-400 mt-1">System Management</p>
                </div>

                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavLink
                        to={routes.ADMIN_PARCEL_LOCKERS}
                        className={({ isActive }) =>
                            `flex items-center px-4 py-3 rounded-lg transition-colors ${
                                isActive
                                    ? 'bg-blue-600 text-white font-medium shadow-md'
                                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                            }`
                        }
                    >
                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                        Parcel Lockers (Map)
                    </NavLink>
                    <NavLink
                        to="/admin/users"
                        className={({ isActive }) =>
                            `flex items-center px-4 py-3 rounded-lg transition-colors ${
                                isActive
                                    ? 'bg-blue-600 text-white font-medium shadow-md'
                                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                            }`
                        }
                    >
                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                        Users
                    </NavLink>
                </nav>

                <div className="p-4 border-t border-slate-700">
                    <NavLink to={routes.HOME} className="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-slate-300 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                        Back to home page
                    </NavLink>
                </div>
            </aside>
            <main className="flex-1 flex flex-col overflow-hidden relative">
                <header className="bg-white shadow-sm border-b border-gray-200 z-10 px-8 py-4 flex justify-between items-center">
                    <h2 className="text-xl font-semibold text-gray-800">Management Panel</h2>
                    <div className="flex items-center text-sm text-gray-600">
                        Logged as: <span className="font-bold ml-1 text-blue-600">{user?.email || 'Admin'}</span>
                    </div>
                </header>
                <div className="flex-1 overflow-auto bg-gray-100">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}