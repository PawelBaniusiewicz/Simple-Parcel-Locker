import { Link } from "react-router"
import * as route from '../../constants/routes.ts'

export default function TopBar(){
    return (
        <header className="bg-black w-[95vw] md:w-[80vw] lg:w-[70vw] h-12 flex items-center rounded-[1vw] m-4 text-white text-center border border-solid border-gray-500">
            <div className="w-[40vw] md:w-[20vw] lg:w-[15vw]">ParcelLocker</div>
            <div className="w-full h-full flex flex-row items-center justify-end">
                <div className="hidden md:block md:w-[15vw] lg:w-[15vw]">
                    <Link to={route.MY_PACKAGES}>My packages</Link>
                </div>
                <div className="hidden md:block md:w-[20vw] lg:w-[20vw]">
                    <Link to={route.PICK_UP_PACKAGE}>Pick up your packages</Link>
                </div>
                <div className="w-[20vw] md:w-[10vw] lg:w-[10vw">
                    <Link to={route.LOGIN}>Log in</Link>
                </div>
                <div className="w-[20vw] md:w-[10vw] bg-indigo-600 text-white rounded-2xl mr-2 hover:bg-indigo-500">
                    <Link to={route.REGISTER}>Sign up</Link>
                </div>
            </div>
        </header>
    )
}