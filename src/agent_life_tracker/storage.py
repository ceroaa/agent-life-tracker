"""JSON storage with a small lock file and atomic writes."""

from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Optional

from .exceptions import StateLockTimeoutError
from .models import TrackerState


DEFAULT_STATE_PATH = Path(".agent_life_tracker") / "state.json"


class JsonStorage:
    """Persist tracker state to a JSON file using atomic replacement."""

    def __init__(self, state_path: Optional[os.PathLike[str] | str] = None) -> None:
        self.state_path = Path(state_path) if state_path else DEFAULT_STATE_PATH
        self.lock_path = self.state_path.with_suffix(self.state_path.suffix + ".lock")

    def initialize(self) -> None:
        """Create the state file if it does not already exist."""

        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            self.write(TrackerState().to_dict())

    def read(self) -> Dict[str, object]:
        """Read state JSON, creating a valid empty state if needed."""

        self.initialize()
        with self.state_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write(self, data: Dict[str, object]) -> None:
        """Atomically write state JSON.

        The file is written to a temporary sibling, flushed and fsynced, then
        moved over the real state path with os.replace.
        """

        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock():
            temp_path = self.state_path.with_name(
                f".{self.state_path.name}.{os.getpid()}.tmp"
            )
            with temp_path.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.state_path)

    @contextmanager
    def _lock(self, timeout_seconds: float = 5.0) -> Iterator[None]:
        """Acquire a best-effort cross-platform lock file."""

        start = time.monotonic()
        descriptor: Optional[int] = None
        while descriptor is None:
            try:
                descriptor = os.open(
                    self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
            except FileExistsError:
                if time.monotonic() - start >= timeout_seconds:
                    raise StateLockTimeoutError(
                        f"Timed out waiting for state lock: {self.lock_path}"
                    )
                time.sleep(0.05)

        try:
            os.write(descriptor, str(os.getpid()).encode("ascii"))
            yield
        finally:
            os.close(descriptor)
            try:
                os.unlink(self.lock_path)
            except FileNotFoundError:
                pass

