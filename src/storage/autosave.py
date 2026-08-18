from pathlib import Path
import threading
from .project_io import ProjectIO
class AutosaveManager:
    def __init__(self,document_provider,interval_seconds=300,autosave_directory='autosave'):
        if interval_seconds<10: raise ValueError('El intervalo mínimo es 10 segundos')
        self.document_provider=document_provider; self.interval_seconds=interval_seconds; self.autosave_directory=Path(autosave_directory); self.project_io=ProjectIO(); self._timer=None; self._running=False
    def start(self):
        if not self._running: self._running=True; self._schedule()
    def stop(self):
        self._running=False
        if self._timer: self._timer.cancel(); self._timer=None
    def run_once(self):
        doc=self.document_provider()
        if doc is None or not doc.dirty: return None
        self.autosave_directory.mkdir(parents=True,exist_ok=True)
        safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in doc.metadata.name).strip('_') or 'Sin_titulo'
        dest=self.autosave_directory/f'{safe}.autosave.aias'; old_path=doc.file_path; old_dirty=doc.dirty
        try: return self.project_io.serializer.serialize(doc,dest)
        finally: doc.file_path=old_path; doc.dirty=old_dirty
    def _schedule(self):
        if self._running:
            self._timer=threading.Timer(self.interval_seconds,self._tick); self._timer.daemon=True; self._timer.start()
    def _tick(self):
        try: self.run_once()
        finally: self._schedule()
