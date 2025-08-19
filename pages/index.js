// pages/index.js
import { useSession, signIn } from "next-auth/react";
import { useRouter } from "next/router";
import { useEffect } from "react";
import styles from '../styles/Home.module.css';

export default function Home() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "authenticated") {
      router.push('/tutor');
    }
  }, [status, router]);

  if (status === "loading" || status === "authenticated") {
    return <div className={styles.loading}>Loading...</div>;
  }

  return (
    <main className={styles.main}>
      <div className={styles.loginBox}>
        <h1 className={styles.title}>Welcome to the AI Tutor</h1>
        <p className={styles.subtitle}>Sign in to begin your personalized learning journey.</p>
        <button onClick={() => signIn()} className={styles.signInButton}>
          Sign In
        </button>
      </div>
    </main>
  );
}
