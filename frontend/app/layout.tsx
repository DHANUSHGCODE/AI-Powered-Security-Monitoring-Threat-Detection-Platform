import './globals.css';

export const metadata = {
    title: 'AI Security Monitor',
    description: 'Advanced UI Dashboard',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <head />
            <body className="bg-gray-900 text-white font-sans">
                {children}
            </body>
        </html>
    );
}
