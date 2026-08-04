import { useState } from "react"
import { useNavigate } from "react-router";
import { pickUpParcel } from "../../../../../api/parcelService";
import { MY_PACKAGES } from "../../../../../constants/routes.ts";

export default function PickUpParcel(){
    const [code, setCode] = useState<string>("");
    const [phoneNumber, setPhoneNumber] = useState<string>("");

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [isSuccess, setIsSuccess] = useState<boolean>(false);

    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setIsLoading(true);

        try {
            const data = await pickUpParcel(code, phoneNumber);

            if (data) {
                setIsSuccess(true);
            } else {
                setErrorMessage('The pickup failed. Incorrect verification code or phone number. Please try again.');
            }
        } catch(error) {
            let message;
            if (error instanceof Error) message = error.message;
            else message = String(error);
            reportError({ message });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <div className="flex h-screen items-center justify-center px-4 py-12 bg-[#09090b] text-white mt-[-10vh]">
                <div className="w-full max-w-md p-8 rounded-3xl border border-gray-600 bg-[#0d0d10] shadow-2xl">
                    {isSuccess ? (
                        <div className="text-center space-y-6">
                            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-500/10 text-emerald-400 mb-2">
                                <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            </div>
                            <div>
                                <h2 className="text-3xl font-semibold tracking-tight text-white">Success!</h2>
                                <p className="text-neutral-400 mt-3 text-sm leading-relaxed">
                                    Your package has been successfully picked up. The locker is now open. Don't forget to close the door!
                                </p>
                            </div>
                            <button
                                onClick={() => navigate(MY_PACKAGES)}
                                className="w-full mt-4 bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 shadow-lg shadow-emerald-900/20 flex justify-center items-center"
                            >
                                Go to My Packages
                            </button>
                        </div>
                    ) : (
                        <>
                            <div className="mb-8 text-center">
                                <h2 className="text-3xl font-semibold tracking-tight">Pick up your package</h2>
                            </div>
                            {errorMessage && (
                                <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                                    {errorMessage}
                                </div>
                            )}
                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="code">Enter pickup code:</label>
                                    <input id="code" type="text" required value={code} onChange={(e) => setCode(e.target.value)}
                                           className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                                           placeholder="123456" disabled={isLoading} />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="phone">Phone Number</label>
                                    <input id="phone" type="tel" required value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)}
                                           className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                                           placeholder="+48 123 456 789" disabled={isLoading} />
                                </div>
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="w-full mt-2 bg-[#4f46e5] hover:bg-[#4338ca] disabled:bg-[#4f46e5]/50 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 shadow-lg shadow-indigo-600/20 flex justify-center items-center"
                                >
                                    Submit
                                </button>
                            </form>
                        </>
                    )}
                </div>
            </div>
        </>
    )
}