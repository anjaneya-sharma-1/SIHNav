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
  title: "SIH Navigator | How to Win SIH 2025 | Smart India Hackathon Problem Statements Guide | Tips & Strategies",
  description: "Learn how to win Smart India Hackathon 2025! Find the correct problem statements, get winning tips, participation guide, and strategies. Browse 1000+ curated SIH problems with difficulty filters. Complete guide for students on how to participate in SIH, choose right problems, and build winning solutions.",
  keywords: "how to win SIH, how to win Smart India Hackathon, how to find correct problem statement for smart india hackathon, how to find correct problem statement for SIH, how to participate in Smart India Hackathon, how to participate in SIH 2025, SIH winning tips, Smart India Hackathon tips, how to choose SIH problem statement, SIH participation guide, Smart India Hackathon guide, how to prepare for SIH, SIH strategy, Smart India Hackathon strategy, how to select problem statement SIH, SIH problem selection tips, how to win hackathon, Smart India Hackathon winning strategies, SIH 2025 tips, how to find best problem statement, SIH problem finding guide, how to participate Smart India Hackathon 2025, SIH registration guide, Smart India Hackathon preparation tips, how to build winning solution SIH, SIH team formation tips, how to get selected in SIH, Smart India Hackathon selection criteria, SIH judging criteria, how to present SIH solution, Smart India Hackathon presentation tips, SIH project ideas, how to implement SIH solution, Smart India Hackathon implementation guide, SIH technology stack, how to choose technology for SIH, Smart India Hackathon tech guide",
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
    siteName: "SIH Navigator - How to Win Smart India Hackathon 2025",
    title: "How to Win SIH 2025 | Smart India Hackathon Guide & Problem Statements",
    description: "Complete guide on how to win Smart India Hackathon 2025! Learn how to find the correct problem statements, winning tips, participation strategies, and browse 1000+ curated SIH problems with expert guidance.",
    images: [
      {
        url: "https://sih-nav.vercel.app/placeholder-logo.png",
        width: 1200,
        height: 630,
        alt: "How to Win Smart India Hackathon 2025 - Complete Guide & Problem Statements",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "How to Win Smart India Hackathon 2025 | Complete SIH Guide & Tips",
    description: "Learn how to win SIH 2025! Complete guide on finding correct problem statements, participation tips, winning strategies. Browse 1000+ curated problems with expert guidance.",
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
    "@type": ["WebApplication", "HowTo"],
    "name": "How to Win Smart India Hackathon 2025 - SIH Navigator Guide",
    "alternateName": "SIH Navigator",
    "description": "Complete guide on how to win Smart India Hackathon 2025, find correct problem statements, participation tips, and winning strategies. Browse 1000+ curated SIH problems with expert guidance.",
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
    "mainEntity": [
      {
        "@type": "DataCatalog",
        "name": "SIH 2025 Problem Statements Database",
        "description": "Searchable and filterable database of 1000+ Smart India Hackathon 2025 problem statements categorized by ministry, technology domain, and difficulty level",
        "keywords": "problem statements, hackathon challenges, government problems, innovation opportunities"
      },
      {
        "@type": "Question",
        "name": "How to win Smart India Hackathon 2025?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "To win SIH 2025: 1) Choose problems matching your technical skills, 2) Focus on user experience and practical implementation, 3) Build a working prototype, 4) Prepare compelling presentations, 5) Research the problem domain thoroughly, 6) Show real-world impact and scalability."
        }
      },
      {
        "@type": "Question",
        "name": "How to find the correct problem statement for Smart India Hackathon?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Find correct SIH problem statements by: 1) Analyzing your team's technical expertise, 2) Using difficulty filters (Easy/Medium/Hard), 3) Choosing domains matching your interests, 4) Considering implementation feasibility, 5) Looking for clear evaluation criteria and measurable outcomes."
        }
      },
      {
        "@type": "Question",
        "name": "How to participate in Smart India Hackathon 2025?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "To participate in SIH 2025: 1) Form a 6-member team with mentor, 2) Register on official SIH portal, 3) Select problem statements, 4) Submit solution proposals, 5) Participate in internal hackathon, 6) Qualify for grand finale through regional selection."
        }
      }
    ],
    "featureList": [
      "Learn how to win Smart India Hackathon",
      "Find correct problem statements guide",
      "SIH participation tips and strategies",
      "Problem difficulty and selection filters",
      "Winning solution examples and tips",
      "Complete SIH preparation guide"
    ]
  }

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="description" content="Learn how to win Smart India Hackathon 2025! Find the correct problem statements, get winning tips, participation guide, and strategies. Browse 1000+ curated SIH problems with difficulty filters. Complete guide for students on how to participate in SIH, choose right problems, and build winning solutions." />
        <meta name="keywords" content="how to win SIH, how to win Smart India Hackathon, how to find correct problem statement for smart india hackathon, how to participate in SIH 2025, SIH winning tips, Smart India Hackathon guide, how to choose SIH problem statement" />
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
