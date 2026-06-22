import Link from 'next/link'
import { getProject, mediaUrl, pathFilename } from '@/lib/api'

export default async function ReaderPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const { project, pages } = await getProject(id)
  return (
    <main className="min-h-screen bg-black p-3 text-white">
      <div className="sticky top-0 z-10 mb-4 rounded-2xl bg-slate-900/90 p-4 backdrop-blur">
        <div className="mx-auto flex max-w-4xl items-center justify-between gap-3">
          <Link href={`/project/${project.id}`} className="text-violet-300">← المشروع</Link>
          <h1 className="text-center font-bold">{project.title}</h1>
          <span className="text-sm text-slate-400">{pages.length} صفحة</span>
        </div>
      </div>
      <div className={project.reading_mode === 'webtoon' ? 'mx-auto max-w-3xl' : 'mx-auto max-w-4xl'}>
        {pages.map((page) => {
          const translated = page.translated_path ? mediaUrl(project.id, 'translated', pathFilename(page.translated_path)) : null
          const original = mediaUrl(project.id, 'original', pathFilename(page.original_path))
          return (
            <div key={page.id} className="mb-2 overflow-hidden rounded-xl bg-slate-900">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={translated || original} alt={`page ${page.page_number}`} className="mx-auto w-full" />
            </div>
          )
        })}
      </div>
    </main>
  )
}
