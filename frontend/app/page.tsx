"use client"

import { useState, useEffect, useMemo } from "react"
import { SearchBar } from "@/components/search-bar"
import { Sidebar } from "@/components/sidebar"
import { ProblemCard } from "@/components/problem-card"
import { ThemeToggle } from "@/components/theme-toggle"
import {
  sampleProblems,
  fuzzySearch,
  filterByTags,
  getAllTags,
  sortProblems,
  type ProblemStatement,
} from "@/lib/search"
import { Button } from "@/components/ui/button"
import { Sparkles, Trophy, Users, Filter } from "lucide-react"

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [filteredProblems, setFilteredProblems] = useState<ProblemStatement[]>(sampleProblems)
  const [sortBy, setSortBy] = useState<"relevance" | "submissions_high" | "submissions_low">("relevance")
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const submissionCounts = sampleProblems.map((p) => p.submission_count || 0)
  const minSubmissions = Math.min(...submissionCounts)
  const maxSubmissions = Math.max(...submissionCounts)
  const [submissionRange, setSubmissionRange] = useState<[number, number]>([minSubmissions, maxSubmissions])

  const allTags = useMemo(() => getAllTags(sampleProblems), [])

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
          <div className="container mx-auto px-3 sm:px-4 py-2 sm:py-3">
            <div className="flex justify-end">
              <ThemeToggle />
            </div>
            <div className="text-center space-y-1">
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
                <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-foreground">Smart India Hackathon 2025</h1>
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground text-balance">
                Discover innovative problem statements and build solutions for India's future
              </p>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-6 sm:py-8 lg:py-12 bg-gradient-to-b from-primary/5 to-background">
          <div className="container mx-auto px-3 sm:px-4">
            <div className="text-center space-y-4 sm:space-y-6 lg:space-y-8">
              <div className="space-y-2 sm:space-y-4">
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground text-balance">
                  Stop <span className="text-red-500 italic">Scrolling</span>. Start{" "}
                  <span className="text-green-500 italic">Winning</span>
                </h2>
                <p className="text-sm sm:text-base lg:text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
                  Search through curated problem statements from various ministries and domains. Use our intelligent
                  search to find challenges that match your skills and interests.
                </p>
              </div>

              {/* Search Bar and Filter Toggle */}
              <div className="space-y-3 sm:space-y-4">
                <SearchBar value={searchQuery} onChange={setSearchQuery} onSearch={handleSearch} />

                {!sidebarOpen && (
                  <Button
                    variant="outline"
                    onClick={() => setSidebarOpen(true)}
                    className="flex items-center gap-2 text-sm"
                  >
                    <Filter className="h-4 w-4" />
                    Show Filters & Sort
                  </Button>
                )}
              </div>

              {/* Stats */}
              <div className="flex items-center justify-center gap-4 sm:gap-6 lg:gap-8 text-xs sm:text-sm text-muted-foreground">
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
          <div className="container mx-auto px-3 sm:px-4 space-y-4 sm:space-y-6 lg:space-y-8">
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
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
                {filteredProblems.map((problem) => (
                  <ProblemCard key={problem.id} problem={problem} searchQuery={searchQuery} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 sm:py-12 space-y-4">
                <div className="text-3xl sm:text-4xl">🔍</div>
                <h3 className="text-base sm:text-lg font-medium text-foreground">No problems found</h3>
                <p className="text-sm text-muted-foreground">
                  Try adjusting your search query or removing some filters
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-border bg-card/30 mt-8 sm:mt-12 lg:mt-16">
          <div className="container mx-auto px-3 sm:px-4 py-6 sm:py-8">
            <div className="text-center space-y-3 sm:space-y-4">
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
                <span className="text-sm sm:text-base font-semibold text-foreground">Smart India Hackathon 2025</span>
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground">
                Empowering innovation through technology • Building solutions for tomorrow
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
