import pprint
import logging
from typing import Any, Text, Dict, List, Type

from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.features import Features
from rasa.shared.nlu.training_data.message import Message

logger = logging.getLogger(__name__)

from rasa.nlu.tokenizers.tokenizer import Token

import collections

def apply_func_to_dict_values(d, func):
    if isinstance(d, dict):
        return {k: apply_func_to_dict_values(v, func) for k, v in d.items()}
    elif isinstance(d, list):
        return [apply_func_to_dict_values(item, func) for item in d]
    else:
        return func(d)
    
def _convert(v):
    if isinstance(v, (Token, Features)):
        return v.__dict__
    return v

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER, is_trainable=False
)
class Printer(GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        """Components that should be included in the pipeline before this component."""
        return []

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            **GraphComponent.get_default_config(),
            "alias": None,
            "pretty": True,
        }
    
    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
        model_storage: ModelStorage,
        resource: Resource,
    ) -> None:
        """Constructs a new tf/idf vectorizer using the sklearn framework."""
        super().__init__()
        self._config = config
        self._name = name
        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """Creates a new untrained component (see parent class for full docstring)."""
        return cls(config, execution_context.node_name, model_storage, resource)
    
    def process(self, messages: List[Message]) -> List[Message]:
        """Processes incoming message and compute and set features."""
        if self._config['alias']:
            logger.info(self._config['alias'])

        _messages = [apply_func_to_dict_values(msg.__dict__, _convert) for msg in messages]
        logger.info(pprint.pformat(_messages) if self._config['pretty'] else str(_messages))
        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Processes the training examples in the given training data in-place."""
        return training_data