import asyncio
from typing import Union

from ...exceptions import NodeJSNotRunning
from ...exceptions import NoMtProtoClientSet
from ...exceptions import NotInGroupCallError
from ...mtproto import BridgedClient
from ...scaffold import Scaffold
from ...types import NotInGroupCall
from ...types.session import Session


class ResumeStream(Scaffold):
    async def resume_stream(
        self,
        chat_id: Union[int, str],
    ):
        """Resume the paused stream

        This method allow to resume the paused streaming file

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier of the target chat.
                Can be a direct id (int) or a username (str)

        Raises:
            NoMtProtoClientSet: In case you try
                to call this method without any MtProto client
            NodeJSNotRunning: In case you try
                to call this method without do
                :meth:`~herokulls.herokulls.start` before
            NotInGroupCallError: In case you try
                to leave a non-joined group call

        Returns:
            ``bool``:
            On success, true is returned if was resumed

        Example:
            .. code-block:: python
                :emphasize-lines: 10-12

                from herokulls import Client
                from herokulls import idle
                ...

                app = herokulls(client)
                app.start()

                ...  # Call API methods

                app.resume_stream(
                    -1001185324811,
                )

                idle()
        """
        try:
            chat_id = int(chat_id)
        except ValueError:
            chat_id = BridgedClient.chat_id(
                await self._app.resolve_peer(chat_id),
            )
        if self._app is not None:
            if self._wait_until_run is not None:
                solver_id = Session.generate_session_id(24)

                async def internal_sender():
                    if not self._wait_until_run.done():
                        await self._wait_until_run
                    await self._binding.send({
                        'action': 'resume',
                        'chat_id': chat_id,
                        'solver_id': solver_id,
                    })
                active_call = self._call_holder.get_active_call(chat_id)
                asyncio.ensure_future(internal_sender())
                result = await self._wait_result.wait_future_update(
                    solver_id,
                )
                if isinstance(result, NotInGroupCall):
                    raise NotInGroupCallError()
                return active_call.status == 'paused'
            else:
                raise NodeJSNotRunning()
        else:
            raise NoMtProtoClientSet()
