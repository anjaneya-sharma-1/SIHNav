// Fuzzy search and ranking utilities for SIH problem statements

export interface ProblemStatement {
  ps_id: string
  title: string
  summary: string
  description: string
  difficulty: string | string[] // Updated to handle both string and array types
  technology: string[]
  stakeholders: string[]
  impact_area: string[]
  data_resource_type: string[]
  solution_type: string | string[] // Updated to handle both string and array types
  organization: string
  department: string
  category: string
  theme: string
  submission_count?: number
}

import problemsData from "./problems-data.json"

// Sample data for SIH 2025 problem statements
export const sampleProblems: ProblemStatement[] = problemsData as ProblemStatement[]

export const TAG_CATEGORIES = {
  Technology: [
    "Artificial Intelligence (AI)",
    "Machine Learning (ML)",
    "Deep Learning (DL)",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "Robotics",
    "IoT (Internet of Things)",
    "Blockchain",
    "Augmented Reality (AR)",
    "Virtual Reality (VR)",
    "Frontend Dev",
    "Backend Dev",
    "Full Stack Development",
    "Web Development",
    "Mobile App Development",
    "Game Dev",
    "Cloud Computing",
    "Edge Computing",
    "Data Analytics",
    "Cybersecurity",
    "GIS / Remote Sensing",
    "Embedded Systems",
  ],
  Difficulty: ["Easy", "Med", "Hard"],
  Stakeholders: [
    "Government Agencies",
    "NGOs",
    "Farmers",
    "Students / Teachers",
    "Doctors / Patients",
    "Industry / Enterprises",
    "Local Communities",
    "Citizens",
    "Travelers",
    "Law Enforcement",
    "Military / Defense",
  ],
  "Impact Area": [
    "Cost Reduction",
    "Efficiency Improvement",
    "Accessibility",
    "Sustainability",
    "Inclusivity",
    "Transparency",
    "Security",
    "Safety",
    "Awareness & Education",
    "Productivity",
  ],
  "Data / Resource Type": [
    "Open Data",
    "Sensor Data",
    "Image Data",
    "Video Data",
    "Text Data",
    "Audio Data",
    "Social Media Data",
    "Satellite Data",
    "Geospatial Data",
    "Real-time Streaming",
  ],
  "Solution Type": ["Mobile Solutions", "Web Solutions", "Mobile and Web Solutions"],
}

export function fuzzySearch(query: string, problems: ProblemStatement[]): ProblemStatement[] {
  if (!query.trim()) return problems

  const searchTerms = query
    .toLowerCase()
    .split(" ")
    .filter((term) => term.length > 0)

  const scoredResults = problems.map((problem) => {
    let score = 0
    const solutionTypeText = Array.isArray(problem.solution_type)
      ? problem.solution_type.join(" ")
      : problem.solution_type
    const searchableText =
      `${problem.ps_id} ${problem.title} ${problem.summary} ${problem.description} ${problem.theme} ${problem.organization} ${problem.department} ${problem.category} ${solutionTypeText} ${Array.isArray(problem.difficulty) ? problem.difficulty.join(" ") : problem.difficulty} ${problem.technology.join(" ")} ${problem.stakeholders.join(" ")} ${problem.impact_area.join(" ")} ${problem.data_resource_type.join(" ")}`.toLowerCase()

    searchTerms.forEach((term) => {
      // Exact match in ps_id (highest score)
      if (problem.ps_id.toLowerCase().includes(term)) {
        score += 15
      }

      // Exact match in title (high score)
      if (problem.title.toLowerCase().includes(term)) {
        score += 10
      }

      // Exact match in summary
      if (problem.summary.toLowerCase().includes(term)) {
        score += 8
      }

      // Exact match in technology, theme, or tags
      const solutionTypeMatch = Array.isArray(problem.solution_type)
        ? problem.solution_type.some((type) => type.toLowerCase().includes(term))
        : problem.solution_type.toLowerCase().includes(term)

      if (
        problem.technology.some((tech) => tech.toLowerCase().includes(term)) ||
        problem.theme.toLowerCase().includes(term) ||
        problem.stakeholders.some((stakeholder) => stakeholder.toLowerCase().includes(term)) ||
        problem.impact_area.some((area) => area.toLowerCase().includes(term)) ||
        problem.data_resource_type.some((type) => type.toLowerCase().includes(term)) ||
        solutionTypeMatch ||
        problem.category.toLowerCase().includes(term) ||
        problem.organization.toLowerCase().includes(term) ||
        problem.department.toLowerCase().includes(term)
      ) {
        score += 7
      }

      // Exact match in description
      if (problem.description.toLowerCase().includes(term)) {
        score += 5
      }

      // Fuzzy match (partial string matching)
      if (searchableText.includes(term)) {
        score += 3
      }

      // Character similarity for typos
      const similarity = calculateSimilarity(term, searchableText)
      if (similarity > 0.7) {
        score += 2
      }
    })

    return { ...problem, score }
  })

  return scoredResults.filter((result) => result.score > 0).sort((a, b) => b.score - a.score)
}

// Simple string similarity calculation
function calculateSimilarity(str1: string, str2: string): number {
  const longer = str1.length > str2.length ? str1 : str2
  const shorter = str1.length > str2.length ? str2 : str1

  if (longer.length === 0) return 1.0

  const editDistance = levenshteinDistance(longer, shorter)
  return (longer.length - editDistance) / longer.length
}

// Levenshtein distance for fuzzy matching
function levenshteinDistance(str1: string, str2: string): number {
  const matrix = Array(str2.length + 1)
    .fill(null)
    .map(() => Array(str1.length + 1).fill(null))

  for (let i = 0; i <= str1.length; i++) matrix[0][i] = i
  for (let j = 0; j <= str2.length; j++) matrix[j][0] = j

  for (let j = 1; j <= str2.length; j++) {
    for (let i = 1; i <= str1.length; i++) {
      const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1
      matrix[j][i] = Math.min(matrix[j][i - 1] + 1, matrix[j - 1][i] + 1, matrix[j - 1][i - 1] + indicator)
    }
  }

  return matrix[str2.length][str1.length]
}

export function filterByTags(problems: ProblemStatement[], selectedTags: string[]): ProblemStatement[] {
  if (selectedTags.length === 0) return problems

  return problems.filter((problem) =>
    selectedTags.some((tag) => {
      const solutionTypeMatch = Array.isArray(problem.solution_type)
        ? problem.solution_type.includes(tag)
        : problem.solution_type === tag

      const difficultyMatch = Array.isArray(problem.difficulty)
        ? problem.difficulty.includes(tag)
        : problem.difficulty === tag

      return (
        problem.technology.includes(tag) ||
        problem.stakeholders.includes(tag) ||
        problem.impact_area.includes(tag) ||
        problem.data_resource_type.includes(tag) ||
        solutionTypeMatch ||
        difficultyMatch ||
        problem.theme === tag ||
        problem.category === tag ||
        problem.organization === tag ||
        problem.department === tag
      )
    }),
  )
}

export function getAllTags(problems: ProblemStatement[]): Record<string, string[]> {
  const categorizedTags: Record<string, string[]> = {}

  // Start with predefined categories
  Object.entries(TAG_CATEGORIES).forEach(([category, tags]) => {
    categorizedTags[category] = [...tags]
  })

  // Add unique values from problems to appropriate categories
  const uniqueThemes = new Set<string>()
  const uniqueCategories = new Set<string>()
  const uniqueOrganizations = new Set<string>()
  const uniqueDepartments = new Set<string>()

  problems.forEach((problem) => {
    uniqueThemes.add(problem.theme)
    uniqueCategories.add(problem.category)
    uniqueOrganizations.add(problem.organization)
    uniqueDepartments.add(problem.department)
  })

  // Add dynamic categories
  if (uniqueThemes.size > 0) {
    categorizedTags["Theme"] = Array.from(uniqueThemes).sort()
  }
  if (uniqueCategories.size > 0) {
    categorizedTags["Category"] = Array.from(uniqueCategories).sort()
  }
  if (uniqueOrganizations.size > 0) {
    categorizedTags["Organization"] = Array.from(uniqueOrganizations).sort()
  }
  if (uniqueDepartments.size > 0) {
    categorizedTags["Department"] = Array.from(uniqueDepartments).sort()
  }

  return categorizedTags
}

export function sortProblems(
  problems: ProblemStatement[],
  sortBy: "relevance" | "submissions_high" | "submissions_low",
): ProblemStatement[] {
  switch (sortBy) {
    case "submissions_high":
      return [...problems].sort((a, b) => (b.submission_count || 0) - (a.submission_count || 0))
    case "submissions_low":
      return [...problems].sort((a, b) => (a.submission_count || 0) - (b.submission_count || 0))
    case "relevance":
    default:
      return problems // Already sorted by relevance from fuzzySearch
  }
}
