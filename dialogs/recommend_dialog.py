# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints, Attachment
from .cancel_and_help_dialog import CancelAndHelpDialog
from helpers.use_helper import use_cal
from helpers.looking_helper import looking_cal
from helpers.cost_helper import cost_cal
from helpers.ok_helper import is_ok


from recommend.recommend import recommend

import json
import os.path
import time

class RecommendDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(RecommendDialog, self).__init__(dialog_id or RecommendDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.use_step,
                    self.cost_step,
                    self.looking_step,
                    self.confirm_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def use_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        if product_details.use is None:
            message_text = "您购买这台笔记本是用于什么用途呢？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.use)

    async def cost_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.use = use_cal(step_context.result)

        #if product_details.cost is None:
        message_text = "您购买这台笔记本的预算大约是多少元呢？"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
        return await step_context.next(product_details.cost)


    async def looking_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        product_details = step_context.options

        # Capture the response to the previous step's prompt
        product_details.cost = cost_cal(step_context.result)

        if product_details.looking is None:
            message_text = "您对电脑的外观有什么要求呢？"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(product_details.looking)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        product_details = step_context.options

        # Capture the results of the previous step
        product_details.looking = looking_cal(step_context.result)

        message_text = (
            #f"请确认：您购买电脑是为了 { product_details.use } 用途。"
            #f"您的预算为：{ product_details.cost['low'] }-{ product_details.cost['high'] }。"
            #f"您的外观需求为：{ product_details.looking}。"
            f"紧张计算中……"
        )
        time.sleep(1)
        calculating_message = MessageFactory.text(
            message_text, message_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(calculating_message)

        return await step_context.next(product_details.looking)


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            product_details = step_context.options

            recommend_id, recommend_result = recommend(product_details.use,product_details.looking,product_details.cost)


            welcome_card = self.create_adaptive_card_attachment(recommend_id)
            response = MessageFactory.attachment(welcome_card)
            await step_context.context.send_activity(response)

            message_text = str(recommend_result)
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )    
            await step_context.context.send_activity(prompt_message)

            return await step_context.end_dialog(product_details)
        return await step_context.end_dialog()


    # Load attachment from file.
    def create_adaptive_card_attachment(self,id):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "../json/test.json")
        img_path = '/Users/fowillwly/Dev/shopping_bot/sources/img/'+str(id+1)+'.png'
        print(img_path)
        with open(path) as in_file:
            card = json.load(in_file)
            card['body'][0]['url'] = img_path
        with open('/Users/fowillwly/Dev/shopping_bot/sources/test.txt','w+') as f:
            f.write(str(card))
        print(card)
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )
