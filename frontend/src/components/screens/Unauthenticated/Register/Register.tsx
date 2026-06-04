import { useState } from "react";
import { register } from "../../../../api/authService";
import * as route from "../../../../constants/routes";

export default function Register() {
    const [name, setName] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [passwordConfirmation, setPasswordConfirmation] = useState<string>('');
    const [phoneNumber, setPhoneNumber] = useState<string>('');
    
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setIsLoading(true);

        try {
            const data = await register(name, email, password, passwordConfirmation, phoneNumber);
            
            if (data) {
                setMessage("We have sent an account activation link to your email address.")
            } else {
                setErrorMessage('Registration failed. Please try again.');
            };
        } catch(error) {
            let message;
            if (error instanceof Error) message = error.message;
            else message = String(error);
            reportError({ message });
        } finally {
            setIsLoading(false);
        };
    };

    return (
        <div className="flex h-screen items-center justify-center px-4 py-12 bg-[#09090b] text-white">
            <div className="w-full max-w-md p-8 rounded-3xl border border-gray-600 bg-[#0d0d10] shadow-2xl">
                <div className="text-[#4f46e5]"><a href={route.HOME}>{"<- Back"}</a></div>
                <div className="mb-8 text-center">
                    <h2 className="text-3xl font-semibold tracking-tight">Create an account</h2>
                    <p className="mt-2 text-sm text-neutral-400">Get started with your ParcelLocker account</p>
                </div>
                {errorMessage && (
                    <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                        {errorMessage}
                    </div>
                )}

                {message && (
                    <div className="mb-6 p-4 rounded-xl bg-green-500/10 border border-red-500/20 text-green-400 text-sm text-center">
                        {message}
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
                    <div>
                        <label className="block text-sm font-medium text-neutral-300 mb-1.5" htmlFor="password">Password Confirmation</label>
                        <input id="password" type="password" required value={passwordConfirmation} onChange={(e) => setPasswordConfirmation(e.target.value)}
                            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-[#141417] text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent transition-all duration-200"
                            placeholder="••••••••" disabled={isLoading} />
                    </div>
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full mt-2 bg-[#4f46e5] hover:bg-[#4338ca] disabled:bg-[#4f46e5]/50 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-full transition-colors duration-200 shadow-lg shadow-indigo-600/20 flex justify-center items-center"
                    >
                        Sign up
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-400">
                    Already have an account?{" "}
                    <a href={route.LOGIN} className="text-[#4f46e5] hover:underline font-medium">Log in</a>
                </p>
            </div>
        </div>
    )
}