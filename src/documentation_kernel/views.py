from dataclasses import replace

class ViewManager:
    def __init__(self):
        self._views = {}

    def add(self, view, *, replace_existing=False):
        if view.view_id in self._views and not replace_existing:
            raise ValueError(f"Vista duplicada: {view.view_id}")
        self._views[view.view_id] = view

    def get(self, view_id):
        return self._views[view_id]

    def add_annotation(self, view_id, annotation):
        view = self._views[view_id]
        updated = replace(view, annotations=view.annotations + (annotation,))
        self._views[view_id] = updated
        return updated

    def update_revision(self, view_id, revision):
        view = self._views[view_id]
        updated = replace(view, model_revision=int(revision))
        self._views[view_id] = updated
        return updated

    def all(self):
        return tuple(self._views[key] for key in sorted(self._views))
