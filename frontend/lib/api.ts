export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export type Project = {
  id: string
  title: string
  source_language: string
  target_language: string
  reading_mode: string
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
  progress: number
  error?: string | null
}

export type Page = {
  id: string
  project_id: string
  page_number: number
  original_path: string
  translated_path?: string | null
  status: string
}

export async function listProjects(): Promise<Project[]> {
  const res = await fetch(`${API_URL}/projects`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to load projects')
  return res.json()
}

export async function getProject(id: string): Promise<{ project: Project; pages: Page[] }> {
  const res = await fetch(`${API_URL}/projects/${id}`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to load project')
  return res.json()
}

export function mediaUrl(projectId: string, folder: 'original' | 'translated' | 'cleaned', filename: string) {
  return `${API_URL}/media/${projectId}/${folder}/${filename}`
}

export function pathFilename(path?: string | null) {
  if (!path) return ''
  return path.split('/').pop() || path.split('\\').pop() || ''
}
