from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if version == "editable":
            return

        frontend_dist = Path(self.root).parent / "frontend" / "dist"
        if not frontend_dist.is_dir():
            raise FileNotFoundError(
                f"Frontend build not found at {frontend_dist}. "
                "Run 'cd frontend && npm install && npm run build' before building a wheel."
            )

        build_data.setdefault("force_include", {})[str(frontend_dist)] = "app/_frontend_dist"