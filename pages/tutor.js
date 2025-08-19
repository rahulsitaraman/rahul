// pages/tutor.js
import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/router";
import { useChat } from 'ai/react';
import styles from '../styles/Tutor.module.css';
import { FiSend, FiLogOut } from 'react-icons/fi';
import { useEffect } from "react";

export default function Tutor() {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  const { messages, input, handleInputChange, handleSubmit } = useChat({
      api: '/api/chat',
  });

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push('/');
    }
  }, [status, router]);

  if (status === "loading") {
    return <div className={styles.loading}>Loading...</div>;
  }
  
  if (!session) {
    return null; // or a redirect component
  }

  return (
    <div className={styles.chatContainer}>
      <header className={styles.header}>
        <div className={styles.userInfo}>
            Welcome, {session.user.name}
        </div>
        <button onClick={() => signOut()} className={styles.signOutButton}>
            <FiLogOut /> Sign Out
        </button>
      </header>
      
      <div className={styles.messagesList}>
        {messages.length === 0 && (
            <div className={styles.emptyState}>
                <h2>Personalized AI Tutor</h2>
                <p>Ask me anything about your subjects, and I'll help you learn!</p>
            </div>
        )}
        {messages.map(m => (
          <div key={m.id} className={`${styles.message} ${m.role === 'user' ? styles.userMessage : styles.aiMessage}`}>
            <div className={styles.messageContent}>
                {m.content}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <input
          className={styles.chatInput}
          value={input}
          onChange={handleInputChange}
          placeholder="Ask a question about any topic..."
        />
        <button type="submit" className={styles.sendButton}>
          <FiSend />
        </button>
      </form>
    </div>
  );
}
