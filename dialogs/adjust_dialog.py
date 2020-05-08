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

from .cancel_and_help_dialog import CancelAndHelpDialog

class AdjustDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(AdjustDialog, self).__init__(dialog_id or AdjustDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.ask_step, self.act_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def ask_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)

        adjust_details = step_context.options

        message_text = (
            str(step_context.options)
            if step_context.options
            else "请说调整建议"
        )

        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

        return await step_context.next(adjust_details.adjust)

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        # Capture the response to the previous step's prompt
        adjust_details.adjust = use_cal(step_context.result)

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








