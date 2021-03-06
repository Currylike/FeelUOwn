import logging

from .base import cmd_handler_mapping

from .help import HelpHandler  # noqa
from .status import StatusHandler  # noqa
from .playlist import PlaylistHandler  # noqa
from .player import PlayerHandler  # noqa
from .search import SearchHandler  # noqa
from .show import ShowHandler  # noqa

logger = logging.getLogger(__name__)


class Cmd:
    def __init__(self, action, *args, **kwargs):
        self.action = action
        self.args = args

    def __str__(self):
        return 'action:{} args:{}'.format(self.action, self.args)


class CmdParser:

    @classmethod
    def parse(cls, cmd_str):
        cmd_str = cmd_str.strip()
        cmd_parts = cmd_str.split(' ', 1)
        if not cmd_parts:
            return None
        return Cmd(*cmd_parts)


class CmdResolver:
    def __init__(self, cmd_handler_mapping):
        self.cmd_handler_mapping = cmd_handler_mapping

    def get_handler(self, cmd):
        return self.cmd_handler_mapping.get(cmd)


cmd_resolver = CmdResolver(cmd_handler_mapping)


def exec_cmd(app, live_lyric, cmd):
    # FIXME: 要么只传 app，要么把 player, live_lyric 等分别传进来
    # 目前更使用 app 作为参数

    logger.debug('EXEC_CMD: ' + str(cmd))

    handler_cls = cmd_resolver.get_handler(cmd.action)
    if handler_cls is None:
        return '\nCommand not found! Oops\n'

    rv = 'ACK {}'.format(cmd.action)
    if cmd.args:
        rv += ' {}'.format(' '.join(cmd.args))
    try:
        cmd_rv = handler_cls(app, live_lyric).handle(cmd)
        if cmd_rv:
            rv += '\n' + cmd_rv
    except Exception as e:
        logger.exception('handle cmd({}) error'.format(cmd))
        return '\nOops\n'
    else:
        rv = rv or ''
        return rv + '\nOK\n'
