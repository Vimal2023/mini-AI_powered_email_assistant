"use client";
import api from "../api/axios";

export default function LoginPage() {
  const googleLogin = async () => {
    const res = await api.get("/auth/google/login-url");
    window.location.href = res.data.url;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-500 to-indigo-600 px-4">
      <div className="bg-white shadow-2xl rounded-xl p-8 max-w-md w-full border">
        <h1 className="text-xl font-bold mb-3 text-center text-blue-600">
          Constructure AI – Email Assistant
        </h1>
        <p className="text-sm text-gray-600 mb-6 text-center">
          Sign in with Google to manage your Gmail using AI.
        </p>

        <button
          onClick={googleLogin}
          className="w-full flex items-center justify-center gap-2 border rounded-lg py-2 text-sm font-medium bg-gray-100 text-black cursor-pointer
 hover:bg-gray-200 transition shadow active:scale-95"
        >
          Continue with Google
        </button>
      </div>
    </div>
  );
}
