import { useState } from "react"
import { register } from "../../../../api/authService";
import { useNavigate } from "react-router";

export default function Register() {
    const [name, setName] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [phoneNumber, setPhoneNumber] = useState<string>('');
    
    // Nowe stany do obsługi UX
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setIsLoading(true);

        try {
            const data = await register(name, email, password, phoneNumber);
            
            if (data) {
                navigate('/');
            } else {
                setErrorMessage('Registration failed. Please try again.');
            }
        } catch(error) {
            let message
            if (error instanceof Error) message = error.message
            else message = String(error)
            reportError({ message })
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-12 bg-[#09090b] text-white">
            <div className="w-full max-w-md p-8 rounded-3xl border border-neutral-800 bg-[#0d0d10] shadow-2xl">
                
                <div className="mb-8 text-center">
                    <h2 className="text-3xl font-semibold tracking-tight">Create an account</h2>
                    <p className="mt-2 text-sm text-neutral-400">Get started with your ParcelLocker account</p>
                </div>
                {errorMessage && (
                    <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                        {errorMessage}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="name">Name</label>
                        <input id="name" type="text" required value={name} onChange={(e) => setName(e.target.value)}
                            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                            placeholder="John Doe" disabled={isLoading} />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="email">Email Address</label>
                        <input id="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                            placeholder="name@example.com" disabled={isLoading} />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="phone">Phone Number</label>
                        <input id="phone" type="tel" required value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)}
                            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                            placeholder="+48 123 456 789" disabled={isLoading} />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="password">Password</label>
                        <input id="password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                            placeholder="••••••••" disabled={isLoading} />
                    </div>
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full mt-2 bg-[#4f46e5] hover:bg-[#4338ca] disabled:bg-[#4f46e5]/50 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 shadow-lg shadow-indigo-600/20 flex justify-center items-center"
                    >
                        {isLoading ? (
                            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        ) : (
                            "Sign up"
                        )}
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-400">
                    Already have an account?{" "}
                    <a href="/login" className="text-[#4f46e5] hover:underline font-medium">Log in</a>
                </p>
            </div>
        </div>
    )
}