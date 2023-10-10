from pathlib import Path
from dataclasses import dataclass
import itertools

from codemodder.change import Change
from codemodder.executor import CodemodExecutorWrapper
from codemodder.registry import CodemodRegistry


@dataclass
class ChangeSet:
    """A set of changes made to a file at `path`"""

    path: str
    diff: str
    changes: list[Change]

    def to_json(self):
        return {"path": self.path, "diff": self.diff, "changes": self.changes}


class CodemodExecutionContext:
    _results_by_codemod: dict[str, list[ChangeSet]] = {}
    _failures_by_codemod: dict[str, list[Path]] = {}
    dependencies: set[str]
    directory: Path
    dry_run: bool = False
    registry: CodemodRegistry

    def __init__(self, directory, dry_run, registry: CodemodRegistry):
        self.directory = directory
        self.dry_run = dry_run
        self.dependencies = set()
        self._results_by_codemod = {}
        self._failures_by_codemod = {}
        self.registry = registry

    def add_result(self, codemod_name, change_set):
        self._results_by_codemod.setdefault(codemod_name, []).append(change_set)

    def add_failure(self, codemod_name, file_path):
        self._failures_by_codemod.setdefault(codemod_name, []).append(file_path)

    def get_results(self, codemod_name):
        return self._results_by_codemod.get(codemod_name, [])

    def get_changed_files(self):
        return [
            change_set.path
            for changes in self._results_by_codemod.values()
            for change_set in changes
        ]

    def get_failures(self, codemod_name):
        return self._failures_by_codemod.get(codemod_name, [])

    def get_failed_files(self):
        return list(
            itertools.chain.from_iterable(
                failures for failures in self._failures_by_codemod.values()
            )
        )

    def add_dependency(self, dependency: str):
        self.dependencies.add(dependency)

    def compile_results(self, codemods: list[CodemodExecutorWrapper]):
        results = []
        for codemod in codemods:
            if not (changeset := self._results_by_codemod.get(codemod.id)):
                continue

            data = {
                "codemod": codemod.id,
                "summary": codemod.summary,
                "description": codemod.description,
                "references": [],
                "properties": {},
                "failedFiles": [],
                "changeset": [change.to_json() for change in changeset],
            }

            results.append(data)

        return results
