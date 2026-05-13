import TopBar from "../TopBar/TopBar"
import { useState } from "react"

export default function PickUpPackage(){
    const [code, setCode] = useState<string>("");
    const [phoneNumber, setPhoneNumber] = useState<string>("");


    return (
        <>
            <div className='w-full flex justify-center'><TopBar /></div>
            <div className="w-full h-auto flex justify-center">
                <div className="bg-black w-[95vw] md:w-[80vw] lg:w-[70vw] rounded-xl">
                    <form className="flex flex-col text-white text-2xl">
                        <label className="flex gap-4 m-4">
                            Enter pickup code:
                            <input 
                                type="text" 
                                className="border border-solid border-white "
                                value={code}
                                onChange={e => setCode(e.target.value)}/>
                        </label>
                        <label className="flex gap-4 m-4">
                            Enter phone number:
                            <input type="text" 
                                className="border border-solid border-white"
                                value={phoneNumber}
                                onChange={e => setPhoneNumber(e.target.value)}/>
                        </label>
                        <input type="submit" className="border border-solid border-white w-[10vw] m-4 hover:bg-white hover:text-black" />
                    </form>
                </div>
            </div>
        </>
    )
}