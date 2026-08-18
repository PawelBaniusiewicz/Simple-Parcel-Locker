import './index.css'
import TopBar from './components/TopBar/TopBar'
import { Outlet } from 'react-router'
import ParcelLockerMap from "./components/Map/ParcelLockersMap/ParcelLockersMap.tsx";

function App() {

  return (
    <div className="w-full h-screen bg-[#09090b]">
      <div className='w-full flex justify-center'><TopBar /></div>
        <ParcelLockerMap />
        <Outlet />
    </div>
  )
}

export default App
