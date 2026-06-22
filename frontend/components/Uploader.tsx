'use client'

import { useState } from 'react'
import { API_URL } from '@/lib/api'

export default function Uploader() {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('Chapter 01')
  const [readingMode, setReadingMode] = useState('webtoon')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')

  async function upload() {
    if (!file) return setMessage('اختر ملف صورة أو ZIP أو CBZ أولًا')
    setBusy(true)
    setMessage('يتم رفع الفصل وبدء المعالجة...')
    const form = new FormData()
    form.append('file', file)
    form.append('title', title)
    form.append('source_language', 'en')
    form.append('target_language', 'ar')
    form.append('reading_mode', readingMode)
    const res = await fetch(`${API_URL}/projects`, { method: 'POST', body: form })
    setBusy(false)
    if (!res.ok) {
      setMessage('فشل الرفع. تأكد من نوع الملف.')
      return
    }
    const project = await res.json()
    window.location.href = `/project/${project.id}`
  }

  return (
    <div className="card p-6">
      <div className="grid gap-4 md:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm text-slate-300">اسم الفصل</span>
          <input className="w-full rounded-2xl bg-white/10 p-3 outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-violet-400" value={title} onChange={(e) => setTitle(e.target.value)} />
        </label>
        <label className="block">
          <span className="mb-2 block text-sm text-slate-300">نوع القراءة</span>
          <select className="w-full rounded-2xl bg-white/10 p-3 outline-none ring-1 ring-white/10" value={readingMode} onChange={(e) => setReadingMode(e.target.value)}>
            <option value="webtoon">مانهوا عمودي</option>
            <option value="manga-rtl">مانجا يمين لليسار</option>
          </select>
        </label>
      </div>
      <div className="mt-5 rounded-3xl border border-dashed border-violet-300/50 bg-black/20 p-8 text-center">
        <input type="file" accept=".jpg,.jpeg,.png,.webp,.zip,.cbz" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <p className="mt-3 text-sm text-slate-300">يدعم JPG / PNG / WEBP / ZIP / CBZ</p>
      </div>
      <button disabled={busy} onClick={upload} className="btn mt-5 w-full bg-violet-500 text-white disabled:opacity-50">{busy ? 'جاري المعالجة...' : 'ابدأ ترجمة الفصل'}</button>
      {message && <p className="mt-3 text-center text-sm text-slate-300">{message}</p>}
    </div>
  )
}
