import './index.css'
import TopBar from './components/TopBar/TopBar'
import { Outlet } from 'react-router'

function App() {

  return (
    <div className="w-full h-screen bg-[#09090b]">
      <div className='w-full flex justify-center'><TopBar /></div>
        <Outlet />
    </div>
  )
}

export default App
