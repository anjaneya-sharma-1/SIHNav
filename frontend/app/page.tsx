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
                Official Problem Statements Database | AI Challenges | Tech Innovation Solutions
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
                  Browse 1000+ Smart India Hackathon 2025 problem statements from 50+ government ministries. 
                  Find AI challenges, tech innovation problems, and digital solutions for SIH2025 preparation.
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
          <h2>Smart India Hackathon 2025 Problem Statements Database</h2>
          <p>This is the official Smart India Hackathon 2025 problem statements database and navigation platform. Students, developers, and innovators can browse through 1000+ carefully curated problem statements from over 50 government ministries and organizations.</p>
          
          <h3>AI Problem Statements and Technology Challenges</h3>
          <p>Find AI website problems for SIH, artificial intelligence challenges, machine learning problems, data science competitions, and cutting-edge technology solutions for Smart India Hackathon 2025.</p>
          
          <h3>Smart India Hackathon Project Ideas and Innovation Challenges</h3>
          <p>Discover smart india hackathon project opportunities across domains like healthcare technology, fintech innovation, smart cities development, agriculture technology, education technology, cybersecurity, renewable energy, transportation technology, e-governance solutions, and digital transformation challenges.</p>
          
          <h3>Government Ministry Problem Statements</h3>
          <p>Browse problem statements from various government ministries including Ministry of Electronics and IT, Ministry of Health, Ministry of Education, Ministry of Agriculture, Ministry of Urban Development, and many more for the Smart India Hackathon 2025 competition.</p>
          
          <h4>Keywords: Smart India Hackathon, Smart India Hackathon 2025, SIH 2025, SIH2025, smart india hackathon project, smart india hackathon website, AI problem statements, AI website SIH, hackathon problems database, government hackathon challenges, ministry problem statements, student hackathon competition, coding challenges India, tech innovation problems, Digital India hackathon, startup problem statements, innovation challenges 2025</h4>
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
