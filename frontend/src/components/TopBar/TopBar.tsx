import { Link } from "react-router"
import * as route from '../../constants/routes.ts'

export default function TopBar(){
    return (
        <header className="bg-[#c5b7c9] w-full h-14">
            <div>ParcelLocker</div>
            <div>
                <Link to={route.MY_PACKAGES}>My packages</Link>
                <Link to={route.ORDER_PACKAGE}>Order your Packages</Link>
            </div>
        </header>
    )
}