import Uploader from '@/components/Uploader'
import { listProjects } from '@/lib/api'
import Link from 'next/link'

export default async function Home() {
  let projects = [] as Awaited<ReturnType<typeof listProjects>>
  try { projects = await listProjects() } catch {}

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,#4c1d95,transparent_35%),#0f172a] p-5 md:p-10">
      <section className="mx-auto max-w-6xl">
        <div className="mb-8 text-center">
          <p className="text-sm font-bold uppercase tracking-[0.3em] text-violet-300">AI Manga Translator Pro</p>
          <h1 className="mt-4 text-4xl font-black md:text-6xl">ترجم المانجا داخل الصورة</h1>
          <p className="mx-auto mt-4 max-w-2xl text-slate-300">ارفع فصل ZIP أو CBZ، وسيتم استخراج الصفحات، مسح النص القديم، تركيب العربية، ثم عرض الفصل في قارئ احترافي.</p>
        </div>
        <Uploader />
        <div className="mt-8 card p-6">
          <h2 className="mb-4 text-2xl font-bold">آخر المشاريع</h2>
          <div className="grid gap-3">
            {projects.length === 0 && <p className="text-slate-400">لا توجد مشاريع بعد.</p>}
            {projects.map((p) => (
              <Link key={p.id} href={`/project/${p.id}`} className="rounded-2xl bg-white/10 p-4 transition hover:bg-white/20">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-bold">{p.title}</span>
                  <span className="text-sm text-violet-200">{p.status} · {p.progress}%</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}
