import "../styles/globals.css";

export const metadata = {
  title: "NMAP MASTER - OSINT with Tejo Manasa",
  description: "Interactive safe Nmap training simulator",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
