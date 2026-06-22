import Link from 'next/link'
import { API_URL, getProject } from '@/lib/api'

export default async function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const data = await getProject(id)
  const { project, pages } = data
  return (
    <main className="min-h-screen p-5 md:p-10">
      <section className="mx-auto max-w-5xl">
        <Link href="/" className="text-violet-300">← رجوع</Link>
        <div className="card mt-5 p-6">
          <h1 className="text-3xl font-black">{project.title}</h1>
          <p className="mt-2 text-slate-300">الحالة: {project.status} · التقدم: {project.progress}%</p>
          <div className="mt-4 h-3 rounded-full bg-white/10"><div className="h-3 rounded-full bg-violet-500" style={{ width: `${project.progress}%` }} /></div>
          {project.error && <p className="mt-3 text-red-300">{project.error}</p>}
          <div className="mt-6 flex flex-wrap gap-3">
            <Link href={`/reader/${project.id}`} className="btn bg-violet-500 text-white">فتح مشغل الفصل</Link>
            <a href={`${API_URL}/projects/${project.id}/download.cbz`} className="btn bg-white/10 text-white">تحميل CBZ مترجم</a>
          </div>
        </div>
        <div className="mt-6 grid gap-3 md:grid-cols-3">
          {pages.map((page) => <div key={page.id} className="card p-4"><b>صفحة {page.page_number}</b><p className="text-sm text-slate-300">{page.status}</p></div>)}
        </div>
      </section>
    </main>
  )
}
