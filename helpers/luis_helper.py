# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from product_details import ProductDetails


class Intent(Enum):
    ASK = "Ask"
    CANCEL = "Cancel"
    GET_WEATHER = "GetWeather"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.ASK.value:
                print("=")
                result = ProductDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                use_entities = recognizer_result.entities.get("$instance", {}).get(
                    "use", []
                )
                if len(use_entities) > 0:
                    if recognizer_result.entities.get("use", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.use = use_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_things.append(
                            to_entities[0]["text"].capitalize()
                        )
                """
                # We need to get the result from the LUIS JSON which at every level returns an array.
                cost_entities = recognizer_result.entities.get("$instance", {}).get(
                    "cost", []
                )
                if len(cost_entities) > 0:
                    if recognizer_result.entities.get("cost", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.cost = cost_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_things.append(
                            to_entities[0]["text"].capitalize()
                        )
                """
                result.cost = turn_context.activity.text
                 # We need to get the result from the LUIS JSON which at every level returns an array.
                brand_entities = recognizer_result.entities.get("$instance", {}).get(
                    "brand", []
                )
                if len(brand_entities) > 0:
                    if recognizer_result.entities.get("brand", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.brand = use_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_things.append(
                            to_entities[0]["text"].capitalize()
                        )               

                # We need to get the result from the LUIS JSON which at every level returns an array.
                looking_entities = recognizer_result.entities.get("$instance", {}).get(
                    "looking", []
                )
                if len(looking_entities) > 0:
                    if recognizer_result.entities.get("looking", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.looking = use_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_things.append(
                            to_entities[0]["text"].capitalize()
                        )

        except Exception as exception:
            print(exception)

        return intent, result
