from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints, Attachment

from product_details import ProductDetails
from recognizer import ShoppingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from helpers.pointExtract_helper import pointExtract 

from .cancel_and_help_dialog import CancelAndHelpDialog

from recommend.adjust_recommend import adjust

import os
import json

from helpers.ok_helper import is_ok




class AdjustDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(AdjustDialog, self).__init__(dialog_id or AdjustDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.ask_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def ask_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        message_text = ("请说调整建议")

        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )


    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        details = step_context.context.activity.text
        score_dict = pointExtract(details)
        #price = {'low':1,'high':20000}
        recommend_id, recommend_result= adjust(score_dict)

        welcome_card = self.create_adaptive_card_attachment(recommend_id)
        response = MessageFactory.attachment(welcome_card)
        await step_context.context.send_activity(response)

        message_text = str(recommend_result)
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.ignoring_input
        )    
        await step_context.context.send_activity(prompt_message)

        #return await step_context.end_dialog()
        msg_txt = (
            f"您对这个推荐结果满意吗？"
        )

        message = MessageFactory.text(msg_txt, msg_txt, InputHints.expecting_input)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        details = step_context.context.activity.text
        ok = is_ok(details)

        if ok:
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/satisfied.txt','w+') as f:
                f.write('Yes')
            return
        else:
            return await step_context.replace_dialog(self.id)

        # Load attachment from file.
    def create_adaptive_card_attachment(self,id):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/json/test.json")
        img_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/img/'+str(id+1)+'.png'
        #print(img_path)
        with open(path) as in_file:
            card = json.load(in_file)
            card['body'][0]['url'] = img_path
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/test.txt','w+') as f:
            f.write(str(card))
        #print(card)
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )








