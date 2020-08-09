from typing import Dict, Any, Tuple, Optional
from ...abstract.node import AbstractNode
from .common import ImmediateActionWithoutReply

from syft.core.common.uid import UID
from syft.core.io.address import Address
from ....store.storeable_object import StorableObject


class RunClassMethodAction(ImmediateActionWithoutReply):
    def __init__(
        self,
        path: str,
        _self: Any,
        args: Tuple[Any],
        kwargs: Dict[Any, Any],
        id_at_location: int,
        address: Address,
        msg_id: Optional[UID] = None,
    ):
        super().__init__(address=address, msg_id=msg_id)
        self.path = path
        self._self = _self
        self.args = args
        self.kwargs = kwargs
        self.id_at_location = id_at_location

    def execute_action(self, node: AbstractNode) -> None:
        print(self.path)
        print(self._self)
        print(self.args)
        print(self.kwargs)
        print(self.id_at_location)

        method = node.lib_ast(self.path)

        resolved_self = node.store[self._self.id_at_location].data

        resolved_args = list()
        for arg in self.args:
            r_arg = node.store[arg.id_at_location].data
            resolved_args.append(r_arg)

        resolved_kwargs = {}
        for arg_name, arg in self.kwargs.items():
            r_arg = node.store[arg.id_at_location].data
            resolved_kwargs[arg_name] = r_arg

        result = method(resolved_self, *resolved_args, **resolved_kwargs)

        if not isinstance(result, StorableObject):
            result = StorableObject(id=self.id_at_location, data=result)
        node.store.store(obj=result)
