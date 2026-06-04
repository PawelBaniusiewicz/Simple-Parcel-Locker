import { useSearchParams } from "react-router"
import { useState, useEffect, useRef } from "react";
import apiClient from "../../../../../api/apiClient";
import * as routes from "../../../../../constants/routes"
import { Link } from "react-router";

export default function ActivateAccount() {
    const [ searchParams ]  = useSearchParams();
    const token = searchParams.get('token');
    const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
        token ? 'loading' : 'error'
    );
    const hasFetched = useRef(false);

    useEffect(() => {
        if (!token) return;
        if (hasFetched.current) return;
        const sendToken = async () => {
            hasFetched.current = true;
            try {
                const response = await apiClient.post(`${import.meta.env.VITE_APP_BASE_API_URL}${routes.ACTIVATE_ACCOUNT}`, {token});
                if (response.status === 200) {
                    setStatus('success');
                }
            } catch(error) {
                setStatus('error')
                let message;
                if (error instanceof Error) message = error.message;
                else message = String(error);
                reportError({ message });
            };
        }
        sendToken();
    }, [token]);

    return (
        <div className="flex h-screen items-center justify-center px-4 py-12 bg-[#09090b] text-white">
            <div className="w-full max-w-md p-8 rounded-3xl border border-neutral-800 bg-[#0d0d10]">
                {status === 'loading' && (
                    <div className="flex flex-col items-center text-center py-6">
                        <svg className="animate-spin h-12 w-12 text-[#4f46e5] mb-6" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <h2 className="text-2xl font-semibold tracking-tight mb-2">Activating Account...</h2>
                        <p className="text-sm text-neutral-400">Please wait while we verify your token.</p>
                    </div>
                )}
                {status === 'success' && (
                    <div className="flex flex-col items-center text-center">
                        <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mb-6 border border-green-500/20">
                            <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                        <h2 className="text-3xl font-semibold tracking-tight mb-2">Account Activated</h2>
                        <p className="text-sm text-neutral-400 mb-8">
                            Your email has been successfully verified. You can now access all features of ParcelLocker.
                        </p>
                        <Link 
                            to={routes.LOGIN} 
                            className="w-full text-center bg-[#4f46e5] hover:bg-[#4338ca] text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 shadow-lg shadow-indigo-600/20 block"
                        >
                            Go to Login
                        </Link>
                    </div>
                )}
                {status === 'error' && (
                    <div className="flex flex-col items-center text-center">
                        <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mb-6 border border-red-500/20">
                            <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </div>
                        <h2 className="text-3xl font-semibold tracking-tight mb-2">Activation Failed</h2>
                        <p className="text-sm text-neutral-400 mb-8">
                            The activation link is invalid or has expired. Please try registering again or request a new link.
                        </p>
                        <Link 
                            to={routes.REGISTER} 
                            className="w-full text-center bg-neutral-800 hover:bg-neutral-700 text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 block"
                        >
                            Back to Sign Up
                        </Link>
                    </div>
                )}
            </div>
        </div>
    )
}