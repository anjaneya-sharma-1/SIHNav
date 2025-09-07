"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { ProblemStatement } from "@/lib/search"
import { Building2, Cpu, Users, Target, Eye, TrendingUp } from "lucide-react"

interface ProblemCardProps {
  problem: ProblemStatement
  searchQuery?: string
}

export function ProblemCard({ problem, searchQuery }: ProblemCardProps) {
  const getDifficultyBorderColor = (difficulty: string) => {
    switch (difficulty) {
      case "Easy":
        return "border-l-green-500 border-l-4"
      case "Med":
        return "border-l-yellow-500 border-l-4"
      case "Hard":
        return "border-l-red-500 border-l-4"
      default:
        return "border-l-muted border-l-4"
    }
  }

  const highlightText = (text: string, query?: string) => {
    if (!query) return text

    const regex = new RegExp(`(${query.split(" ").join("|")})`, "gi")
    const parts = text.split(regex)

    return parts.map((part, index) =>
      regex.test(part) ? (
        <mark key={index} className="bg-primary/20 text-primary-foreground px-1 rounded">
          {part}
        </mark>
      ) : (
        part
      ),
    )
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Card
          className={`group hover:shadow-lg transition-all duration-300 hover:-translate-y-1 bg-card border-border cursor-pointer ${getDifficultyBorderColor(problem.difficulty)}`}
        >
          <CardHeader className="pb-2 sm:pb-3 p-3 sm:p-6">
            <div className="flex items-start justify-between gap-2 sm:gap-3">
              <CardTitle className="text-sm sm:text-base lg:text-lg font-semibold text-card-foreground leading-tight">
                {highlightText(problem.title, searchQuery)}
              </CardTitle>
            </div>
            <div className="flex items-center justify-between">
              <div className="text-xs text-muted-foreground font-mono">{problem.ps_id}</div>
              {problem.submission_count && (
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingUp className="w-3 h-3" />
                  <span className="hidden sm:inline">{problem.submission_count} submissions</span>
                  <span className="sm:hidden">{problem.submission_count}</span>
                </div>
              )}
            </div>
          </CardHeader>

          <CardContent className="space-y-2 sm:space-y-3 lg:space-y-4 p-3 sm:p-6 pt-0">
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed line-clamp-2 sm:line-clamp-3">
              {highlightText(problem.summary, searchQuery)}
            </p>

            <div className="space-y-1 sm:space-y-2">
              <div className="flex items-center gap-1 sm:gap-2 text-xs">
                <Building2 className="w-3 h-3 text-muted-foreground flex-shrink-0" />
                <span className="text-muted-foreground truncate">{problem.organization}</span>
              </div>

              <div className="flex items-center gap-1 sm:gap-2 text-xs">
                <Target className="w-3 h-3 text-muted-foreground flex-shrink-0" />
                <span className="text-muted-foreground truncate">{problem.solution_type}</span>
              </div>
            </div>

            <div className="space-y-1 sm:space-y-2">
              <div className="text-xs font-medium text-muted-foreground">Technologies:</div>
              <div className="flex flex-wrap gap-1">
                {problem.technology.slice(0, 2).map((tech) => (
                  <Badge key={tech} variant="outline" className="text-xs px-1 py-0">
                    {tech}
                  </Badge>
                ))}
                {problem.technology.length > 2 && (
                  <Badge variant="outline" className="text-xs px-1 py-0">
                    +{problem.technology.length - 2}
                  </Badge>
                )}
              </div>
            </div>

            <div className="space-y-1 sm:space-y-2">
              <div className="text-xs font-medium text-muted-foreground flex items-center gap-1">
                <Target className="w-3 h-3" />
                Impact:
              </div>
              <div className="flex flex-wrap gap-1">
                {problem.impact_area.slice(0, 1).map((area) => (
                  <Badge key={area} variant="secondary" className="text-xs px-1 py-0">
                    {area}
                  </Badge>
                ))}
                {problem.impact_area.length > 1 && (
                  <Badge variant="secondary" className="text-xs px-1 py-0">
                    +{problem.impact_area.length - 1}
                  </Badge>
                )}
              </div>
            </div>

            <div className="flex items-center justify-center pt-1 sm:pt-2 border-t border-border/50">
              <div className="flex items-center gap-1 sm:gap-2 text-xs text-muted-foreground group-hover:text-primary transition-colors">
                <Eye className="w-3 h-3" />
                <span className="hidden sm:inline">Click to view full details</span>
                <span className="sm:hidden">View details</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </DialogTrigger>

      <DialogContent className="flex flex-col max-w-7xl w-[95vw] sm:w-[90vw] h-[95vh] sm:h-[90vh] p-0">
        <DialogHeader className="flex-shrink-0 p-4 sm:p-6 pb-2 sm:pb-3 border-b">
          <DialogTitle className="text-base sm:text-lg lg:text-xl font-bold text-balance pr-6 sm:pr-8">
            {problem.title}
          </DialogTitle>
          <div className="flex items-center gap-2 sm:gap-4 text-sm text-muted-foreground flex-wrap">
            <span className="font-mono text-xs sm:text-sm">{problem.ps_id}</span>
            <div className="flex items-center gap-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  problem.difficulty === "Easy"
                    ? "bg-green-500"
                    : problem.difficulty === "Med"
                      ? "bg-yellow-500"
                      : "bg-red-500"
                }`}
              ></div>
              <span className="text-xs sm:text-sm">{problem.difficulty}</span>
            </div>
            {problem.submission_count && (
              <div className="flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                <span className="text-xs sm:text-sm">{problem.submission_count} submissions</span>
              </div>
            )}
          </div>
        </DialogHeader>

        <ScrollArea className="flex-1 min-h-0 px-4 sm:px-6">
          <div className="space-y-4 sm:space-y-6 py-4 sm:py-6">
            <div>
              <h3 className="font-semibold mb-2 text-sm sm:text-base">Summary</h3>
              <p className="text-muted-foreground leading-relaxed text-sm sm:text-base">{problem.summary}</p>
            </div>

            <div>
              <h3 className="font-semibold mb-2 text-sm sm:text-base">Full Description</h3>
              <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap text-sm sm:text-base">
                {problem.description}
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <h3 className="font-semibold mb-2 flex items-center gap-2 text-sm sm:text-base">
                  <Building2 className="w-4 h-4" />
                  Organization Details
                </h3>
                <div className="space-y-2 text-xs sm:text-sm">
                  <div>
                    <span className="font-medium">Organization:</span> {problem.organization}
                  </div>
                  <div>
                    <span className="font-medium">Department:</span> {problem.department}
                  </div>
                  <div>
                    <span className="font-medium">Category:</span> {problem.category}
                  </div>
                  <div>
                    <span className="font-medium">Theme:</span> {problem.theme}
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-2 flex items-center gap-2 text-sm sm:text-base">
                  <Target className="w-4 h-4" />
                  Solution Requirements
                </h3>
                <div className="space-y-2 text-xs sm:text-sm">
                  <div>
                    <span className="font-medium">Solution Type:</span> {problem.solution_type}
                  </div>
                  <div>
                    <span className="font-medium">Difficulty:</span> {problem.difficulty}
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2 flex items-center gap-2 text-sm sm:text-base">
                <Cpu className="w-4 h-4" />
                Technologies Required
              </h3>
              <div className="flex flex-wrap gap-1 sm:gap-2">
                {problem.technology.map((tech) => (
                  <Badge key={tech} variant="outline" className="text-xs">
                    {tech}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2 flex items-center gap-2 text-sm sm:text-base">
                <Users className="w-4 h-4" />
                Stakeholders
              </h3>
              <div className="flex flex-wrap gap-1 sm:gap-2">
                {problem.stakeholders.map((stakeholder) => (
                  <Badge key={stakeholder} variant="secondary" className="text-xs">
                    {stakeholder}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2 flex items-center gap-2 text-sm sm:text-base">
                <Target className="w-4 h-4" />
                Impact Areas
              </h3>
              <div className="flex flex-wrap gap-1 sm:gap-2">
                {problem.impact_area.map((area) => (
                  <Badge key={area} variant="secondary" className="text-xs">
                    {area}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2 text-sm sm:text-base">Data & Resource Types</h3>
              <div className="flex flex-wrap gap-1 sm:gap-2">
                {problem.data_resource_type.map((type) => (
                  <Badge key={type} variant="outline" className="text-xs">
                    {type}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}
