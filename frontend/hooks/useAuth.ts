"use client";

import { useEffect, useState } from "react";
import api from "../app/api/axios";
import { UserSession } from "../lib/session";
import { useRouter } from "next/navigation";

export const useAuth = (redirectIfUnauthed: boolean = true) => {
  const [user, setUser] = useState<UserSession | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    api
      .get("/auth/me")
      .then((res) => {
        setUser(res.data);
      })
      .catch(() => {
        setUser(null);
        if (redirectIfUnauthed) {
          router.push("/login");
        }
      })
      .finally(() => setLoading(false));
  }, [redirectIfUnauthed, router]);

  return { user, loading };
};
