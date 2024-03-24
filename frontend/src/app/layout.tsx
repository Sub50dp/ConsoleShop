import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Console",
  description: "Інтернет-магазин, котрий містить список ретро товарів з рекомендаціями та описом. Купівля типів товарів: вживаних, нових ретро товарів зі складів, нові репліки ретро товарів та сучасні товари.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="uk">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
