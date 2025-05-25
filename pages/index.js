// pages/index.js
import { useSession, signIn, signOut } from "next-auth/react";

export default function Home() {
  const { data: session } = useSession();

  if (session) {
    return (
      <main style={{ padding: '2rem' }}>
        <h1>Welcome, {session.user.name}</h1>
        <p>Email: {session.user.email}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </main>
    );
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>AI Tutor Login</h1>
      <p>Please sign in to access the AI Tutor.</p>
      <button onClick={() => signIn()}>Sign in</button>
    </main>
  );
}
