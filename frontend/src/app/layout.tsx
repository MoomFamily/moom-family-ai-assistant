import type { Metadata } from 'next';
import './style.css';
export const metadata: Metadata = { title: 'AI Assistant', description: 'A standalone AI assistant' };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html>; }
