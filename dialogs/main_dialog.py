# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints

from product_details import ProductDetails
from recognizer import ShoppingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .recommend_dialog import RecommendDialog


class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: ShoppingRecognizer, recommend_dialog: RecommendDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._recommend_dialog_id = recommend_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(recommend_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "您好！有什么能帮到您的吗？"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._recommend_dialog_id, ProductDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        '''
        status_message_text = (
            "intent: "+intent+"  luis_result: "+luis_result
            )
        status_message = MessageFactory.text(
            status_message_text, status_message_text, InputHints.ignoring_input
        )
        
        await step_context.context.send_activity(status_message)
        '''
        #if intent == Intent.ASK.value and luis_result:
        if intent == Intent.ASK.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._recommend_dialog_id, luis_result)

        else:
            didnt_understand_text = (
                "有一说一，这个我搞不懂。"+str(intent)+Intent.ASK.value+str(luis_result)
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg_txt = (
                #f"请确认：您购买电脑是为了 { result.use } 用途"
                #f"您的预算为：{ result.cost }"
                #f"您的外观需求为：{ result.looking }"
                f"如何？"
            )

            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

        prompt_message = "我还能帮到什么吗？"
        return await step_context.replace_dialog(self.id, prompt_message)

