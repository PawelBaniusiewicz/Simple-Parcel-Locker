import { Link, useNavigate } from "react-router";
import * as route from '../../constants/routes.ts';
import { useAuth } from "../../hooks/useAuth.ts";
import apiClient from "../../api/apiClient.ts";

export default function TopBar(){
    const { isAuthenticated, checkAuthStatus, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await apiClient.post(`${import.meta.env.VITE_APP_BASE_API_URL}${route.LOGOUT}`);
            checkAuthStatus();
            navigate(route.HOME);
        } catch (error) {
            console.error("Error while logging out", error);
        }
    };

    return (
        <header className="bg-black w-[95vw] md:w-[80vw] lg:w-[70vw] h-12 flex items-center rounded-[1vw] m-4 text-white text-center border border-solid border-gray-500">
            <div className="w-[40vw] md:w-[20vw] lg:w-[15vw]">ParcelLocker</div>
            <div className="w-full h-full flex flex-row items-center justify-end">
                {!isAuthenticated ? (
                    <>
                        <div className="hidden md:block md:w-[15vw] lg:w-[15vw]">
                            <Link to={route.MY_PACKAGES}>My packages</Link>
                        </div>
                        <div className="hidden md:block md:w-[20vw] lg:w-[20vw]">
                            <Link to={route.PICK_UP_PARCEL}>Pick up your packages</Link>
                        </div>
                        <div className="w-[20vw] md:w-[10vw] lg:w-[10vw">
                            <Link to={route.LOGIN}>Log in</Link>
                        </div>
                        <div className="w-[20vw] md:w-[10vw] bg-indigo-600 text-white rounded-2xl mr-2 hover:bg-indigo-500">
                            <Link to={route.REGISTER}><div className="w-full rounded-2xl">Sign up</div></Link>
                        </div>
                    </>
                    ) : (
                    <>
                        {user?.role === 'supplier' ? (
                            <>
                                <div className="hidden md:block md:w-[10vw] lg:w-[10vw]">
                                    <Link to={route.MY_PACKAGES}>My packages</Link>
                                </div>
                                <div className="hidden md:block md:w-[15vw] lg:w-[15vw]">
                                    <Link to={route.PICK_UP_PARCEL}>Pick up your packages</Link>
                                </div>
                                <div className="md:block md:w-[15vw] lg:w-[15vw]">
                                    <Link to={route.SUPPLIER_PARCELS}>Supplier Panel</Link>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="hidden md:block md:w-[15vw] lg:w-[15vw]">
                                    <Link to={route.MY_PACKAGES}>My packages</Link>
                                </div>
                                <div className="hidden md:block md:w-[20vw] lg:w-[20vw]">
                                    <Link to={route.PICK_UP_PARCEL}>Pick up your packages</Link>
                                </div>
                            </>
                        )
                        }
                        <div className="w-[20vw] md:w-[10vw] lg:w-[10vw">
                            <button onClick={handleLogout}>Log Out</button>
                        </div>
                    </>
                    )
                }
            </div>
        </header>
    )
}