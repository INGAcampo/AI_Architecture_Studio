from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SyncReport:
    model_revision: int
    updated_view_ids: tuple[str, ...]
    unchanged_view_ids: tuple[str, ...]

class DocumentationSynchronizer:
    def synchronize(self, view_manager, model_revision):
        updated, unchanged = [], []
        for view in view_manager.all():
            if view.model_revision < model_revision:
                view_manager.update_revision(view.view_id, model_revision)
                updated.append(view.view_id)
            else:
                unchanged.append(view.view_id)
        return SyncReport(
            model_revision=int(model_revision),
            updated_view_ids=tuple(updated),
            unchanged_view_ids=tuple(unchanged),
        )
