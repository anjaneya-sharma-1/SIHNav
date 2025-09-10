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
  title: "SIH Navigator - Smart India Hackathon 2025 Problem Statements Database | AI Problems & Tech Solutions",
  description: "Official Smart India Hackathon 2025 problem statements database. Browse 1000+ AI problems, tech challenges from 50+ government ministries. Filter by difficulty, domain, technology. Perfect platform for SIH2025 preparation, hackathon projects, and innovation challenges.",
  keywords: "Smart India Hackathon, Smart India Hackathon 2025, SIH 2025, SIH2025, smart india hackathon project, smart india hackathon website, AI problem statements, AI website SIH, hackathon problems database, government hackathon challenges, ministry problem statements, student hackathon competition, coding challenges India, tech innovation problems, Digital India hackathon, startup problem statements, innovation challenges 2025, hackathon project ideas, SIH problem database, government tech challenges, AI hackathon problems, machine learning challenges, data science problems, blockchain hackathon, IoT challenges, healthcare tech problems, fintech innovation challenges, smart cities hackathon, agriculture technology problems, education tech challenges, cybersecurity hackathon problems, renewable energy challenges, transportation tech problems, e-governance solutions, digital transformation challenges, artificial intelligence competition, technology solutions India",
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
    siteName: "SIH Navigator - Smart India Hackathon 2025 Problem Statements Database",
    title: "Smart India Hackathon 2025 Problem Statements Database | AI Problems & Tech Challenges",
    description: "Official Smart India Hackathon 2025 problem statements database. Browse 1000+ AI problems, tech challenges from 50+ government ministries. Filter by difficulty, domain, technology. Perfect platform for SIH2025 preparation.",
    images: [
      {
        url: "https://sih-nav.vercel.app/placeholder-logo.png",
        width: 1200,
        height: 630,
        alt: "SIH Navigator - Smart India Hackathon 2025 Problem Statements Database",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Smart India Hackathon 2025 Problem Statements Database | AI Problems & Tech Solutions",
    description: "Official Smart India Hackathon 2025 problem statements database. Browse 1000+ AI problems, tech challenges from 50+ government ministries for SIH2025 preparation.",
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
        <meta name="description" content="Official Smart India Hackathon 2025 problem statements database. Browse 1000+ AI problems, tech challenges from 50+ government ministries. Filter by difficulty, domain, technology. Perfect platform for SIH2025 preparation, hackathon projects, and innovation challenges." />
        <meta name="keywords" content="Smart India Hackathon, Smart India Hackathon 2025, SIH 2025, SIH2025, smart india hackathon project, smart india hackathon website, AI problem statements, AI website SIH, hackathon problems database" />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta name="subject" content="Smart India Hackathon 2025 Problem Statements and Innovation Challenges" />
        <meta name="abstract" content="Comprehensive database of Smart India Hackathon 2025 problem statements for students, developers, and innovators" />
        <meta name="topic" content="Smart India Hackathon, Technology Innovation, Government Challenges" />
        <meta name="summary" content="Browse and search Smart India Hackathon 2025 problem statements. Find AI challenges, tech problems from government ministries." />
        <meta name="Classification" content="Education, Technology, Innovation, Hackathon" />
        <meta name="designer" content="Anjaneya and Ishaan" />
        <meta name="copyright" content="SIH Navigator Team" />
        <meta name="reply-to" content="team@sih-nav.vercel.app" />
        <meta name="owner" content="SIH Navigator" />
        <meta name="url" content="https://sih-nav.vercel.app" />
        <meta name="identifier-URL" content="https://sih-nav.vercel.app" />
        <meta name="directory" content="submission" />
        <meta name="category" content="Education, Technology, Innovation, Government, Hackathon" />
        <meta name="coverage" content="Worldwide" />
        <meta name="distribution" content="Global" />
        <meta name="rating" content="General" />
        <meta name="revisit-after" content="1 days" />
        <meta httpEquiv="Expires" content="0" />
        <meta httpEquiv="Pragma" content="no-cache" />
        <meta httpEquiv="Cache-Control" content="no-cache" />
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
