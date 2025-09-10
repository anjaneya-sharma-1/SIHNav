import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import { SpeedInsights } from "@vercel/speed-insights/next"
import { ThemeProvider } from "@/components/theme-provider"
import { Suspense } from "react"
import "./globals.css"

export const metadata: Metadata = {
  title: "SIH Navigator | Smart India Hackathon 2025 Problem Statements & Solutions",
  description: "🚀 Discover 1000+ Smart India Hackathon 2025 problem statements! Search, filter & bookmark SIH problems from 50+ ministries. Find innovation challenges in AI, healthcare, fintech, smart cities & more. Perfect for students, developers & startups preparing for SIH2025.",
  keywords: "Smart India Hackathon 2025, SIH 2025, SIH2025, hackathon problems, problem statements, innovation challenge, government hackathon, ministry problems, student competition, coding hackathon, tech solutions, startup ideas, Digital India, AI problems, healthcare tech, fintech innovation, smart cities, agriculture tech, education technology",
  authors: [{ name: "Anjaneya" }, { name: "Ishaan" }],
  creator: "Anjaneya and Ishaan",
  publisher: "SIH Navigator Team",
  generator: "Next.js",
  applicationName: "SIH Navigator",
  referrer: "origin-when-cross-origin",
  colorScheme: "light dark",
  viewport: "width=device-width, initial-scale=1",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://sih-nav.vercel.app",
    siteName: "SIH Navigator - Smart India Hackathon 2025",
    title: "SIH Navigator | 1000+ Smart India Hackathon 2025 Problem Statements",
    description: "🎯 Browse & search Smart India Hackathon 2025 problems from 50+ ministries. Filter by difficulty, technology, domain. Bookmark your favorites for SIH2025 preparation!",
    images: [
      {
        url: "https://sih-nav.vercel.app/placeholder-logo.png",
        width: 1200,
        height: 630,
        alt: "SIH Navigator - Smart India Hackathon 2025 Problem Statements Platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "SIH Navigator | Smart India Hackathon 2025 Problems & Solutions 🚀",
    description: "Discover 1000+ SIH 2025 problem statements from 50+ ministries. Perfect for students preparing for Smart India Hackathon 2025!",
    images: ["https://sih-nav.vercel.app/placeholder-logo.png"],
    creator: "@sih_navigator",
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon.ico',
    apple: '/favicon.ico',
  },
  manifest: "/site.webmanifest",
  category: "technology",
}
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "SIH Navigator - Smart India Hackathon 2025 Problem Statements",
    "alternateName": "SIH Navigator",
    "description": "Comprehensive platform to browse, search, and filter Smart India Hackathon 2025 problem statements from 50+ ministries and government organizations",
    "url": "https://sih-nav.vercel.app",
    "sameAs": [
      "https://sih.gov.in",
      "https://www.mygov.in/campaigns/smart-india-hackathon/"
    ],
    "applicationCategory": ["EducationalApplication", "ProductivityApplication"],
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript. Requires HTML5.",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "INR",
      "availability": "https://schema.org/InStock"
    },
    "author": [
      {
        "@type": "Person",
        "name": "Anjaneya"
      },
      {
        "@type": "Person", 
        "name": "Ishaan"
      }
    ],
    "publisher": {
      "@type": "Organization",
      "name": "SIH Navigator Team"
    },
    "inLanguage": "en-IN",
    "keywords": "Smart India Hackathon 2025, SIH2025, hackathon problems, government challenges, innovation competition, student hackathon, ministry problems, technology solutions, Digital India, startup ideas",
    "about": [
      {
        "@type": "Event",
        "name": "Smart India Hackathon 2025",
        "description": "India's biggest hackathon initiative bringing together students, startups, and innovators to solve pressing challenges faced by ministries and government organizations",
        "startDate": "2025",
        "location": {
          "@type": "Country",
          "name": "India"
        },
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/MixedEventAttendanceMode",
        "organizer": {
          "@type": "Organization",
          "name": "Government of India"
        }
      },
      {
        "@type": "EducationalOrganizationalCredential",
        "name": "Problem Statement Database",
        "description": "Curated collection of real-world challenges from Indian government ministries"
      }
    ],
    "mainEntity": {
      "@type": "DataCatalog",
      "name": "SIH 2025 Problem Statements Database",
      "description": "Searchable and filterable database of 1000+ Smart India Hackathon 2025 problem statements categorized by ministry, technology domain, and difficulty level",
      "keywords": "problem statements, hackathon challenges, government problems, innovation opportunities",
      "includedInDataCatalog": {
        "@type": "DataCatalog",
        "name": "Smart India Hackathon Official Problems"
      }
    },
    "featureList": [
      "Search and filter problem statements",
      "Bookmark favorite challenges",
      "Filter by difficulty level",
      "Filter by technology domain",
      "Mobile-responsive interface",
      "Real-time search results"
    ]
  }

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </head>
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <Suspense>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
            {children}
          </ThemeProvider>
        </Suspense>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
