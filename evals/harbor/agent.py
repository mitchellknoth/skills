"""Harbor external-agent bridge. Requires the optional Harbor installation."""
import asyncio
import json
from pathlib import Path
import tempfile
from harbor.agents.base import BaseAgent
from .transport import execute


def boolean(value):
    if value is True or value == 'true':
        return True
    if value is False or value == 'false':
        return False
    raise ValueError('Boolean options must be true or false')


class LocalFleetAgent(BaseAgent):
    def __init__(self, *args, bundle, allow_inference=False, mock=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundle = str(Path(bundle).resolve())
        self.allow_inference = boolean(allow_inference)
        self.mock = boolean(mock)

    @staticmethod
    def name():
        return 'fleet-local-decision-probe'

    def version(self):
        return '1.0.0'

    async def setup(self, environment):
        # No installation, authentication, hooks or inference in the container.
        pass

    async def run(self, instruction, environment, context):
        output = await asyncio.to_thread(execute, self.bundle, instruction,
                                         self.allow_inference, self.mock)
        with tempfile.TemporaryDirectory(prefix='fleet-harbor-answer-') as tmp:
            source = Path(tmp) / 'answer.json'
            source.write_text(json.dumps(output))
            await environment.upload_file(source_path=source, target_path='/app/answer.json')
