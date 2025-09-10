"use client"

import { useState, useEffect, useMemo } from "react"
import { SearchBar } from "@/components/search-bar"
import { Sidebar } from "@/components/sidebar"
import { ProblemCard } from "@/components/problem-card"
import { ThemeToggle } from "@/components/theme-toggle"
import { BookmarksView } from "@/components/bookmarks-view"
import { useIsMobile } from "@/hooks/use-mobile"
import {
  sampleProblems,
  fuzzySearch,
  filterByTags,
  getAllTags,
  sortProblems,
  type ProblemStatement,
} from "@/lib/search"
import { Button } from "@/components/ui/button"
import { Sparkles, Trophy, Users, Filter, Bookmark } from "lucide-react"

export default function HomePage() {
  const isMobile = useIsMobile()
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [filteredProblems, setFilteredProblems] = useState<ProblemStatement[]>(sampleProblems)
  const [sortBy, setSortBy] = useState<"relevance" | "submissions_high" | "submissions_low">("relevance")
  const [sidebarOpen, setSidebarOpen] = useState(false) // Will be set properly in useEffect
  const [currentView, setCurrentView] = useState<"search" | "bookmarks">("search")

  const submissionCounts = sampleProblems.map((p) => p.submission_count || 0)
  const minSubmissions = Math.min(...submissionCounts)
  const maxSubmissions = Math.max(...submissionCounts)
  const [submissionRange, setSubmissionRange] = useState<[number, number]>([minSubmissions, maxSubmissions])

  const allTags = useMemo(() => getAllTags(sampleProblems), [])

  // Update sidebar state based on mobile status
  useEffect(() => {
    if (isMobile !== undefined) {
      setSidebarOpen(!isMobile)
    }
  }, [isMobile])

  const handleSearch = () => {
    let results = fuzzySearch(searchQuery, sampleProblems)
    results = filterByTags(results, selectedTags)

    results = results.filter((problem) => {
      const submissions = problem.submission_count || 0
      return submissions >= submissionRange[0] && submissions <= submissionRange[1]
    })

    results = sortProblems(results, sortBy)
    setFilteredProblems(results)
  }

  const handleTagToggle = (tag: string) => {
    setSelectedTags((prev) => (prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]))
  }

  useEffect(() => {
    handleSearch()
  }, [searchQuery, selectedTags, sortBy, submissionRange])

  if (currentView === "bookmarks") {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <BookmarksView onBack={() => setCurrentView("search")} />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        availableTags={allTags}
        selectedTags={selectedTags}
        onTagToggle={handleTagToggle}
        minSubmissions={minSubmissions}
        maxSubmissions={maxSubmissions}
        submissionRange={submissionRange}
        onSubmissionRangeChange={setSubmissionRange}
        sortBy={sortBy}
        onSortChange={setSortBy}
      />

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? "lg:ml-80" : "ml-0"}`}>
        {/* Header */}
        <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-30">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
            <div className="flex justify-between items-center mb-3 sm:mb-4">
              <Button
                variant="ghost"
                onClick={() => setCurrentView("bookmarks")}
                className="flex items-center gap-2 text-sm px-2 sm:px-3"
              >
                <Bookmark className="h-4 w-4" />
                <span className="hidden sm:inline">Bookmarks</span>
                <span className="sm:hidden">Saved</span>
              </Button>
              <ThemeToggle />
            </div>
            <div className="text-center space-y-1 sm:space-y-2">
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
                <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-foreground">Smart India Hackathon 2025</h1>
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground text-balance px-2">
                Discover innovative problem statements and build solutions for India's future
              </p>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-6 sm:py-8 lg:py-12 bg-gradient-to-b from-primary/5 to-background">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center space-y-4 sm:space-y-6 lg:space-y-8">
              <div className="space-y-2 sm:space-y-4">
                <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground text-balance px-2">
                  Stop <span className="text-red-500 italic">Scrolling</span>. Start{" "}
                  <span className="text-green-500 italic">Winning</span>
                </h2>
                <p className="text-sm sm:text-base lg:text-lg text-muted-foreground max-w-2xl mx-auto text-pretty px-4">
                  Search through curated problem statements from various ministries and domains. Use our intelligent
                  search to find challenges that match your skills and interests.
                </p>
              </div>

              {/* Search Bar and Filter Toggle */}
              <div className="space-y-3 sm:space-y-4 px-4">
                <SearchBar value={searchQuery} onChange={setSearchQuery} onSearch={handleSearch} />

                {!sidebarOpen && (
                  <Button
                    variant="outline"
                    onClick={() => setSidebarOpen(true)}
                    className="flex items-center gap-2 text-sm w-full sm:w-auto"
                  >
                    <Filter className="h-4 w-4" />
                    Show Filters & Sort
                  </Button>
                )}
              </div>

              {/* Stats */}
              <div className="flex items-center justify-center gap-3 sm:gap-6 lg:gap-8 text-xs sm:text-sm text-muted-foreground flex-wrap px-4">
                <div className="flex items-center gap-1 sm:gap-2">
                  <Trophy className="h-3 w-3 sm:h-4 sm:w-4" />
                  <span>{sampleProblems.length} Problems</span>
                </div>
                <div className="flex items-center gap-1 sm:gap-2">
                  <Users className="h-3 w-3 sm:h-4 sm:w-4" />
                  <span>Multiple Domains</span>
                </div>
                <div className="flex items-center gap-1 sm:gap-2">
                  <Sparkles className="h-3 w-3 sm:h-4 sm:w-4" />
                  <span>AI-Powered Search</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Results Section */}
        <section className="py-4 sm:py-6 lg:py-8">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 space-y-4 sm:space-y-6 lg:space-y-8">
            {/* Results Header */}
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="space-y-1">
                <h3 className="text-lg sm:text-xl font-semibold text-foreground">Problem Statements</h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  {filteredProblems.length} result{filteredProblems.length !== 1 ? "s" : ""} found
                  {searchQuery && ` for "${searchQuery}"`}
                </p>
              </div>
            </div>

            {/* Results Grid */}
            {filteredProblems.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4 sm:gap-5 lg:gap-6">
                {filteredProblems.map((problem) => (
                  <ProblemCard key={problem.ps_id} problem={problem} searchQuery={searchQuery} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 sm:py-12 space-y-4 px-4">
                <div className="text-3xl sm:text-4xl">🔍</div>
                <h3 className="text-base sm:text-lg font-medium text-foreground">No problems found</h3>
                <p className="text-sm text-muted-foreground">
                  Try adjusting your search query or removing some filters
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Hidden SEO Content for Better Indexing */}
        <div className="sr-only">
          <h2>How to Win Smart India Hackathon 2025 - Complete Guide</h2>
          <p>Learn how to win Smart India Hackathon 2025 with our comprehensive guide! This platform provides everything you need to know about participating in SIH, finding the correct problem statements, and building winning solutions.</p>
          
          <h3>How to Find the Correct Problem Statement for Smart India Hackathon</h3>
          <p>Finding the right problem statement is crucial for SIH success. Here's how to find correct problem statement for SIH: 1) Analyze your team's technical skills and expertise, 2) Review problem difficulty levels using our filters, 3) Choose domains that match your interests (AI, healthcare, fintech, etc.), 4) Consider the feasibility of implementation within the hackathon timeline, 5) Look for problems with clear evaluation criteria and measurable outcomes.</p>
          
          <h3>How to Participate in Smart India Hackathon 2025</h3>
          <p>Complete guide on how to participate in SIH 2025: 1) Form a team of 6 members (students + mentor), 2) Register on the official SIH portal during registration period, 3) Browse and select problem statements using our platform, 4) Submit your innovative solution proposal, 5) Prepare for internal hackathon at your institute, 6) Qualify for the grand finale through regional selection.</p>
          
          <h3>Smart India Hackathon Winning Tips and Strategies</h3>
          <p>Top SIH winning tips from past champions: 1) Choose problems aligned with your technical expertise, 2) Focus on user experience and practical implementation, 3) Prepare a compelling presentation and demo, 4) Research the problem domain thoroughly, 5) Build a minimum viable product (MVP), 6) Practice your pitch multiple times, 7) Show real-world impact and scalability, 8) Demonstrate technical innovation and creativity.</p>
          
          <h3>How to Choose the Right SIH Problem Statement</h3>
          <p>Expert guide on how to choose SIH problem statement: 1) Assess problem complexity vs. team capabilities, 2) Use our difficulty filters (Easy, Medium, Hard), 3) Consider available technology stack and resources, 4) Evaluate market potential and social impact, 5) Check if similar solutions already exist, 6) Ensure problem aligns with your career goals, 7) Review past winning solutions for insights.</p>
          
          <h3>SIH Preparation and Strategy Guide</h3>
          <p>How to prepare for SIH 2025: 1) Start early with problem analysis, 2) Build prototypes and test concepts, 3) Create detailed project timeline, 4) Prepare backup solutions for technical challenges, 5) Practice presentation skills, 6) Study judging criteria and evaluation parameters, 7) Network with mentors and industry experts, 8) Keep updated with latest technology trends.</p>
          
          <h3>Smart India Hackathon Team Formation Tips</h3>
          <p>SIH team formation tips for success: 1) Include diverse skill sets (frontend, backend, AI/ML, design, business), 2) Choose committed and reliable team members, 3) Select an experienced mentor from industry or academia, 4) Ensure good communication and collaboration, 5) Define clear roles and responsibilities, 6) Practice working together on smaller projects first.</p>
          
          <h3>How to Build Winning Solutions for SIH</h3>
          <p>Steps to build winning SIH solutions: 1) Conduct thorough problem research and user analysis, 2) Design user-centric and innovative solutions, 3) Choose appropriate technology stack, 4) Focus on scalability and real-world implementation, 5) Create compelling demos and presentations, 6) Prepare for technical questions from judges, 7) Document your solution architecture and business model.</p>
          
          <h3>SIH Technology Selection and Implementation Guide</h3>
          <p>How to choose technology for SIH: 1) Match technology with problem requirements, 2) Consider team expertise and learning curve, 3) Evaluate development time and complexity, 4) Check for available APIs and resources, 5) Ensure technology supports scalability, 6) Consider deployment and maintenance aspects, 7) Stay updated with trending technologies like AI, blockchain, IoT.</p>
          
          <h3>Smart India Hackathon Judging Criteria and Presentation Tips</h3>
          <p>Understanding SIH judging criteria: 1) Innovation and creativity (30%), 2) Technical implementation and complexity (25%), 3) Social impact and feasibility (25%), 4) Presentation and demonstration (20%). Presentation tips: Keep it simple, focus on problem-solution fit, demonstrate live working prototype, explain technical architecture clearly, highlight unique features and benefits.</p>
          
          <h4>Complete Keywords Coverage: how to win SIH, how to win Smart India Hackathon, how to find correct problem statement for smart india hackathon, how to find correct problem statement for SIH, how to participate in Smart India Hackathon, how to participate in SIH 2025, SIH winning tips, Smart India Hackathon tips, how to choose SIH problem statement, SIH participation guide, Smart India Hackathon guide, how to prepare for SIH, SIH strategy, Smart India Hackathon strategy, how to select problem statement SIH, SIH problem selection tips, how to win hackathon, Smart India Hackathon winning strategies, SIH 2025 tips, how to find best problem statement, SIH problem finding guide, how to participate Smart India Hackathon 2025, SIH registration guide, Smart India Hackathon preparation tips, how to build winning solution SIH, SIH team formation tips, how to get selected in SIH</h4>
        </div>

        {/* Footer */}
        <footer className="border-t border-border bg-card/30 mt-8 sm:mt-12 lg:mt-16">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <div className="text-center space-y-3 sm:space-y-4">
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
                <span className="text-sm sm:text-base font-semibold text-foreground">Smart India Hackathon 2025</span>
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground px-4">
                assembled at 3 AM by anjaneya and ishaan
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
